# deepeval — Concepts & Evaluation Guide
Aim: Test and Observe. More than a syntax sugar.

Test what?
1. Agents, LLM Applications <- V1
2. RAG <- V1
3. MCP <- V3
4. Chatbot <- V3
   
Test/Observe how?
1. Online(observe)/Offline, CI/CD
2. One Turn (V1) vs Multi Turn (V3)
3. E2E, Component Eval.
4. Built in metrics (most of them LLM-as-a-Judge style)
   
What else? <- V3, V4
1. Synthetising data.
2. LLM Arena.
3. Prompt optimization.
4. Benchmarking of LLM.   

## Talk Outline: Evaluating Agents and RAGs with deepeval

**Scope:** one-turn evaluation only. Multi-turn, chatbot, MCP, and LLM arena covered in a follow-up talk.

**1. Why evaluation matters**
- LLMs are non-deterministic — you can't just read the code to know if it works
- Manual spot-checking doesn't scale
- Need a systematic, repeatable way to measure quality

**2. Core building blocks**
- `LLMTestCase` — the unit of evaluation (input + output + optional context)
- `Golden` — a test case without output; you fill it in by running your app
- `Dataset` — a collection of goldens
- Metrics — LLM judges that score a test case on a 0–1 scale

**3. E2E vs component-level evaluation**
- Same workflow, different granularity
- E2E: final input → final output, `AnswerRelevancyMetric`, `FaithfulnessMetric`
- Component: retriever gets `ContextualPrecision/Recall`, generator gets `Faithfulness`
- Agent tool selection: `ToolCorrectnessMetric` (offline only — needs `expected_tools`)
- Demo: `test_rag_component.py` + `test_tool_correctness.py`

**4. Running evaluations: pytest vs evaluate()**
- `evaluate()` — scores, not pass/fail; use while iterating and tuning
- pytest + `assert_test` — CI/CD gate; use once you know what "good" looks like
- Typical flow: explore with `evaluate()` → lock in threshold → add to pytest
- Results always saved locally to `.deepeval/.latest_test_run.json`
- Demo: `test_offline_evaluate.py` + `test_offline_pytest.py`

**5. Custom metrics with GEval**
- When built-in metrics don't capture your requirement
- Define any criterion in natural language; LLM judge scores against it
- Example: conciseness, professional tone, domain-specific correctness

**6. Observability (brief)**
- `@observe` + `update_current_span` + `CallbackHandler` — for production monitoring
- Not a testing tool — sends traces to Confident AI dashboard
- Requires work email account; all offline evaluation works without it

## Core Concepts

### TestCase
- **`LLMTestCase`** — single input/output pair (one-turn). Fields: `input`, `actual_output`, optionally `expected_output`, `retrieval_context`, `context`, `tools_called`, `expected_tools`.
- **`ConversationalTestCase`** — list of `LLMTestCase` turns (multi-turn chat). Out of scope for this talk.

### Golden
A `LLMTestCase` without `actual_output` — holds the input (and optionally expected output). You run your app against it, then fill in `actual_output` to get a full test case.

