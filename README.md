# Terraform GitHub Examples

This repository contains examples for automating GitHub with Terraform. It also includes a local MCP server that can return the latest Terraform CLI version and the latest `integrations/github` Terraform provider version.

## MCP Server

The MCP server lives in `mcp-server/` and exposes these tools:

- `get_latest_github_provider_version`: returns the latest GitHub provider version from the Terraform Registry.
- `get_latest_terraform_cli_version`: returns the latest Terraform CLI version from the GitHub releases API.
- `get_latest_terraform_versions`: returns both versions in one response.

The server uses the official Python MCP SDK and communicates over stdio, which is the transport used by the VS Code configuration in `.vscode/mcp.json`.

## Prerequisites

- Python 3.11 or newer
- `pip`
- Internet access to call the Terraform Registry and GitHub API

## Install The MCP Server

From the repository root, create a virtual environment and install the local package:

```bash
cd mcp-server
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e .
```

## Start The MCP Server

For normal MCP usage, VS Code starts the server automatically from `.vscode/mcp.json`.

You can also start it manually from the repository root:

```bash
cd mcp-server
. .venv/bin/activate
python -m terraform_versions_mcp.server
```

When started manually, the process waits for MCP JSON-RPC messages on stdin. That is expected for a stdio MCP server.

## Stop The MCP Server

If VS Code started the server, stop it from VS Code by opening the MCP server controls and stopping or restarting the `terraform-versions` server.

If you started it manually in a terminal, stop it with:

```bash
Ctrl+C
```

If the server is running as a background process, find and stop it with:

```bash
pgrep -af terraform_versions_mcp
kill <PID>
```

## Add The Server To VS Code

The workspace already contains this MCP configuration:

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

After installing the server dependencies, reload VS Code or restart the MCP server from the MCP controls. The server name is `terraform-versions`.

## Use The MCP Server In VS Code

In Copilot Chat, ask for one of the exposed version lookups. Example prompts:

```text
Use the terraform-versions MCP server to get the latest Terraform GitHub provider version.
```

```text
Use the terraform-versions MCP server to get the latest Terraform CLI version.
```

```text
Use the terraform-versions MCP server to return both the latest Terraform CLI and integrations/github provider versions.
```

Example structured response from `get_latest_terraform_versions`:

```json
{
	"github_provider": {
		"name": "github",
		"namespace": "integrations",
		"version": "6.12.1",
		"tag": "v6.12.1",
		"source": "https://github.com/integrations/terraform-provider-github",
		"registry_url": "https://registry.terraform.io/v1/providers/integrations/github",
		"docs_url": "https://registry.terraform.io/providers/integrations/github/latest/docs",
		"published_at": "2026-04-28T15:42:00Z"
	},
	"terraform_cli": {
		"version": "1.15.6",
		"tag": "v1.15.6",
		"release_url": "https://github.com/hashicorp/terraform/releases/tag/v1.15.6",
		"published_at": "2026-06-10T11:52:20Z"
	}
}
```

The exact versions change as new releases are published.

## Debug And Inspect

You can inspect the server with the MCP Inspector if Node.js and npm are installed:

```bash
cd mcp-server
. .venv/bin/activate
npx -y @modelcontextprotocol/inspector python -m terraform_versions_mcp.server
```

You can also run the MCP SDK development command:

```bash
cd mcp-server
. .venv/bin/activate
mcp dev src/terraform_versions_mcp/server.py
```

## Terraform Examples

The Terraform example for creating a GitHub repository is in `examples/repository/`.

