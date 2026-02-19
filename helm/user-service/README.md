# user-service Helm Chart

This chart deploys the User Service microservice (FastAPI).

Quick production-friendly install notes

- If you prefer CI-side secret injection instead of in-cluster Job, I can add a small script and `values-kong.yaml` example.

Custom Kong plugin

This chart references a custom Kong plugin named `custom` (injects `X-Custom-Trace`).
Kong must have the plugin present in its runtime for the `KongPlugin` resource to work.

To build a Kong image with the plugin included, see `kong/README.md` and build the
image from the `kong/` folder in this repository. Then deploy Kong using that image
or configure your Kong installation to load the plugin directory.
# user-service Helm Chart

This chart deploys the User Service microservice (FastAPI).

Quick production-friendly install notes

- Provide secrets from a secure source (HashiCorp Vault, SealedSecrets, or CI):

  ```bash
  # Create a Kubernetes secret with your strong secret key
  kubectl create secret generic user-service-secret --from-literal=SECRET_KEY="$SECRET_KEY" -n user-service

  # Install the chart (namespace will be created by the chart)
  helm install user-service ./user-service --namespace user-service
  ```

- To pass the secret via helm (less recommended):

  ```bash
  helm install user-service ./user-service \
    --set secrets.enabled=true \
    --set secrets.secretKey="$SECRET_KEY" \
    --namespace user-service
  ```

- Recommended values to override in production:
  - `image.tag`: use immutable tags (not `latest`)
  - `image.pullPolicy`: `Always`
  - `replicaCount`: set according to load / HPA
  - `persistence.enabled`: `true` and set `storageClass`

Validation

```bash
helm template user-service ./user-service
```

If you want, I can add a `values-production.yaml` example and a `helmfile`/CI snippet for secure secret injection.
