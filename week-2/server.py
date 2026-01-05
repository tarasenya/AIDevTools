from fastmcp import FastMCP

mcp = FastMCP("Demo 🚀")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool
def read_url(url: str, target_selector: str = None) -> str:
    """Read content of a URL using Jina Reader.
    
    Args:
        url: The URL to read.
        target_selector: Optional CSS selector to target specific content (e.g. "#readme").
    """
    import requests
    jina_url = f"https://r.jina.ai/{url}"
    headers = {}
    if target_selector:
        headers["X-Target-Selector"] = target_selector
    response = requests.get(jina_url, headers=headers)
    return response.text

@mcp.tool
def search_documentation(query: str) -> str:
    """
    Search the documentation for a given query.
    
    Args:
        query: The search query.
    """
    from search_docs import query_index
    results = query_index(query)
    
    if not results:
        return "No results found."
        
    formatted_results = []
    for i, result in enumerate(results, 1):
        content_preview = result['content'][:300].replace('\n', ' ')
        formatted_results.append(f"{i}. File: {result['filename']}\n   Content: {content_preview}...")
        
    return "\n\n".join(formatted_results)

if __name__ == "__main__":
    mcp.run()
