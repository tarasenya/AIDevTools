    # Model Context Protocol (MCP)

In this homework, we will build our own MCP server - a clone of Context7.

For that, we will need:

- Select a GitHub repo with documentation
- Download the data from it
- Make it searchable

Let's start!


## Question 1: Create a New Project

Create a new project. We will use `uv` for dependency management. Install it if you don't have it:

```bash
pip install uv
```

Create a directory and initialize an empty project there:

```bash
uv init
```

Install fastmcp:

```bash
uv add fastmcp
``` 


In `uv.lock`, what's the first hash in the `wheels` section of `fastmcp`? Include the entire string without quotes.

e33cd622e1ebd5110af6a981804525b6cd41072e3c7d68268ed69ef3be651aca

## Question 2: FastMCP Transport

Now let's update the main file.

Use the starter code from [their docs](https://github.com/jlowin/fastmcp):

```python
from fastmcp import FastMCP

mcp = FastMCP("Demo 🚀")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

if __name__ == "__main__":
    mcp.run()
```


Run the server.

You'll see the welcome screen. What's the transport?

* STDIO <--- this
* HTTP
* HTTPS
* SSE


## Question 3: Scrape Web Tool

Now let's create a tool for downloading content of any web page. 

We'll use Jina reader for that.

To get content of any page in markdown, you simply need to add `r.jina.ai` in front of the address. For example: `https://r.jina.ai/https://datatalks.club`

Ask your AI assistant to create a tool based on this. You can ask it to use the `requests` library. 

I also recommend testing it. I used a prompt like that:

```
Create a file `test.py` which invokes this function to test that it works well
```

Test it to retrieve the content of `https://github.com/alexeygrigorev/minsearch`. How many characters does it return? 


* 1184
* 9184 <--- this
* 19184
* 29184

Select the closest answer if you don't get the exact match.


## Question 4: Integrate the Tool

Integrate the MCP tool into your AI assistant. 

The command for running the MCP server is this:

```bash
uv --directory ~/path/to/homework run python main.py
```

(or `C:/Users/username/path/to/homework` if you're on Windows)

Replace the directory with the full path to this project

Ask it the following:

```
Count how many times the word "data" appears on https://datatalks.club/
Use available MCP tools for that
```

What's the answer?

* 61 <-- this
* 111
* 161
* 261

Select the closest answer if you don't get the exact match.


## Question 5: Implement Search (2 points)

Now ask the agent to: 

* Download https://github.com/jlowin/fastmcp/archive/refs/heads/main.zip. Don't download it if it's already downloaded
* Iterate over all zip files but read only md and mdx ones 
* Remove the first part of the path in the filename. So "fastmcp-main/docs/getting-started/welcome.mdx" becomes "docs/getting-started/welcome.mdx"
* Index these files with minsearch. Put the text content in "content" field and filename in "filename" 
* Use https://github.com/alexeygrigorev/minsearch to learn how to use minsearch
* Create a search function that retrieves 5 most relevant documents from the index
* Create search.py and test the implementation there

What's the first file returned that you get with the query "demo"? 

* README.md
* docs/servers/context.mdx
* examples/testing_demo/README.md <-- this
* docs/python-sdk/fastmcp-settings.mdx


## Question 6: Search Tool (ungraded)

Now you can ask your assistant to implement it as a tool in main.py - and voila, you have a documentation search engine in your AI assistant!

# Claude Conversation Log

Session ID: f7efeed6-682a-4057-809c-f6c5683ff174
Date: 2026-01-05 16:38:47

---

## 👤 User

what mcp tool you can use

---

## 🤖 Claude

I have access to the following MCP tools:

## From `mcp-course-server`:

1. **add** - Add two numbers
   - Parameters: `a` (integer), `b` (integer)

2. **read_url** - Read content of a URL using Jina Reader
   - Parameters: `url` (string), optional `target_selector` (CSS selector)

3. **search_documentation** - Search the documentation for a given query
   - Parameters: `query` (string)

## General MCP Resource Tools:

4. **ListMcpResourcesTool** - List available resources from configured MCP servers
   - Can optionally filter by server name

5. **ReadMcpResourceTool** - Read a specific resource from an MCP server
   - Parameters: `server` (required), `uri` (required)

Would you like me to demonstrate any of these tools or help you use them for a specific task?

---

## 👤 User

what are mcp tools decorator. Search the documentation 

---

## 🤖 Claude

Let me search with more specific queries to find information about MCP tools decorator:

---

## 👤 User

[Request interrupted by user for tool use]

---

## 👤 User

use search documentation but for query mcp tools

---

## 🤖 Claude

The search is returning limited content. Let me try reading a URL from the MCP documentation directly to get better information about tools:

---

## 🤖 Claude

Now let me search for Python-specific implementation details with decorators:

---

## 👤 User

[Request interrupted by user]

---



## Homework URL

Commit your code to GitHub. You can create a repository for this course. Within the repository, create a folder, e.g. "03-mcp", where you put the code.

Use the link to this folder in the homework submission form.


## Tip

You can copy-paste the homework description into the AI system of your choice. But make sure you understand (and follow) all the steps in the response.


## Submission

Submit your homework here: https://courses.datatalks.club/ai-dev-tools-2025/homework/hw3
