# examples\repository

This Terraform example automates creation and basic configuration of a GitHub repository using the Terraform GitHub provider. It defines the repository resource, exposes inputs for name/description/visibility and repo features (issues, wiki, projects), and uses a provider configuration that reads authentication from the environment so infrastructure can be applied non-interactively.

 * Goal: Create a GitHub repository (github_repository.repo) with configurable metadata and initialization options.
 * Provider & Auth: Uses the github provider; authentication is supplied via the GITHUB_TOKEN environment variable (so the token is not stored in plaintext). The repo owner is provided via github_owner variable.
 * Token variable: You do not need to set a Terraform variable named github_token. The GitHub provider reads GITHUB_TOKEN out of the box when the token argument is not set explicitly in providers.tf.
 * Inputs: Configurable through variables.tf and terraform.tfvars (examples live in terraform.tfvars), including repository_name, description, visibility, auto_init, has_issues, has_wiki, and has_projects.
 * Files of interest: terraform.tf (required_providers / Terraform version), providers.tf (provider configuration), main.tf (resource declaration), and terraform.tfvars (example values).
 * Remote state: GitHub Actions writes a temporary backend.generated.tf file and stores Terraform state in Azure Blob Storage account stdemodevsdc001, container tfstate, resource group azureworkshop-demo-rg. Local runs use local state by default.
 * Typical workflow: set the environment variable, run terraform init, then terraform plan and terraform apply to create the repository.
 * Caveat: Keep only one non-aliased provider and one required_providers block in the module root to avoid duplicate-configuration errors.

# Deploy a new GitHub repository using Terraform

## Prepare the parametrization files

 * Rename "examples/repository/terraform.tfvars.example" to "examples/repository/terraform.tfvars"
 * Set your GitHub owner inb line 2 of the terraform.tfvars file
 * Set the name of the GitHub repository to be created in line 5

## Create authentication

For GitHub Actions, the workflow in ../../.github/workflows/deploy-github-repository.yml creates a short-lived GitHub App installation token and passes it to Terraform as GITHUB_TOKEN.

For local runs, create a proper Personal Access Token or another GitHub token with the required permissions.
You do not need to set TF_VAR_github_token locally; export GITHUB_TOKEN and the provider will pick it up automatically.

Click on your profile in the right upper corner and choose "Settings"

<p align="left">
  <img src="pictures/gh-pk-settings.png" width="30%" height="30%" title="gh-pk-settings">
</p>

Click on "Developer Settings"

<p align="left">
  <img src="pictures/gh-pk-dev-settings.png" width="30%" height="30%" title="gh-pk-dev-settings">
</p>

Choose the following scopes for your PAT:

<p align="left">
  <img src="pictures/gh-pk-pat-scope-1.png" width="80%" height="80%" title="gh-pk-pat-scope-1">
</p>

<p align="left">
  <img src="pictures/gh-pk-pat-scope-2.png" width="70%" height="70%" title="gh-pk-pat-scope-2">
</p>

Create the PAT and copy the value of it.

## Set the environment variable

Set the value of the previously created value by starting a new bash prompt and set it like:

```bash
export GITHUB_TOKEN="your_token_here"
```


## Initialize the working direcotory

Local runs use Terraform's local backend by default. You do not need Azure backend access unless you intentionally create a backend.generated.tf file or run through GitHub Actions.

For GitHub Actions or intentional remote-backend runs, sign in to Azure first with an account that can access the storage account:

```bash
az login
az account set --subscription ff676f41-96fb-4d4e-80a8-e8a7d6ccd42e
export ARM_USE_AZUREAD=true
```

```bash
terraform init
```

If this directory was previously initialized with the Azure backend, reconfigure it once after pulling the local-backend setup:

```bash
terraform init -reconfigure
```

If remote-backend initialization fails with `AuthorizationPermissionMismatch` while listing blobs, the signed-in Azure identity can access the storage account management plane but does not have Blob data-plane permissions. Assign `Storage Blob Data Contributor` on the storage account or the `tfstate` container to the user or service principal that runs Terraform.

## Validate it

```bash
terraform validate
```

## Create an execution plan

```bash
terraform plan -out tfplan
```

## Apply using the created plan

```bash
terraform apply tfplan
```
The repository should be created.

# Destroy the GitHub repository

```bash
terraform destroy
```

Verify the logs and confirm it with "yes"