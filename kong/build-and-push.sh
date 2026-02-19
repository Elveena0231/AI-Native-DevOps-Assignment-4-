#!/usr/bin/env bash
set -euo pipefail

# Build and optionally push a Kong image that includes the custom plugin.
# Usage:
#  DOCKER_IMAGE=your-registry.example.com/kong-custom:latest ./build-and-push.sh [push]

IMAGE=${DOCKER_IMAGE:-kong-custom:latest}

echo "Building image $IMAGE"
docker build -t "$IMAGE" .

if [[ ${1:-} == "push" ]]; then
  echo "Pushing $IMAGE"
  docker push "$IMAGE"
fi

echo "Done"
