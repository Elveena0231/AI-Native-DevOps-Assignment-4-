variable "cluster_name" {
  description = "Name of the Kubernetes cluster (for labeling)."
  type        = string
  default     = "local-cluster"
}

variable "kubeconfig_path" {
  description = "Path to kubeconfig file. If empty, provider will use environment defaults (KUBECONFIG)."
  type        = string
  default     = ""
}

variable "namespace" {
  description = "Namespace to create for the API platform."
  type        = string
  default     = "api-platform"
}

variable "kong_namespace" {
  description = "Namespace to create for Kong."
  type        = string
  default     = "kong"
}

variable "allowed_cidrs" {
  description = "List of CIDR ranges allowed to access protected endpoints (used for IP whitelisting)."
  type        = list(string)
  default     = []
}

variable "user_service_port" {
  description = "Port for the user-service (used in NetworkPolicy)."
  type        = number
  default     = 8000
}

variable "kong_proxy_port" {
  description = "Kong proxy port (used in Kong NetworkPolicy)."
  type        = number
  default     = 8000
}
