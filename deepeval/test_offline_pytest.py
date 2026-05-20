"""
Offline evaluation — pytest + assert_test.

Run with:  deepeval run test_offline_pytest.py

Each golden becomes one pytest test. The suite fails if any metric
falls below its threshold. Suitable for CI/CD gates.
"""
import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from deepeval.metrics import AnswerRelevancyMetric, GEval
from deepeval.dataset import EvaluationDataset, Golden
from agent_with_tools import run_agent

dataset = EvaluationDataset(goldens=[
    Golden(input="What is the powerhouse of the cell?"),
    Golden(input="How does photosynthesis work?"),
    Golden(input="What programming language is known for readability?"),
])

bam_metric = GEval(name="BAM metric",
                   criteria="The output is funny, not funny is evaluated with 0, somehow funny with 0.5, very funny with 1",
                   evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
                   threshold=0.6)

# One test function per golden — pytest parametrize handles the loop.
# Typical e2e test!
@pytest.mark.parametrize("golden", dataset.goldens)
def test_agent_answer_relevancy(golden: Golden):
    answer, _ = run_agent(golden.input)

    test_case = LLMTestCase(
        input=golden.input,
        actual_output=answer,
    )
    # assert_test raises AssertionError if the metric score < threshold,
    # which causes the pytest test to fail.
    assert_test(test_case, metrics=[AnswerRelevancyMetric(threshold=0.7), bam_metric])
