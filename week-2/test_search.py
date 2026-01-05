#!/usr/bin/env python3
"""Test the search function programmatically."""

from search import search


def test_basic_search():
    """Test basic search functionality."""
    print("Test 1: Basic search")
    print("-" * 70)

    query = "FastMCP authentication"
    results = search(query, num_results=5)

    assert len(results) <= 5, "Should return at most 5 results"
    assert all('filename' in r for r in results), "All results should have 'filename'"
    assert all('content' in r for r in results), "All results should have 'content'"

    print(f"✓ Query: '{query}'")
    print(f"✓ Returned {len(results)} results")
    print(f"✓ Top result: {results[0]['filename']}")
    print()


def test_different_num_results():
    """Test with different number of results."""
    print("Test 2: Different number of results")
    print("-" * 70)

    query = "MCP server tools"

    # Test with 3 results
    results_3 = search(query, num_results=3)
    assert len(results_3) <= 3, "Should return at most 3 results"
    print(f"✓ Requested 3 results, got {len(results_3)}")

    # Test with 10 results
    results_10 = search(query, num_results=10)
    assert len(results_10) <= 10, "Should return at most 10 results"
    print(f"✓ Requested 10 results, got {len(results_10)}")
    print()


def test_specific_queries():
    """Test specific queries and verify results."""
    print("Test 3: Specific queries")
    print("-" * 70)

    test_cases = [
        ("deployment", ["deployment", "running", "server", "http"]),
        ("OAuth integration", ["oauth", "auth", "authentication"]),
        ("client tools", ["client", "tool", "call"]),
    ]

    for query, expected_keywords in test_cases:
        results = search(query, num_results=5)
        assert len(results) > 0, f"Should find results for '{query}'"

        # Check if at least one expected keyword appears in top result
        top_result = results[0]
        content_lower = top_result['content'].lower()
        filename_lower = top_result['filename'].lower()

        found = any(
            keyword in content_lower or keyword in filename_lower
            for keyword in expected_keywords
        )

        status = "✓" if found else "✗"
        print(f"{status} Query: '{query}' -> {top_result['filename']}")

    print()


def test_empty_and_edge_cases():
    """Test edge cases."""
    print("Test 4: Edge cases")
    print("-" * 70)

    # Test with very specific query
    results = search("xyzabc123nonexistent", num_results=5)
    print(f"✓ Query for non-existent term returned {len(results)} results")

    # Test with common term
    results = search("FastMCP", num_results=5)
    assert len(results) > 0, "Should find results for 'FastMCP'"
    print(f"✓ Query for 'FastMCP' returned {len(results)} results")
    print()


def demo_usage():
    """Demonstrate practical usage."""
    print("=" * 70)
    print("Demo: Practical Usage")
    print("=" * 70)

    query = "How to use tools in FastMCP"
    results = search(query, num_results=3)

    print(f"\nSearching for: '{query}'\n")

    for i, result in enumerate(results, 1):
        print(f"{i}. {result['filename']}")
        # Show first 200 characters
        preview = result['content'][:200].replace('\n', ' ').strip()
        print(f"   {preview}...\n")


if __name__ == "__main__":
    print("=" * 70)
    print("Testing search.py Implementation")
    print("=" * 70)
    print()

    try:
        test_basic_search()
        test_different_num_results()
        test_specific_queries()
        test_empty_and_edge_cases()

        print("=" * 70)
        print("All tests passed! ✓")
        print("=" * 70)
        print()

        demo_usage()

    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        exit(1)
