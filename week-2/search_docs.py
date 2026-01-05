#!/usr/bin/env python3
"""Search indexed markdown documentation."""

import pickle
import sys

def load_index():
    """Load the pickled index."""
    with open('docs_index.pkl', 'rb') as f:
        return pickle.load(f)

def query_index(query, num_results=5):
    """Search the index and return results."""
    index = load_index()
    results = index.search(query, num_results=num_results)
    return results

def search(query, num_results=5):
    """Search the index and display results."""
    results = query_index(query, num_results)

    print(f"\nSearch results for: '{query}'")
    print("=" * 70)

    if not results:
        print("No results found.")
        return

    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['filename']}")
        print("-" * 70)
        # Show first 300 chars of content
        content_preview = result['content'][:300].replace('\n', ' ')
        print(f"{content_preview}...")
        print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python search_docs.py <query>")
        print("\nExample: python search_docs.py 'FastMCP authentication'")
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    search(query)
