# 🔍 Search Agent using LangGraph & LangChain

This project is an AI-powered query assistant built with [LangGraph](https://github.com/langchain-ai/langgraph) and [LangChain](https://www.langchain.com/). It intelligently handles natural language queries using a multi-step agent architecture that includes tool calling (e.g., web search via Tavily) and structured response formatting.

## 🚀 Features

- 🌐 Web-enhanced search with the Tavily Search tool
- 🧠 Context-aware conversation handling using `LangGraph` message passing
- 📦 Structured, JSON-formatted output for vulnerability-related queries
- ⚙️ Modular graph-based execution with conditional branching
- 🤖 Built-in support for LLMs via Ollama (`qwen3:4b`)

## 📁 Project Structure

```
├── main.py          # Main execution script with LangGraph flow
├── chains.py        # Defines the tools, prompts, and model chains
├── prompts.py       # Contains reusable prompt templates
├── .env             # Environment variables (e.g., for API keys)
```

## 📦 Requirements

- Python 3.10+
- Ollama installed and running (with `qwen3:4b` model pulled)
- Dependencies (install via pip):
  
```bash
pip3 install langchain langgraph langchain-community langchain-ollama pydantic python-dotenv
```

> Optional: Install and configure [Tavily](https://docs.tavily.com/) for web search integration.

## 🧪 How It Works

1. **User Input**: Accepts a query and description.
2. **LLM Tool Phase**: Uses a chat model to decide whether to call tools (like Tavily).
3. **Tool Invocation**: If needed, the tool is called to fetch more data.
4. **Structured Output**: Generates final JSON with vulnerability, remediation, and resources.

### Example JSON Output

```json
{
  "vulnerability": "Example vulnerability description",
  "Remediation": "Steps to fix the issue",
  "Resources": [
    "https://example.com/resource1",
    "https://example.com/resource2"
  ]
}
```

## 🧠 Powered By

- [LangChain](https://www.langchain.com/)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [Ollama](https://ollama.com/)
- [Tavily](https://www.tavily.com/)

## 📌 Notes

- Make sure to run Ollama with the correct model (`qwen3:4b`).
- The `.env` file is used for any secrets or API keys needed by Tavily or LangChain integrations.

## 📸 Demo

```bash
$ python main.py

[User] Enter your query (type 'exit' to quit): What is CVE-2023-23397?
[User] Enter a description for the query: Looking for remediation steps and references.

[Graph Chunk]: {...}
[Final Output JSON]:
{
  "vulnerability": "...",
  "Remediation": "...",
  "Resources": [...]
}
```
