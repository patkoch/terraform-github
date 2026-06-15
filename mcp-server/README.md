# Terraform Versions MCP Server

This MCP server exposes tools for retrieving the latest Terraform CLI version and the latest Terraform GitHub provider version.

## VS Code Configuration

The workspace already contains a VS Code MCP configuration at `.vscode/mcp.json`:

```json
{
	"servers": {
		"terraform-versions": {
			"type": "stdio",
			"command": "${workspaceFolder}/mcp-server/.venv/bin/python",
			"args": [
				"-m",
				"terraform_versions_mcp.server"
			],
			"cwd": "${workspaceFolder}/mcp-server"
		}
	}
}
```

Before using it in VS Code, install the server dependencies once:

```bash
cd mcp-server
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e .
```

After that, reload VS Code and start or restart the `terraform-versions` MCP server from the MCP server controls.

The main repository README contains the full setup, start, stop, VS Code integration, and usage examples.