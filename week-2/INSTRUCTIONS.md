# Connecting Claude Code to MCP
1. Run
```bash
 claude mcp add mcp-course-server -- uv --directory /home/taras/my_code_for_courses/mcp-server run server.py
```
The output should be:
```bash
Added stdio MCP server mcp-course-server with command: uv --directory /home/taras/my_code_for_courses/mcp-server run server.py to local config
File modified: /home/taras/.claude.json [project: /home/taras/my_code_for_courses/mcp-server]
```
2. The corresponding part of `.claude.json` should be:
```json
    "/home/taras/my_code_for_courses/mcp-server": {
      "mcpContextUris": [],
      "mcpServers": {
        "mcp-course-server": {
            "/home/taras/my_code_for_courses/mcp-server",
        }
      }
    }
```
3. The call in Claude Code: [image.png](image.png)