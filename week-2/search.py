#!/usr/bin/env python3
"""Search function for indexed markdown documentation."""

import pickle
from typing import List, Dict


def load_index():
    """Load the pickled minsearch index."""
    with open('docs_index.pkl', 'rb') as f:
        return pickle.load(f)


def search(query: str, num_results: int = 5) -> List[Dict[str, str]]:
    """
    Search the indexed documents and return the most relevant results.

    Args:
        query: The search query string
        num_results: Number of results to return (default: 5)

    Returns:
        List of dictionaries containing 'filename' and 'content' fields
    """
    index = load_index()
    results = index.search(query, num_results=num_results)
    return results


if __name__ == "__main__":
    # Test the search function
    print("Testing search function...")
    print("=" * 70)

    test_queries = [
        "How to create FastMCP server",
        "authentication and OAuth",
        "tools decorator",
        "client connection",
        "deployment options"
    ]

    for query in test_queries:
        print(f"\nQuery: '{query}'")
        print("-" * 70)

        results = search(query, num_results=5)

        if not results:
            print("No results found.")
            continue

        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['filename']}")
            # Show first 150 chars of content
            content_preview = result['content'][:150].replace('\n', ' ').strip()
            print(f"   Preview: {content_preview}...")

    print("\n" + "=" * 70)
    print("Test completed!")

    # Demonstrate programmatic usage
    print("\n" + "=" * 70)
    print("Example programmatic usage:")
    print("=" * 70)
    print("\nfrom search import search")
    print("\nresults = search('FastMCP tools')")
    print("for result in results:")
    print("    print(result['filename'])")
    print("    print(result['content'][:100])")
