from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from langchain_community.tools import TavilySearchResults

from prompts import SYSTEM_PROMPT
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

search_tool = TavilySearchResults(search_depth="basic")

tools = [search_tool]

class OutputFormat(BaseModel):
    vulnerability: str = Field(..., description= "Information about vulnerability.")
    Remediation: str = Field(..., description="Steps to remediate the vulnerabiltiy.")
    Resources: list = Field(..., description="Sources used to gather information")

chat_model = ChatOllama(
    model="qwen3:4b"
)

chat_model_tools = chat_model.bind_tools(tools=tools)
chat_model_structured = chat_model.with_structured_output( OutputFormat )

prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content=SYSTEM_PROMPT.format(tools=tools)),
    MessagesPlaceholder(variable_name="messages")
])

chat_model_tools_chain = prompt | chat_model_tools
chat_model_structured_chain = prompt | chat_model_structured