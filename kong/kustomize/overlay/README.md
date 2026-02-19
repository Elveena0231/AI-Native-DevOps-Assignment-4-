Kustomize overlay to switch Kong to a custom image that includes the `custom` plugin.

Usage:

1. Edit `kustomization.yaml` to set `images.newName` and `newTag` or replace the
   placeholders in `deployment_patch.yaml`.

2. Apply the overlay against your cluster where Kong is deployed (the overlay
   assumes `namespace: kong` and `deployment name: kong` with container `proxy`).

```bash
# Example (after editing placeholders):
kustomize build . | kubectl apply -f -
```

If your Kong deployment has a different name or container, use the helper script
`../apply-kong-custom-image.sh` instead.
