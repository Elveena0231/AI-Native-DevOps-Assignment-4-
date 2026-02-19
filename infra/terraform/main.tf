terraform {
  required_version = ">= 1.4.0"
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 2.11.0"
    }
  }
}

provider "kubernetes" {}

resource "kubernetes_namespace" "api_platform" {
  metadata {
    name = var.namespace
    labels = {
      cluster = var.cluster_name
    }
  }
}

resource "kubernetes_namespace" "kong" {
  metadata {
    name = var.kong_namespace
    labels = {
      cluster = var.cluster_name
    }
  }
}

# NetworkPolicy for user-service: allow ingress only from configured CIDR ranges
resource "kubernetes_network_policy" "user_service_ingress" {
  metadata {
    name      = "user-service-allow-cidrs"
    namespace = kubernetes_namespace.api_platform.metadata[0].name
  }

  spec {
    pod_selector {}

    ingress {
      dynamic "from" {
        for_each = var.allowed_cidrs
        content {
          ip_block {
            cidr = from.value
          }
        }
      }

      ports {
        port     = var.user_service_port
        protocol = "TCP"
      }
    }

    policy_types = ["Ingress"]
  }
}

# NetworkPolicy for Kong (edge): allow ingress only from configured CIDRs (optional)
resource "kubernetes_network_policy" "kong_ingress" {
  metadata {
    name      = "kong-allow-cidrs"
    namespace = kubernetes_namespace.kong.metadata[0].name
  }

  spec {
    pod_selector {}

    ingress {
      dynamic "from" {
        for_each = var.allowed_cidrs
        content {
          ip_block {
            cidr = from.value
          }
        }
      }

      ports {
        port     = var.kong_proxy_port
        protocol = "TCP"
      }
    }

    policy_types = ["Ingress"]
  }
}
