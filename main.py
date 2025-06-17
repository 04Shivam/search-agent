from dotenv import load_dotenv
from typing import TypedDict, Annotated, List, Dict

from langgraph.graph.message import add_messages
from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt import ToolNode

from chains import chat_model_tools_chain, chat_model_structured_chain, tools, OutputFormat
from prompts import HUMAN_PROMPT

load_dotenv()

class State(TypedDict):
    messages: Annotated[List, add_messages]
    output_json: Annotated[Dict, "Contains the final output of the graph in json format"]

def chat_model_tools_call(state: State):
    print("\n[+] Calling chat_model_tools_chain...")
    response = chat_model_tools_chain.invoke({"messages": state["messages"]})
    print("[+] Response from chat_model_tools_chain received.")
    return {"messages": [response]}

def chat_model_structured_call(state: State):
    print("\n[+] Calling chat_model_structured_chain...")
    response = chat_model_structured_chain.invoke({"messages": state["messages"]})
    print("[+] Final structured response received.")
    return {"output_json": response.model_dump_json()}

def tool_call(state: State):
    ai_message = state["messages"][-1]
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        print("[+] Tools were called in AI message. Routing to tools...")
        return "tools"
    print("[+] No tools called. Routing to structured model...")
    return "chat_model_structured"

# Node Labels
chat_model_tools = "chat_model_tools"
chat_model_structured = "chat_model_structured"
tools_label = "tools"

# Tool node
tool_node = ToolNode(tools=tools)

# Build the graph
graph_builder = StateGraph(State)
graph_builder.add_node(chat_model_tools, chat_model_tools_call)
graph_builder.add_node(chat_model_structured, chat_model_structured_call)
graph_builder.add_node(tools_label, tool_node)

graph_builder.add_edge(START, chat_model_tools)
graph_builder.add_conditional_edges(chat_model_tools, tool_call, {"tools": tools_label, "chat_model_structured": chat_model_structured})
graph_builder.add_edge(tools_label, chat_model_structured)
graph_builder.add_edge(chat_model_structured, END)

graph = graph_builder.compile()

# Main interaction loop
while True:
    query = input("\n[User] Enter your query (type 'exit' to quit): ")
    if query.strip().lower() == "exit":
        print("[+] Exiting the assistant. Goodbye!")
        break

    description = input("[User] Enter a description for the query: ")

    human_message = HUMAN_PROMPT.format(query=query, description=description)
    state = State(messages=[human_message])

    final_state = None
    for chunk in graph.stream(state):
        final_state = chunk
        print(f"\n[Graph Chunk]: {chunk}")

    if final_state and "output_json" in final_state[chat_model_structured]:
        print("\n[Final Output JSON]:")
        print(final_state[chat_model_structured]["output_json"])
    else:
        print("\n[!] No final output was returned.")
