output "namespace_api_platform" {
  description = "Name of the created API platform namespace."
  value       = kubernetes_namespace.api_platform.metadata[0].name
}

output "namespace_kong" {
  description = "Name of the created Kong namespace."
  value       = kubernetes_namespace.kong.metadata[0].name
}