### Dataset
`EvaluationDataset` — a collection of `Golden`s or `LLMTestCase`s. Built in code or loaded from Confident AI (deepeval's cloud platform).

### Metrics
Each metric uses an LLM judge. Requires specific `LLMTestCase` fields:

| Metric | What it measures | Required fields |
|---|---|---|
| `AnswerRelevancyMetric` | Is output relevant to input? | `input`, `actual_output` |
| `FaithfulnessMetric` | Does output stick to retrieved context? | `actual_output`, `retrieval_context` |
| `ContextualRelevancyMetric` | Is retrieved context relevant? | `input`, `retrieval_context` |
| `ContextualPrecisionMetric` | Are all retrieved chunks useful? | `input`, `expected_output`, `retrieval_context` |
| `ContextualRecallMetric` | Did retrieval cover everything needed? | `expected_output`, `retrieval_context` |
| `HallucinationMetric` | Does output contain made-up facts? | `actual_output`, `context` |
| `ToolCorrectnessMetric` | Did agent call the right tools? | `input`, `tools_called`, `expected_tools` |
| `GEval` | Custom criterion defined in natural language | depends on `evaluation_params` |

---

## Evaluation Modes

| Mode | How to run | Needs ground truth | Use case |
|---|---|---|---|
| pytest + `assert_test` | `deepeval test run test_*.py` | yes | CI/CD gate |
| standalone `evaluate()` | `python script.py` | yes | ad-hoc analysis |
| `@observe` (online) | runs in prod | no* | production monitoring |

*`ToolCorrectnessMetric` requires `expected_tools` — ground truth you don't have in production. **Only use it offline.** Online-safe metrics: `AnswerRelevancyMetric`, `FaithfulnessMetric`.

### When to use evaluate() over pytest

`assert_test` enforces a threshold — pass/fail, stops on failure. Use it for CI/CD gates once you know what "good" looks like.

`evaluate()` returns actual scores across all cases. Use it when you need to *understand*, not just *enforce*: tuning prompts, calibrating thresholds, debugging a CI failure, or working in a notebook where you want to process or log results programmatically.

Typical flow: iterate with `evaluate()` → once scores stabilize, codify the threshold into a pytest test.

### pytest vs evaluate()

| | pytest + `assert_test` | `evaluate()` |
|---|---|---|
| Run with | `deepeval test run test_*.py` | `python script.py` |
| On failure | test fails, CI blocks | prints result, continues |
| Granularity | one test per golden | all cases in one batch |
| Use case | CI/CD gate | exploration, debugging |

### Offline — pytest
```python
@pytest.mark.parametrize("golden", dataset.goldens)
def test_agent(golden: Golden):
    output = my_app(golden.input)
    assert_test(LLMTestCase(input=golden.input, actual_output=output),
                metrics=[AnswerRelevancyMetric(threshold=0.7)])
```

### Offline — standalone
```python
test_cases = [LLMTestCase(input=g.input, actual_output=my_app(g.input)) for g in dataset.goldens]
evaluate(test_cases=test_cases, metrics=[AnswerRelevancyMetric()])
```

### Online
```python
@observe(type="llm", metrics=[AnswerRelevancyMetric()])
def run_agent(prompt: str):
    result = my_app(prompt)
    update_current_span(test_case=LLMTestCase(input=prompt, actual_output=result))
    return result
```

---

## E2E vs Component-level Evaluation

These are not two separate workflows — the same `LLMTestCase` + metrics pattern, at different granularities.

**End-to-end** — treat the whole app as one black box. One test case per run: final input → final output. Use `AnswerRelevancyMetric`, `FaithfulnessMetric`.

**Component-level** — evaluate internal components separately: retriever, generator, tool selection. Same `LLMTestCase`, but `retrieval_context` is populated from the actual retriever output, not the final answer. Use retrieval metrics (`ContextualPrecisionMetric`, `ContextualRecallMetric`, `ContextualRelevancyMetric`) on the retriever, faithfulness metrics on the generator.

| Component | Metrics |
|---|---|
| Retriever | `ContextualPrecisionMetric`, `ContextualRecallMetric`, `ContextualRelevancyMetric` |
| Generator | `FaithfulnessMetric`, `AnswerRelevancyMetric` |
| Agent tool selection | `ToolCorrectnessMetric` (offline only) |

---

## Agent vs RAG Evaluation

### End-to-end agent
Given an input, does the final answer make sense? → `AnswerRelevancyMetric`, `FaithfulnessMetric`

### Tool correctness (offline only)
Did the agent call the right tools? → `ToolCorrectnessMetric`. Requires `tools_called` (extracted from agent messages) and `expected_tools` (defined per test case). Scoring modes: default (name match, no ordering), `should_consider_ordering=True` (LCS), `should_exact_match=True` (all-or-nothing).

### Component-wise RAG
Test retriever and generator separately. `retrieval_context` must be populated with actual retrieved chunks. `expected_output` needed for Precision/Recall.

---

## Observability: Spans and Traces

Primarily for production monitoring, not testing. Requires Confident AI account (work email).

A **trace** is the full execution tree of one request. A **span** is one node in that tree — inputs, outputs, duration, metric scores.

```
trace (one user request)
└── span: run_agent        (type="llm")   ← scored by metrics
    ├── span: rag_search   (type="tool")  ← auto-created by CallbackHandler
    └── span: web_search   (type="tool")  ← auto-created by CallbackHandler
```

**`@observe(type=..., metrics=[...])`** — creates a span shell: records function args, return value, and duration. `type=` is just a label — it controls which metrics are valid to attach. deepeval has no access to function internals.

**`update_current_span(test_case=...)`** — you manually attach a structured `LLMTestCase` so metrics have `input`, `actual_output`, `retrieval_context`, etc. Without this, the span has raw args but nothing for metrics to score.

**`CallbackHandler()`** — hooks into LangChain's internal events (tool started/ended, LLM called) and auto-creates child spans. Without it, the agent's internals are a black box to deepeval.

### Online vs Offline: Why Spans?

| | `evaluate()` offline | `@observe` online |
|---|---|---|
| When | explicit test run | every prod request |
| Latency | blocks | background |
| Tool visibility | none | nested child spans |
| Trends over time | no | yes (Confident AI) |

Local results are always saved to `.deepeval/.latest_test_run.json` regardless of mode.

### Span types

| Span type | Valid metrics |
|---|---|
| `"llm"` | `AnswerRelevancyMetric`, `FaithfulnessMetric`, `HallucinationMetric` |
| `"retriever"` | `ContextualRecallMetric`, `ContextualPrecisionMetric` |
| `"agent"` | `ConversationCompletenessMetric`, `ConversationRelevancyMetric` |
| `"tool"` | observability only |

Use `type="llm"` even when wrapping a LangChain agent if you want `LLMTestCase`-based metrics — `type="agent"` requires `ConversationalTestCase`.

---

## Technical: Azure OpenAI

Two places need config: the LangChain agent and the deepeval metric judge.

Via `.env` (recommended — both clients pick up vars automatically):
```
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
OPENAI_API_VERSION=2024-02-01
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=...   # LangChain
AZURE_DEPLOYMENT_NAME=...               # deepeval
AZURE_MODEL_NAME=gpt-4o-mini            # deepeval
```

---

## Code Files

| File | Description |
|---|---|
| `agent_with_tools.py` | Agent with `web_search` (DuckDuckGo) + `rag_search` (mock KB). `run_agent()` returns `(answer, retrieval_context)`. `run_agent_with_tool_trace()` also returns `List[ToolCall]` for tool correctness tests. |
| `test_offline_pytest.py` | Offline — pytest + `assert_test` |
| `test_offline_evaluate.py` | Offline — standalone `evaluate()` |
| `test_online.py` | Online — `@observe`, answer quality only |
| `test_rag_component.py` | Component-wise RAG, both pytest and standalone |
| `test_tool_correctness.py` | Tool selection tests, both pytest and standalone |

---

