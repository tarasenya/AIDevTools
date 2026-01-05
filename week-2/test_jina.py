from server import read_url

def test_read_url():
    url = "https://example.com"
    print(f"Testing read_url with {url}...")
    try:
        content = read_url.fn(url)
        print("Successfully fetched content:")
        print(content[:500])
    except Exception as e:
        print(f"Error: {e}")

def task_3_of_homework():
    url = "https://github.com/alexeygrigorev/minsearch"    
    try:
        content = read_url.fn(url, target_selector="article")
        print("Successfully fetched content")
        print(f'Length of content: {len(content)}')
        print("--- Content Preview ---")
        print(content[:1000])
        print("-----------------------")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    task_3_of_homework()
