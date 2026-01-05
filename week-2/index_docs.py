#!/usr/bin/env python3
"""Index markdown documentation files using minsearch."""

import os
from pathlib import Path
from minsearch import Index
import pickle

def find_markdown_files(root_dir="."):
    """Find all .md and .mdx files, excluding .git and __pycache__."""
    markdown_files = []
    root_path = Path(root_dir)

    for pattern in ["**/*.md", "**/*.mdx"]:
        for file_path in root_path.glob(pattern):
            # Skip files in .git and __pycache__ directories
            if ".git" in file_path.parts or "__pycache__" in file_path.parts:
                continue
            markdown_files.append(file_path)

    return sorted(markdown_files)

def read_file_content(file_path):
    """Read file content, return empty string if error."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

def index_documents():
    """Index all markdown files."""
    print("Finding markdown files...")
    markdown_files = find_markdown_files()
    print(f"Found {len(markdown_files)} markdown files")

    # Create documents
    print("Reading file contents...")
    docs = []
    for file_path in markdown_files:
        content = read_file_content(file_path)
        if content:
            docs.append({
                "filename": str(file_path),
                "content": content
            })

    print(f"Successfully read {len(docs)} files")

    # Create and fit the index
    print("Creating index...")
    index = Index(
        text_fields=["content", "filename"],
        keyword_fields=[]
    )

    print("Fitting index...")
    index.fit(docs)

    print(f"Index created with {len(docs)} documents")

    # Save the index
    print("Saving index to 'docs_index.pkl'...")
    with open('docs_index.pkl', 'wb') as f:
        pickle.dump(index, f)

    print("Done!")
    return index, docs

def test_search(index):
    """Test the search functionality."""
    print("\n" + "="*50)
    print("Testing search...")
    print("="*50)

    test_queries = [
        "FastMCP server",
        "authentication oauth",
        "tools decorator"
    ]

    for query in test_queries:
        print(f"\nQuery: '{query}'")
        results = index.search(query, num_results=3)
        for i, result in enumerate(results, 1):
            print(f"  {i}. {result['filename']}")
            # Show first 100 chars of content
            content_preview = result['content'][:100].replace('\n', ' ')
            print(f"     {content_preview}...")

if __name__ == "__main__":
    index, docs = index_documents()
    test_search(index)
