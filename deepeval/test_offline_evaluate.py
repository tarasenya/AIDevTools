"""
Offline evaluation — standalone evaluate().

Run with:  python test_offline_evaluate.py

No pytest needed. Results are printed to the console and sent to
Confident AI if logged in. Does not raise on failure — use this
for ad-hoc analysis rather than CI/CD gates.
"""
from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric
from deepeval.dataset import EvaluationDataset, Golden
from agent_with_tools import run_agent

dataset = EvaluationDataset(goldens=[
    Golden(input="What is the powerhouse of the cell?"),
    Golden(input="How does photosynthesis work?"),
    Golden(input="What programming language is known for readability?"),
])

# Build test cases by running the agent against each golden.
test_cases = []
for golden in dataset.goldens:
    answer, retrieval_context = run_agent(golden.input)
    test_cases.append(
        LLMTestCase(
            input=golden.input,
            actual_output=answer,
            # retrieval_context is needed for FaithfulnessMetric;
            # it holds the chunks the agent retrieved from rag_search.
            retrieval_context=retrieval_context if retrieval_context else None,
        )
    )

# evaluate() runs all metrics against all test cases and prints a summary.
evaluate(
    test_cases=test_cases,
    metrics=[
        AnswerRelevancyMetric(threshold=0.7),
        FaithfulnessMetric(threshold=0.7),
    ],
)
