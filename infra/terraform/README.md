Terraform module: Kubernetes base infra for API platform and Kong

This folder contains a minimal Terraform configuration which provisions:
- Kubernetes namespaces: `api-platform` (default) and `kong` (default)
- NetworkPolicies restricting ingress to specified CIDR ranges for both the
  `api-platform` pods and Kong pods.

Usage

1. Ensure Terraform is installed (>= 1.4) and you have access to the target
   Kubernetes cluster (set `KUBECONFIG` or provide `kubeconfig_path` variable).

2. Initialize and plan:

```bash
cd infra/terraform
terraform init
terraform plan -var='allowed_cidrs=["198.51.100.0/24","203.0.113.0/24"]'
```

3. Apply:

```bash
terraform apply -var='allowed_cidrs=["198.51.100.0/24","203.0.113.0/24"]' -auto-approve
```

Notes
- The `kubernetes` provider will use the environment `KUBECONFIG` if you do
  not set `kubeconfig_path` explicitly.
- The NetworkPolicy resources created will allow ingress only from the CIDRs
  listed in `allowed_cidrs`. If `allowed_cidrs` is empty, the policies will be
  created with no `from` entries (resulting in an ingress rule that only opens
  the specified ports but does not permit any IPs) — in effect blocking ingress.
- Customize `user_service_port` and `kong_proxy_port` as needed.
