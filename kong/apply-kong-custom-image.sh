#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 4 ]; then
  echo "Usage: $0 <deployment> <namespace> <container_name> <image:tag>"
  exit 2
fi

DEPLOYMENT=$1
NAMESPACE=$2
CONTAINER=$3
IMAGE=$4

echo "Setting image for deployment/$DEPLOYMENT (container: $CONTAINER) to $IMAGE in namespace $NAMESPACE"
kubectl -n "$NAMESPACE" set image deployment/"$DEPLOYMENT" "$CONTAINER"="$IMAGE"
echo "Ensuring KONG_PLUGINS includes custom"
kubectl -n "$NAMESPACE" set env deployment/"$DEPLOYMENT" KONG_PLUGINS="bundled,custom"

echo "Done"
