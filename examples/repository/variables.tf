variable "github_owner" {
  description = "GitHub owner (user or organization) where the repo will be created."
  type        = string
}

variable "repository_name" {
  description = "Name of the repository to create."
  type        = string
}

variable "description" {
  description = "Repository description"
  type        = string
  default     = ""
}

variable "visibility" {
  description = "Repository visibility: public, private or internal (for orgs)."
  type        = string
  default     = "private"
}

variable "has_issues" {
  type    = bool
  default = true
}

variable "has_wiki" {
  type    = bool
  default = false
}

variable "has_projects" {
  type    = bool
  default = false
}

variable "auto_init" {
  description = "If true, initializes the repository with an empty README."
  type        = bool
  default     = false
}