from __future__ import annotations

import json
from typing import Any, TypedDict
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from mcp.server.fastmcp import FastMCP


TERRAFORM_PROVIDER_URL = "https://registry.terraform.io/v1/providers/integrations/github"
TERRAFORM_CLI_URL = "https://api.github.com/repos/hashicorp/terraform/releases/latest"
USER_AGENT = "terraform-versions-mcp/0.1.0"


class GitHubProviderVersion(TypedDict):
    name: str
    namespace: str
    version: str
    tag: str
    source: str
    registry_url: str
    docs_url: str
    published_at: str | None


class TerraformCliVersion(TypedDict):
    version: str
    tag: str
    release_url: str
    published_at: str | None


class TerraformVersions(TypedDict):
    github_provider: GitHubProviderVersion
    terraform_cli: TerraformCliVersion


mcp = FastMCP(
    "Terraform Versions",
    instructions=(
        "Use this server to look up the latest Terraform CLI release and the "
        "latest integrations/github Terraform provider version."
    ),
)


def fetch_json(url: str) -> dict[str, Any]:
    request = Request(url, headers={"Accept": "application/json", "User-Agent": USER_AGENT})

    try:
        with urlopen(request, timeout=20) as response:
            payload = response.read().decode("utf-8")
    except HTTPError as error:
        raise RuntimeError(f"Request to {url} failed with HTTP {error.code}: {error.reason}") from error
    except URLError as error:
        raise RuntimeError(f"Request to {url} failed: {error.reason}") from error
    except TimeoutError as error:
        raise RuntimeError(f"Request to {url} timed out") from error

    try:
        data = json.loads(payload)
    except json.JSONDecodeError as error:
        raise RuntimeError(f"Request to {url} did not return valid JSON") from error

    if not isinstance(data, dict):
        raise RuntimeError(f"Request to {url} returned an unexpected JSON payload")

    return data


@mcp.tool()
def get_latest_github_provider_version() -> GitHubProviderVersion:
    """Return the latest integrations/github Terraform provider version from the Terraform Registry."""
    data = fetch_json(TERRAFORM_PROVIDER_URL)
    version = str(data.get("version") or "")

    if not version:
        raise RuntimeError("Terraform Registry response did not contain a provider version")

    tag = str(data.get("tag") or f"v{version}")

    return {
        "name": str(data.get("name") or "github"),
        "namespace": str(data.get("namespace") or "integrations"),
        "version": version,
        "tag": tag,
        "source": str(data.get("source") or "https://github.com/integrations/terraform-provider-github"),
        "registry_url": TERRAFORM_PROVIDER_URL,
        "docs_url": "https://registry.terraform.io/providers/integrations/github/latest/docs",
        "published_at": data.get("published_at") if isinstance(data.get("published_at"), str) else None,
    }


@mcp.tool()
def get_latest_terraform_cli_version() -> TerraformCliVersion:
    """Return the latest Terraform CLI version from HashiCorp's GitHub releases."""
    data = fetch_json(TERRAFORM_CLI_URL)
    tag = str(data.get("tag_name") or "")

    if not tag:
        raise RuntimeError("GitHub release response did not contain tag_name")

    return {
        "version": tag.removeprefix("v"),
        "tag": tag,
        "release_url": str(data.get("html_url") or "https://github.com/hashicorp/terraform/releases/latest"),
        "published_at": data.get("published_at") if isinstance(data.get("published_at"), str) else None,
    }


@mcp.tool()
def get_latest_terraform_versions() -> TerraformVersions:
    """Return both the latest Terraform GitHub provider version and Terraform CLI version."""
    return {
        "github_provider": get_latest_github_provider_version(),
        "terraform_cli": get_latest_terraform_cli_version(),
    }


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()