# Building a Kong image with the custom plugin

This folder contains a Dockerfile and plugin sources to produce a Kong image
that includes the `custom` plugin which injects `X-Custom-Trace` response headers.

Steps:

1. Build the image locally:

```bash
DOCKER_IMAGE=your-registry.example.com/kong-custom:1.0.0 ./build-and-push.sh
```

2. To push to a registry:

```bash
DOCKER_IMAGE=your-registry.example.com/kong-custom:1.0.0 ./build-and-push.sh push
```

3. Deploy Kong using this image (example with Kubernetes Deployment override):

 - Edit your Kong Deployment to use the built image.
 - Ensure the Kong environment includes `KONG_PLUGINS=bundled,custom` (the Dockerfile sets this).

Notes:

- The plugin source is in `plugins/custom/` and provides `handler.lua` and a minimal
  `schema.lua`.
- Do not store production secrets or credentials in this repository.
