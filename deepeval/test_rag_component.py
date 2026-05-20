"""
Component-wise RAG evaluation.

Run with:  python test_rag_component.py
       or: deepeval run test_rag_component.py  (for the pytest section)

Tests the RAG pipeline in two layers:
  - Retriever: did it fetch relevant and complete chunks?
  - Generator: did it use those chunks faithfully?

This is separate from end-to-end agent evaluation — here we call
rag_search directly, bypassing the agent, to isolate the retriever.
"""
import pytest
from deepeval import evaluate, assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import (
    ContextualPrecisionMetric,
    ContextualRecallMetric,
    ContextualRelevancyMetric,
    FaithfulnessMetric,
    AnswerRelevancyMetric,
)
from deepeval.dataset import EvaluationDataset, Golden
from agent_with_tools import rag_search, run_agent


# Goldens include expected_output — needed for Precision and Recall metrics.
dataset = EvaluationDataset(goldens=[
    Golden(
        input="What is the powerhouse of the cell?",
        expected_output="The mitochondria is the powerhouse of the cell and produces ATP.",
    ),
    Golden(
        input="How does photosynthesis work?",
        expected_output="Photosynthesis converts sunlight, water, and CO2 into glucose and oxygen.",
    ),
    Golden(
        input="What is DNA?",
        expected_output="DNA is a double helix structure made of nucleotide base pairs.",
    ),
])


def build_rag_test_case(golden: Golden) -> LLMTestCase:
    """Call rag_search directly and the agent to get retrieval_context and actual_output."""
    # Retrieve context directly from rag_search (component isolation).
    raw = rag_search.invoke({"query": golden.input, "k": 5})
    retrieval_context = [line.lstrip("- ") for line in raw.splitlines() if line.strip()]

    # Run the full agent to get the final answer.
    answer, _ = run_agent(golden.input)

    return LLMTestCase(
        input=golden.input,
        actual_output=answer,
        expected_output=golden.expected_output,
        retrieval_context=retrieval_context,
    )


# --- Option A: standalone evaluate() ---

if __name__ == "__main__":
    test_cases = [build_rag_test_case(g) for g in dataset.goldens]

    # Retriever metrics — score the quality of retrieved chunks.
    print("=== Retriever evaluation ===")
    evaluate(
        test_cases=test_cases,
        metrics=[
            ContextualRelevancyMetric(threshold=0.7),   # are chunks relevant to the question?
            ContextualPrecisionMetric(threshold=0.7),   # are all retrieved chunks useful?
            ContextualRecallMetric(threshold=0.7),      # did retrieval cover the expected answer?
        ],
    )

    # Generator metrics — score how well the model used the retrieved chunks.
    print("=== Generator evaluation ===")
    evaluate(
        test_cases=test_cases,
        metrics=[
            FaithfulnessMetric(threshold=0.7),          # no hallucinations beyond the context?
            AnswerRelevancyMetric(threshold=0.7),        # is the answer on-topic?
        ],
    )


# --- Option B: pytest + assert_test (run with: deepeval run test_rag_component.py) ---

@pytest.mark.parametrize("golden", dataset.goldens)
def test_rag_retriever(golden: Golden):
    test_case = build_rag_test_case(golden)
    assert_test(test_case, metrics=[
        ContextualRelevancyMetric(threshold=0.7),
        ContextualPrecisionMetric(threshold=0.7),
        ContextualRecallMetric(threshold=0.7),
    ])


@pytest.mark.parametrize("golden", dataset.goldens)
def test_rag_generator(golden: Golden):
    test_case = build_rag_test_case(golden)
    assert_test(test_case, metrics=[
        FaithfulnessMetric(threshold=0.7),
        AnswerRelevancyMetric(threshold=0.7),
    ])
