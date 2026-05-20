"""
Tool correctness evaluation.

Tests whether the agent calls the right tools for a given input.
Does NOT evaluate the quality of the answer — only tool selection.

Run (pytest):     deepeval run test_tool_correctness.py
Run (standalone): python test_tool_correctness.py
"""
import pytest
from deepeval import assert_test, evaluate
from deepeval.test_case import LLMTestCase, ToolCall
from deepeval.metrics import ToolCorrectnessMetric
from agent_with_tools import run_agent_with_tool_trace

# ---------------------------------------------------------------------------
# Test cases: each entry defines the prompt and which tool(s) are expected.
# Only `name` is set on expected tools — we don't know args/output in advance.
# The metric matches by name only (default mode).
# ---------------------------------------------------------------------------

TOOL_TEST_CASES = [
    {
        "input": "What is the powerhouse of the cell?",
        # General knowledge → should use the internal knowledge base
        "expected_tools": [ToolCall(name="rag_search")],
    },
    {
        "input": "Who won the latest FIFA World Cup?",
        # Current event → should search the web
        "expected_tools": [ToolCall(name="web_search")],
    },
    {
        "input": "Tell me about DNA structure and the latest AI news",
        # Needs both: knowledge base for DNA, web for AI news
        "expected_tools": [ToolCall(name="rag_search"), ToolCall(name="web_search")],
    },
]

"""
from deepeval.metrics import ToolCorrectnessMetric
from deepeval.metrics.tool_correctness.schema import ToolCallParams

ToolCorrectnessMetric(
    threshold=0.5,
    evaluation_params=[
        ToolCallParams.TOOL_NAME,
        ToolCallParams.INPUT_PARAMETERS,  # adds param matching
    ]
)
"""
def build_tool_test_case(case: dict) -> LLMTestCase:
    answer, _, tools_called = run_agent_with_tool_trace(case["input"])
    return LLMTestCase(
        input=case["input"],
        actual_output=answer,
        tools_called=tools_called,
        expected_tools=case["expected_tools"],
    )


# ---------------------------------------------------------------------------
# Option A: pytest + assert_test  (deepeval test run test_tool_correctness.py)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("case", TOOL_TEST_CASES, ids=[c["input"][:40] for c in TOOL_TEST_CASES])
def test_tool_selection(case: dict):
    test_case = build_tool_test_case(case)

    # Default mode: score = (correctly named tools called) / (expected tools).
    # Order doesn't matter, input parameters are not compared.
    assert_test(test_case, metrics=[ToolCorrectnessMetric(threshold=0.5)])


@pytest.mark.parametrize(
    "case",
    [TOOL_TEST_CASES[2]],  # only the multi-tool case makes sense for ordering
    ids=["dna-and-ai-news"],
)
def test_tool_ordering(case: dict):
    test_case = build_tool_test_case(case)

    # Order-sensitive mode: rag_search should come before web_search.
    # Uses weighted LCS — partial credit if some tools are in the right order.
    assert_test(test_case, metrics=[
        ToolCorrectnessMetric(threshold=0.5, should_consider_ordering=True)
    ])


# ---------------------------------------------------------------------------
# Option B: standalone evaluate()  (python test_tool_correctness.py)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    test_cases = [build_tool_test_case(c) for c in TOOL_TEST_CASES]

    evaluate(
        test_cases=test_cases,
        metrics=[ToolCorrectnessMetric(threshold=0.5)],
    )
