import sys
import os

# Add current directory to path so we can import server
sys.path.append(os.getcwd())

try:
    from server import search_documentation
    print("Successfully imported search_documentation")
    print(f"Type: {type(search_documentation)}")
    print(f"Dir: {dir(search_documentation)}")
    
    query = "fastmcp"
    print(f"Searching for: {query}")

    # Try to find the callable
    if hasattr(search_documentation, 'fn'):
        print("Found 'fn' attribute, trying to call it...")
        results = search_documentation.fn(query)
    else:
        # Fallback: assume it might be callable despite previous error, or we need another way
        # But let's try to call it if it has __call__, otherwise fail
        print("Trying to call directly...")
        results = search_documentation(query)

    print("Results:")
    print(results)
    
    if "No results found" in results and "File:" not in results:
         pass
         
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
