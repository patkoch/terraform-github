resource "github_repository" "repo" {
  name         = var.repository_name
  description  = var.description
  visibility   = var.visibility
  has_issues   = var.has_issues
  has_wiki     = var.has_wiki
  has_projects = var.has_projects
  auto_init    = var.auto_init
}
