"""
Online evaluation — @observe + update_current_span.

Run with:  python test_online.py

Simulates production usage: each call is scored as it executes.
In a real system this function would be called by your API handler.
Traces (with scores) are sent to Confident AI if logged in.

Only metrics that don't require ground truth are used here:
  - AnswerRelevancyMetric: needs only input + actual_output
  - FaithfulnessMetric:    needs actual_output + retrieval_context

ToolCorrectnessMetric is NOT used online — it requires expected_tools,
which is ground truth you don't have in production. Use it offline instead.
"""
from deepeval.tracing import observe, update_current_span
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric
from deepeval.integrations.langchain import CallbackHandler
from agent_with_tools import agent

# Create a span - place/container to attach scores
# update_current_span - put objects to this container
# Trigger metric during a call -> close a span
# Results are sent to ConfidentAI. Note type
@observe(type="llm", metrics=[AnswerRelevancyMetric(), FaithfulnessMetric()])
def run_agent_observed(prompt: str):
    result = agent.invoke(
        {"messages": [{"role": "user", "content": prompt}]},
        config={"callbacks": [CallbackHandler()]},
    ) # here we feed datra to the current span: LLM, tool invocation,lattency

    retrieval_context = []
    for msg in result["messages"]:
        if hasattr(msg, "name") and msg.name == "rag_search":
            retrieval_context.extend(
                line.lstrip("- ") for line in msg.content.splitlines() if line.strip()
            )

    answer = result["messages"][-1].content
    update_current_span(
        test_case=LLMTestCase(
            input=prompt,
            actual_output=answer,
            retrieval_context=retrieval_context if retrieval_context else None,
        )
    )
    return answer


if __name__ == "__main__":
    for prompt in [
        "What is the powerhouse of the cell?",
        "How does photosynthesis work?",
        "What programming language is known for readability?",
    ]:
        print(f"Q: {prompt}")
        print(f"A: {run_agent_observed(prompt)}\n")
