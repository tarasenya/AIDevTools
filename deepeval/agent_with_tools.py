import random
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from deepeval.test_case import ToolCall

load_dotenv("../.env")



KNOWLEDGE_BASE = [
    "The mitochondria is the powerhouse of the cell and produces ATP through cellular respiration.",
    "Photosynthesis converts sunlight, water, and CO2 into glucose and oxygen.",
    "The speed of light in a vacuum is approximately 299,792,458 meters per second.",
    "DNA is a double helix structure made of nucleotide base pairs: A-T and C-G.",
    "The French Revolution began in 1789 and led to the rise of Napoleon Bonaparte.",
    "Gravity is described by Einstein's general relativity as the curvature of spacetime.",
    "The human brain contains approximately 86 billion neurons.",
    "Water boils at 100°C at sea level and freezes at 0°C under standard pressure.",
    "The Amazon rainforest produces about 20% of the world's oxygen.",
    "Python is an interpreted, high-level programming language known for its readability.",
    "Machine learning is a subset of AI where models learn patterns from data.",
    "The periodic table organizes elements by atomic number and chemical properties.",
    "Shakespeare wrote 37 plays and 154 sonnets during his lifetime.",
    "The Great Wall of China stretches over 21,000 kilometers.",
    "Black holes are regions of spacetime where gravity is so strong nothing can escape.",
    "The human genome contains approximately 3 billion base pairs.",
    "Quantum mechanics describes the behavior of matter at atomic and subatomic scales.",
    "The Renaissance was a cultural movement in Europe spanning the 14th to 17th centuries.",
    "Neural networks are inspired by the structure and function of biological brains.",
    "The Earth is approximately 4.5 billion years old.",
]



@tool
def web_search(query: str) -> str:
    """Search the web for current information using DuckDuckGo."""
    search = DuckDuckGoSearchRun()
    return search.run(query)


@tool
def rag_search(query: str, k: int = 3) -> str:
    """Search the internal knowledge base and return k relevant documents."""
    results = random.sample(KNOWLEDGE_BASE, min(k, len(KNOWLEDGE_BASE)))
    return "\n".join(f"- {r}" for r in results)




llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

agent = create_agent(
    model=llm,
    tools=[web_search, rag_search],
    system_prompt=(
        "You are a helpful assistant. "
        "Use rag_search for general knowledge questions. "
        "Use web_search for current events or real-time information. "
        "Be concise."
    ),
)


def run_agent(prompt: str) -> tuple[str, list[str]]:
    """Run the agent and return (final_answer, retrieved_context)."""
    result = agent.invoke({"messages": [{"role": "user", "content": prompt}]})

    retrieval_context = []
    for msg in result["messages"]:
        if hasattr(msg, "name") and msg.name == "rag_search":
            retrieval_context.extend(
                line.lstrip("- ") for line in msg.content.splitlines() if line.strip()
            )

    answer = result["messages"][-1].content
    return answer, retrieval_context


def run_agent_with_tool_trace(prompt: str) -> tuple[str, list[str], list[ToolCall]]:
    """Run the agent and return (final_answer, retrieved_context, tools_called).

    tools_called contains ToolCall objects with name, input_parameters, and output,
    suitable for use with deepeval's ToolCorrectnessMetric.
    """
    result = agent.invoke({"messages": [{"role": "user", "content": prompt}]})
    tools_called = []
    retrieval_context = []

    for msg in result["messages"]:
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            for tc in msg.tool_calls:
                # Match each tool call to its ToolMessage output by tool_call_id.
                output = next(
                    (m.content for m in result["messages"]
                     if hasattr(m, "tool_call_id") and m.tool_call_id == tc["id"]),
                    None,
                )
                tools_called.append(ToolCall(
                    name=tc["name"],
                    input_parameters=tc["args"],
                    output=output,
                ))
                if tc["name"] == "rag_search" and output:
                    retrieval_context.extend(
                        line.lstrip("- ") for line in output.splitlines() if line.strip()
                    )

    answer = result["messages"][-1].content
    return answer, retrieval_context, tools_called
