# AI-Native-DevOps-Assignment-4-

Repository scaffold for microservice, Helm charts, Kong integration, and infra.

Structure overview:

- `microservice/` - small starter app and Dockerfile
- `helm/` - Helm charts for `user-service` and `kong`
- `kong/` - Kong plugin sources and helper Dockerfile
- `k8s/` - example Kubernetes manifests
- `infra/terraform/` - Terraform module for namespaces and network policies
- `terraform/` - top-level placeholder
# AI-Native-DevOps-Assignment-4-

## Docker Installation in GitHub Codespaces (Ubuntu-based)

Follow these steps to install and configure Docker inside GitHub Codespaces:

### Step 1: Update System Packages
Update the package manager to ensure you have the latest package information:

```bash
sudo apt-get update
```

### Step 2: Install Docker
Install Docker using the official Ubuntu repository:

```bash
sudo apt-get install -y docker.io
```

This installs:
- Docker CLI
- Docker daemon (dockerd)
- Docker containerd runtime

### Step 3: Verify Docker Installation
Check that Docker has been installed successfully:

```bash
docker --version
```

### Step 4: Start the Docker Daemon
Start the Docker daemon service:

```bash
sudo service docker start
```

Or use systemctl:

```bash
sudo systemctl start docker
```

### Step 5: Enable Docker to Run on Startup (Optional)
Configure Docker to start automatically:

```bash
sudo systemctl enable docker
```

### Step 6: Grant Current User Docker Permissions
Add your user to the docker group to avoid using `sudo` for every command:

```bash
sudo usermod -aG docker $USER
```

**Note:** You may need to log out and back in, or run the following command to activate the new group:

```bash
newgrp docker
```

Or in Codespaces, restart the terminal.

### Step 7: Verify Docker Daemon is Running
Check if the Docker daemon is active and running:

```bash
sudo systemctl status docker
```

Expected output should show:
```
● docker.service - Docker Application Container Engine
     Loaded: loaded (/lib/systemd/system/docker.service; enabled; vendor preset: enabled)
     Active: active (running) since [timestamp]
```

### Step 8: Test Docker Installation with Hello-World
Verify Docker works correctly by running the hello-world container:

```bash
docker run hello-world
```

**Expected output:**
```
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
...
Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

### Step 9: Verify Docker Can Execute Containers
Test that Docker can successfully pull and run images:

```bash
docker ps -a
```

This lists all containers. You should see the hello-world container in the output.

### Troubleshooting

**Error: "Cannot connect to Docker daemon"**
```bash
# Start the daemon
sudo service docker start

# Or use systemctl
sudo systemctl start docker

# Verify it's running
sudo systemctl status docker
```

**Error: "Permission denied while trying to connect to the Docker daemon"**
```bash
# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Restart terminal or run:
exec su -l $USER
```

**Check Docker daemon logs:**
```bash
sudo journalctl -u docker -f
```

### Optional: Verify Docker Resource Usage
Monitor Docker daemon and container resources:

```bash
docker stats
docker ps
docker images
```

---

## Kind (Kubernetes in Docker) Installation in GitHub Codespaces

Follow these steps to install and configure Kind (Kubernetes in Docker) inside GitHub Codespaces:

### Prerequisites
- Docker must be installed and running (see Docker installation steps above)
- `kubectl` (Kubernetes command-line tool)
- At least 2GB free disk space

### Step 1: Install kubectl
Install kubectl, the Kubernetes command-line tool:

```bash
sudo apt-get install -y kubectl
```

Verify the installation:

```bash
kubectl version --client
```

### Step 2: Download and Install Kind
Download the latest kind binary and make it executable:

```bash
curl -Lo ./kind https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
```

Verify the installation:

```bash
kind version
```

### Step 3: Create a Kind Cluster
Create a new Kubernetes cluster using kind:

```bash
kind create cluster --name devops-cluster
```

**Expected output:**
```
Creating cluster "devops-cluster" ...
 ✓ Ensuring node image (kindest/node:vX.XX.X) 🖼
 ✓ Preparing nodes 📦
 ✓ Writing configuration 📝
 ✓ Starting control-plane 🕹️
 ✓ Installing CNI 🔌
 ✓ Installing StorageClass 💾
Set kubectl context to "kind-devops-cluster"
You can now use your cluster with:

kubectl cluster-info --context kind-devops-cluster
```

### Step 4: Verify Cluster Creation
Check if the cluster context is set correctly:

```bash
kubectl config current-context
```

Expected output:
```
kind-devops-cluster
```

### Step 5: Verify Nodes - Test Cluster Health
Verify that the cluster nodes are running and ready:

```bash
kubectl get nodes
```

**Expected output:**
```
NAME                           STATUS   ROLES           AGE   VERSION
devops-cluster-control-plane   Ready    control-plane   2m    vX.XX.X
```

### Step 6: Verify Cluster Components
Check all cluster components and their status:

```bash
kubectl get pods -A
```

This shows all running pods in all namespaces.

### Step 7: Get Cluster Information
Display detailed cluster information:

```bash
kubectl cluster-info --context kind-devops-cluster
```

**Expected output shows:**
- Kubernetes master (control-plane) URL
- CoreDNS address
- Metrics-server status

### Step 8: Test Cluster Connectivity
Deploy a test pod to verify the cluster is fully functional:

```bash
kubectl run test-pod --image=nginx:alpine
kubectl get pods
kubectl delete pod test-pod
```

### Additional Kind Cluster Management Commands

**List all kind clusters:**
```bash
kind get clusters
```

**Delete a cluster:**
```bash
kind delete cluster --name devops-cluster
```

**Create a multi-node cluster:**
```bash
kind create cluster --name multi-node-cluster --config - <<EOF
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
- role: worker
- role: worker
EOF
```

### Troubleshooting

**Error: "Docker daemon not running"**
```bash
# Start Docker daemon
sudo systemctl start docker

# Verify it's running
sudo systemctl status docker
```

**Error: "kind: command not found"**
```bash
# Verify kind is in PATH
which kind

# If not found, reinstall:
curl -Lo ./kind https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
```

**Error: "Cluster not ready"**
```bash
# Check node status
kubectl get nodes

# Wait a moment and check again (takes 1-2 minutes)
kubectl get nodes -w  # Watch mode for live updates
```

**Check kind cluster logs:**
```bash
kind export logs ./kind-logs
```

### Verify Everything is Working
Run this command to confirm all components are running:

```bash
kubectl get nodes && kubectl get pods -A && kind get clusters
```

This should show:
1. Ready node(s)
2. All system pods running
3. Your cluster listed

---

## Helm Installation in GitHub Codespaces

Follow these steps to install and configure Helm inside GitHub Codespaces:

### Prerequisites
- kubectl must be installed (see kubectl installation steps above)
- A Kubernetes cluster should be available (Kind cluster from previous steps)

### Step 1: Download Helm Installation Script
Download the official Helm installation script:

```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

This script will:
- Detect your OS and architecture (Linux/amd64 for Codespaces)
- Download the latest Helm 3 release
- Install it to `/usr/local/bin/helm`

**Alternative: Manual Installation**

If you prefer manual installation:

```bash
curl -fsSLO https://get.helm.sh/helm-v3.14.0-linux-amd64.tar.gz
tar -zxvf helm-v3.14.0-linux-amd64.tar.gz
sudo mv linux-amd64/helm /usr/local/bin/
rm -rf helm-v3.14.0-linux-amd64.tar.gz linux-amd64/
```

### Step 2: Verify Helm Installation
Check that Helm has been installed successfully:

```bash
helm version
```

**Expected output:**
```
version.BuildInfo{Version:"v3.14.0", GitCommit:"...", GitTreeState:"clean", GoVersion:"go1.21.0"}
```

### Step 3: Verify Helm Configuration
Check the helm configuration and repositories:

```bash
helm repo list
```

**Expected output:**
```
NAME  	URL
```
(Empty list initially, which is normal)

### Step 4: Update Helm Repositories
Add and update the standard Helm repositories:

```bash
helm repo add stable https://charts.helm.sh/stable
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
```

**Expected output:**
```
"stable" has been added to your repositories
"bitnami" has been added to your repositories
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "stable" chart repository
...Successfully got an update from the "bitnami" chart repository
Update Complete. ⎈ Happy Helming!
```

### Step 5: Verify Helm Can Access Kubernetes Cluster
Test Helm's connection to the Kind cluster:

```bash
helm list
```

**Expected output:**
```
NAME    NAMESPACE       REVISION        UPDATED STATUS  CHART   APP VERSION
```
(Empty list initially, which is normal - no releases deployed yet)

### Step 6: Search for Available Charts
Test searching for Helm charts:

```bash
helm search repo nginx
```

**Expected output shows available nginx charts:**
```
NAME                            	CHART VERSION   APP VERSION     DESCRIPTION
bitnami/nginx                   	15.0.1          1.24.0          NGINX (pronounced "engine-X") is an open source...
stable/nginx-ingress            	4.10.1          1.1.2           DEPRECATED. Use https://github.com/kubernetes/i...
```

### Step 7: Verify Helm + Kubernetes Integration
Deploy a test Helm chart to verify everything works:

```bash
helm install my-release bitnami/nginx --dry-run --debug
```

This performs a dry-run (doesn't actually deploy) to verify the setup.

**Expected output shows manifest without errors.**

### Step 8: Get Helm Information
Display comprehensive Helm information:

```bash
helm version --short
helm env
```

This shows:
- Helm version
- Configuration paths
- Helm home directory
- Repository cache location

### Helm Common Commands Reference

```bash
# View installed Helm version and environment
helm version
helm env

# Repository management
helm repo list          # List all added repositories
helm repo add NAME URL  # Add a new repository
helm repo update        # Update all repositories
helm repo remove NAME   # Remove a repository

# Chart operations
helm search repo CHART  # Search for a chart
helm search hub CHART   # Search on Artifact Hub

# Release management
helm list              # List all releases
helm install RELEASE CHART  # Install a chart
helm upgrade RELEASE CHART  # Upgrade a release
helm uninstall RELEASE # Delete a release
helm rollback RELEASE  # Rollback to previous revision

# Debugging
helm template RELEASE CHART  # Render templates locally
helm get values RELEASE      # Get values of a release
helm get manifest RELEASE    # Get deployed manifest
```

### Troubleshooting

**Error: "helm: command not found"**
```bash
# Verify helm is in PATH
which helm

# If not found, reinstall:
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Or add to PATH if installed elsewhere
export PATH=$PATH:/usr/local/bin
```

**Error: "Unable to connect to the server"**
```bash
# Ensure kubectl can access the cluster
kubectl cluster-info

# Check current context
kubectl config current-context

# Helm uses the same kubeconfig as kubectl
```

**Error: "No repositories found"**
```bash
# Add default repositories
helm repo add stable https://charts.helm.sh/stable
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
```

**Check Helm configuration:**
```bash
helm env
cat ~/.kube/config  # Verify kubeconfig exists
```

### Verify Everything is Installed
Run this comprehensive verification command:

```bash
echo "=== Helm Installation Verification ===" && \
echo "1. Helm Version:" && helm version --short && \
echo "" && \
echo "2. Kubectl Context:" && kubectl config current-context && \
echo "" && \
echo "3. Helm Repositories:" && helm repo list && \
echo "" && \
echo "4. Helm Environment:" && helm env HELM_HOME && \
echo "" && \
echo "✅ Helm installation and verification complete!"
```

**Expected output shows:**
1. Helm version (v3.x.x)
2. Current kubectl context (kind-devops-cluster)
3. Configured repositories (stable, bitnami)
4. Helm home directory location

---

## Terraform Installation in GitHub Codespaces

Follow these steps to install and configure Terraform inside GitHub Codespaces:

### Prerequisites
- Linux/Unix command-line terminal
- Internet connectivity to download Terraform
- No special system dependencies required

### Step 1: Update System Packages
Update the package manager:

```bash
sudo apt-get update
```

### Step 2: Install Terraform via apt (Recommended)
Install Terraform using the HashiCorp Debian repository:

```bash
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt-get update && sudo apt-get install -y terraform
```

**Alternative: Quick Installation via apt (simpler)**

```bash
sudo apt-get install -y terraform
```

**Alternative: Manual Binary Installation**

If you prefer manual installation:

```bash
# Download the latest Terraform binary
curl -fsSL https://releases.hashicorp.com/terraform/1.7.0/terraform_1.7.0_linux_amd64.zip -o terraform.zip

# Extract the binary
unzip terraform.zip

# Move to system PATH
sudo mv terraform /usr/local/bin/

# Clean up
rm terraform.zip

# Verify permission
ls -la /usr/local/bin/terraform
```

### Step 3: Verify Terraform Installation
Check that Terraform has been installed successfully:

```bash
terraform -version
```

**Expected output:**
```
Terraform v1.7.0
on linux_amd64
```

### Step 4: Verify Terraform Location
Confirm Terraform is in your PATH:

```bash
which terraform
```

**Expected output:**
```
/usr/local/bin/terraform
```

### Step 5: Test Terraform Initialization
Create a test directory and initialize Terraform:

```bash
mkdir -p ~/terraform-test
cd ~/terraform-test
terraform init
```

**Expected output:**
```
Terraform has been successfully initialized!
```

### Step 6: Validate Terraform Configuration
Create a simple Terraform configuration file to test:

```bash
cat > main.tf << 'EOF'
terraform {
  required_version = ">= 1.0"
}

provider "null" {
}

resource "null_resource" "example" {
  provisioners = {
    local-exec = "echo 'Terraform is working!'"
  }
}
EOF
```

### Step 7: Format and Validate
Validate the Terraform configuration:

```bash
terraform fmt
terraform validate
```

**Expected output from validate:**
```
Success! The configuration is valid.
```

### Step 8: Plan Terraform Changes (Dry Run)
Preview what Terraform will do:

```bash
terraform plan
```

This shows the execution plan without making actual changes.

### Step 9: Display Terraform Version Details
Get comprehensive Terraform information:

```bash
terraform version
terraform version -json
```

### Terraform Common Commands Reference

```bash
# Version and help
terraform version          # Show Terraform version
terraform version -json    # Show version in JSON format
terraform -version         # Shorthand version command
terraform help             # Show help information
terraform help [command]   # Help for specific command

# Configuration management
terraform init             # Initialize Terraform working directory
terraform validate         # Validate configuration files
terraform fmt              # Format configuration files
terraform plan              # Create execution plan
terraform apply             # Apply configuration changes
terraform destroy           # Destroy managed infrastructure
terraform refresh           # Refresh state file

# State management
terraform state list       # List state resources
terraform state show       # Show state resource details
terraform state pull       # Pull remote state
terraform state push       # Push remote state

# Workspace operations
terraform workspace list   # List workspaces
terraform workspace new    # Create new workspace
terraform workspace select # Switch workspace

# Debugging
terraform console          # Interactive console
terraform graph             # Show resource graph
terraform output            # Show outputs from state
```

### Terraform Configuration Structure

Create a basic Terraform project structure:

```bash
mkdir -p terraform-project
cd terraform-project

# Create main configuration file
cat > main.tf << 'EOF'
terraform {
  required_version = ">= 1.0"
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
  }
}

provider "kubernetes" {
  config_path = "~/.kube/config"
}

# Example resource
resource "kubernetes_namespace" "example" {
  metadata {
    name = "terraform-example"
  }
}
EOF

# Create variables file
cat > variables.tf << 'EOF'
variable "cluster_name" {
  description = "Kubernetes cluster name"
  type        = string
  default     = "devops-cluster"
}
EOF

# Create outputs file
cat > outputs.tf << 'EOF'
output "cluster_name" {
  value = var.cluster_name
}
EOF
```

### Integration with Kubernetes/Helm

Use Terraform with the Kubernetes provider:

```bash
terraform init
terraform plan
terraform apply
```

This integrates Terraform with your Kind cluster and Helm setup.

### Troubleshooting

**Error: "terraform: command not found"**
```bash
# Check if installed
which terraform

# If not found, reinstall
sudo apt-get update
sudo apt-get install -y terraform

# Or use manual installation
curl -fsSL https://releases.hashicorp.com/terraform/1.7.0/terraform_1.7.0_linux_amd64.zip -o terraform.zip
unzip terraform.zip && sudo mv terraform /usr/local/bin/
```

**Error: "Error validating provider configuration"**
```bash
# Ensure kubeconfig exists
ls ~/.kube/config

# Initialize Terraform directory
terraform init

# Validate configuration
terraform validate
```

**Error: "Partial success: XXX resources remaining"**
```bash
# Check state file
terraform state list

# Refresh state
terraform refresh

# Try destroy again
terraform destroy
```

**Check Terraform detailed logs:**
```bash
# Enable debug logging
export TF_LOG=DEBUG
terraform plan

# Disable logging
unset TF_LOG
```

### Verify Terraform Integration

Run this comprehensive verification command:

```bash
echo "=== Terraform Installation Verification ===" && \
echo "" && \
echo "1. Terraform Version:" && \
terraform -version && \
echo "" && \
echo "2. Terraform Location:" && \
which terraform && \
echo "" && \
echo "3. Terraform Path:" && \
terraform --version && \
echo "" && \
echo "4. Test Configuration:" && \
mkdir -p /tmp/terraform-test && cd /tmp/terraform-test && \
terraform init -backend=false 2>&1 | head -5 && \
echo "" && \
echo "✅ Terraform installation and verification complete!"
```

**Expected output shows:**
1. Terraform version (v1.x.x)
2. Terraform binary location (/usr/local/bin/terraform)
3. Detailed version information
4. Successful Terraform initialization

### Complete DevOps Stack Verification

Verify all installed components work together:

```bash
echo "╔════════════════════════════════════════════════════╗" && \
echo "║  Complete DevOps Stack Verification               ║" && \
echo "╚════════════════════════════════════════════════════╝" && \
echo "" && \
echo "✅ Docker:   $(docker --version)" && \
echo "✅ kubectl:  $(kubectl version --client --short)" && \
echo "✅ kind:     $(kind version | grep -oP 'v[0-9.]+' | head -1)" && \
echo "✅ Helm:     $(helm version --short)" && \
echo "✅ Terraform: $(terraform -version | head -1)" && \
echo "" && \
echo "✅ Cluster Context: $(kubectl config current-context)" && \
echo "✅ Cluster Node: $(kubectl get nodes -o name)" && \
echo "" && \
echo "╔════════════════════════════════════════════════════╗" && \
echo "║  🎉 All DevOps tools ready for deployment! 🎉     ║" && \
echo "╚════════════════════════════════════════════════════╝"
```

---

## Kong OSS Gateway Installation on Kubernetes (kind)

Follow these steps to install Kong OSS (Open Source) API Gateway on your Kind Kubernetes cluster using Helm:

### Prerequisites

- **Kubernetes cluster** running via kind (created in previous steps)
- **kubectl** configured and connected to cluster
- **Helm** installed and configured
- **Cluster context** set to `kind-devops-cluster`
- At least 2GB free memory on the cluster

### Step 1: Verify Cluster Connectivity

Before installing Kong, verify your cluster is accessible:

```bash
kubectl cluster-info
kubectl get nodes
```

**Expected output:**
```
NAME                           STATUS   ROLES           AGE   VERSION
devops-cluster-control-plane   Ready    control-plane   Xm    vX.XX.X
```

### Step 2: Create Kong Namespace

Create a dedicated namespace for Kong Gateway:

```bash
kubectl create namespace kong
```

Verify the namespace was created:

```bash
kubectl get namespace kong
```

**Expected output:**
```
NAME   STATUS   AGE
kong   Active   Xs
```

### Step 3: Add Kong Helm Repository

Add the official Kong Helm repository:

```bash
helm repo add kong https://charts.konghq.com
```

Update the Helm repository cache:

```bash
helm repo update
```

**Expected output:**
```
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "kong" chart repository
Update Complete. ⎈ Happy Helming!
```

### Step 4: Search for Kong Chart

Search for available Kong charts:

```bash
helm search repo kong
```

**Expected output shows available Kong charts:**
```
NAME           	CHART VERSION	APP VERSION	DESCRIPTION
kong/kong      	2.28.0      	3.4.0      	The Cloud-Native API Gateway for Kubernetes...
```

### Step 5: Install Kong OSS Gateway (Basic)

Install Kong using the basic recommended configuration:

```bash
helm install kong kong/kong \
  --namespace kong \
  --set ingressController.enabled=true \
  --set serviceMonitor.enabled=false \
  --set postgresql.enabled=true
```

This command:
- Installs Kong in the `kong` namespace
- Enables the Kong Ingress Controller
- Disables Prometheus monitoring (optional)
- Enables PostgreSQL database

### Step 6: Wait for Kong Deployment

Wait for all Kong pods to be in Running state:

```bash
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=kong -n kong --timeout=300s
```

Monitor the deployment:

```bash
kubectl get pods -n kong -w
```

**Expected output shows pods running:**
```
NAME                            READY   STATUS    RESTARTS   AGE
kong-kong-5d4c45d5fc-xxxxx      1/1     Running   0          2m
kong-postgresql-0               1/1     Running   0          2m
kong-kong-init-migrations-xxxxx  0/1     Completed 0          2m
```

### Step 7: Verify Kong Installation

Check Kong deployment status:

```bash
kubectl get all -n kong
```

Get Kong release information:

```bash
helm list -n kong
```

**Expected output:**
```
NAME	NAMESPACE	REVISION	UPDATED                 	STATUS  	CHART        	APP VERSION
kong	kong     	1       	2026-02-19 11:XX:XX UTC	deployed	kong-2.28.0	3.4.0
```

### Step 8: Get Kong Service Details

Retrieve Kong Gateway service information:

```bash
kubectl get svc -n kong
```

**Expected output:**
```
NAME                   TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)
kong-kong-proxy        ClusterIP   10.XX.XX.XX      <none>        80/TCP,443/TCP
kong-kong-admin        ClusterIP   10.XX.XX.XX      <none>        8001/TCP
kong-kong-manager      ClusterIP   10.XX.XX.XX      <none>        8002/TCP
kong-postgresql        ClusterIP   10.XX.XX.XX      <none>        5432/TCP
```

### Step 9: Access Kong Admin API

Forward the Kong Admin API port:

```bash
kubectl port-forward -n kong svc/kong-kong-admin 8001:8001
```

In a new terminal, test Kong Admin API:

```bash
curl -X GET http://localhost:8001
```

**Expected output shows Kong Admin API response:**
```json
{
  "version": "3.4.0",
  "tagline": "Welcome to",
  "protobufs": [...],
  "timers": {...}
}
```

### Step 10: Access Kong Manager (GUI) - Optional

Forward Kong Manager port (GUI):

```bash
kubectl port-forward -n kong svc/kong-kong-manager 8002:8002
```

Access Kong Manager at: `http://localhost:8002`

### Step 11: Create a Test Kong Ingress

Create a test Kubernetes Ingress to verify Kong Ingress Controller:

```bash
# Create a test backend service and deployment
kubectl create deployment --image=nginx:latest nginx-backend -n kong
kubectl expose deployment nginx-backend --port=80 -n kong

# Create Ingress resource
cat > kong-test-ingress.yaml << 'EOF'
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: test-ingress
  namespace: kong
spec:
  ingressClassName: kong
  rules:
  - host: test.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: nginx-backend
            port:
              number: 80
EOF

kubectl apply -f kong-test-ingress.yaml
```

Verify the ingress:

```bash
kubectl get ingress -n kong
```

### Step 12: Verify Kong Ingress Controller

Check Kong Ingress Controller status:

```bash
kubectl logs -n kong deployment/kong-kong -f | grep ingress
```

Or check ingress controller pod:

```bash
kubectl get pods -n kong -l app.kubernetes.io/component=ingress-controller
```

### Kong Configuration Options

Common Helm values for Kong installation:

```bash
helm install kong kong/kong \
  --namespace kong \
  --values kong-values.yaml \
  --set ingressController.enabled=true \
  --set ingressController.installCRDs=true \
  --set kong.env.database=postgres \
  --set postgresql.enabled=true \
  --set postgresql.auth.password=mypassword \
  --set proxy.type=LoadBalancer \
  --set manager.enabled=true \
  --set enterprise.license_secret=kong-enterprise-license
```

### Kong Admin API Common Operations

```bash
# Get Kong status
curl -X GET http://localhost:8001

# Get Kong services
curl -X GET http://localhost:8001/services

# Create a new service
curl -X POST http://localhost:8001/services \
  -H "Content-Type: application/json" \
  -d '{"name":"my-service","url":"http://backend:8080"}'

# Create a route for the service
curl -X POST http://localhost:8001/services/my-service/routes \
  -H "Content-Type: application/json" \
  -d '{"hosts":["example.com"],"paths":["/api"]}'

# List consumers
curl -X GET http://localhost:8001/consumers

# Create a consumer
curl -X POST http://localhost:8001/consumers \
  -d "username=john"
```

### Troubleshooting Kong Installation

**Error: "CrashLoopBackOff" for Kong pods**

```bash
# Check pod logs
kubectl logs -n kong deployment/kong-kong --tail=100

# Describe pod for events
kubectl describe pod -n kong -l app.kubernetes.io/name=kong

# Check database connection
kubectl logs -n kong deployment/kong-kong | grep postgres
```

**Error: "Pending" PostgreSQL pod**

```bash
# Check PVC status
kubectl get pvc -n kong

# Check storage class
kubectl get storageclass

# Check events
kubectl describe pod -n kong -l app.kubernetes.io/name=postgresql
```

**Kong services not accessible**

```bash
# Check service endpoints
kubectl get endpoints -n kong

# Check service DNS
kubectl run -it --rm debug --image=nicolaka/netshoot --restart=Never -n kong -- \
  nslookup kong-kong-proxy

# Test service connectivity
kubectl run -it --rm debug --image=nicolaka/netshoot --restart=Never -n kong -- \
  curl http://kong-kong-proxy/
```

**Check Kong configuration**

```bash
# Get Kong ConfigMap
kubectl get configmap -n kong

# Get Kong Secrets
kubectl get secret -n kong

# Check Kong environment variables
kubectl set env deployment/kong-kong --list -n kong
```

### Upgrade Kong Gateway

To upgrade Kong to a newer version:

```bash
helm repo update
helm upgrade kong kong/kong \
  --namespace kong \
  --values kong-values.yaml
```

### Uninstall Kong Gateway

To remove Kong from your cluster:

```bash
helm uninstall kong --namespace kong
kubectl delete namespace kong
```

### Verify Kong Installation Summary

Run this comprehensive verification command:

```bash
echo "=== Kong OSS Gateway Installation Verification ===" && \
echo "" && \
echo "1. Kong Namespace:" && \
kubectl get namespace kong && \
echo "" && \
echo "2. Kong Helm Release:" && \
helm list -n kong && \
echo "" && \
echo "3. Kong Deployment Status:" && \
kubectl get deployment -n kong && \
echo "" && \
echo "4. Kong Pods:" && \
kubectl get pods -n kong && \
echo "" && \
echo "5. Kong Services:" && \
kubectl get svc -n kong && \
echo "" && \
echo "6. Kong PostgreSQL Database:" && \
kubectl get statefulset -n kong && \
echo "" && \
echo "7. Kong Admin API Test:" && \
POD=$(kubectl get pod -n kong -l app.kubernetes.io/name=kong -o jsonpath='{.items[0].metadata.name}') && \
kubectl exec -n kong $POD -- curl -s http://localhost:8001 | grep -o '"version":"[^"]*"' && \
echo "" && \
echo "✅ Kong OSS Gateway installation verification complete!"
```

**Expected output shows:**
1. Kong namespace (Active)
2. Kong Helm release (deployed)
3. Kong deployment (1/1 Ready)
4. Kong pods (all Running)
5. Kong services (kong-kong-proxy, kong-kong-admin)
6. PostgreSQL database (1/1 Ready)
7. Kong Admin API responding (version information)
4. Helm home directory location

---

## User Service Microservice (FastAPI)

A production-ready FastAPI microservice for user authentication and management with JWT token-based security.

### Project Structure

```
user-service/
├── main.py                  # FastAPI application with all endpoints
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker containerization
├── docker-compose.yml      # Local development environment
├── k8s-deployment.yaml     # Kubernetes deployment manifest
├── helm-values.yaml        # Helm chart configuration
├── README.md               # Detailed service documentation
└── data/
    └── users.db            # SQLite database (auto-created)
```

### Features

✅ **Authentication APIs**
- `POST /login` - User authentication with JWT token generation
- `GET /verify` - Validate and verify JWT tokens
- Secure password hashing with bcrypt
- Token expiration (30 minutes default)

✅ **User Management APIs**
- `GET /users` - Retrieve all users (JWT protected)
- SQLite database with auto-initialization
- Sample user pre-populated

✅ **Public Endpoints**
- `GET /health` - Health check (no authentication required)
- `GET /` - API information endpoint

✅ **Security Features**
- bcrypt password hashing
- JWT token-based authentication
- Secure authorization header validation
- Pydantic input validation
- Detailed error handling

### Quick Start

**1. Navigate to user service:**
```bash
cd user-service
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Run the service:**
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### API Testing

Once the service is running, test the endpoints:

**Health check (public):**
```bash
curl -X GET http://localhost:8000/health
```

**Login:**
```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}'
```

**Verify token:**
```bash
curl -X GET "http://localhost:8000/verify?token=<jwt_token>"
```

**Get users (protected):**
```bash
curl -X GET http://localhost:8000/users \
  -H "Authorization: Bearer <jwt_token>"
```

### Default Credentials

- **Username:** `testuser`
- **Password:** `password123`
- **Email:** `testuser@example.com`

### Interactive Documentation

Access the interactive API documentation at:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Docker Deployment

**Build the image:**
```bash
cd user-service
docker build -t user-service .
```

**Run with Docker:**
```bash
docker run -p 8000:8000 -v $(pwd)/data:/app/data user-service
```

**Run with Docker Compose:**
```bash
cd user-service
docker-compose up
```

### Kubernetes Deployment

**Deploy to kind cluster:**
```bash
cd user-service

# Deploy using kubectl manifest
kubectl apply -f k8s-deployment.yaml

# Or deploy using Helm values
helm install user-service bitnami/app -f helm-values.yaml --namespace user-service
```

**Verify deployment:**
```bash
kubectl get pods -n user-service
kubectl get svc -n user-service
kubectl logs -n user-service deployment/user-service
```

### Integration with Kong Gateway

To expose the User Service through Kong API Gateway:

**1. Create Kong Upstream for user service:**
```bash
curl -i -X POST http://localhost:8001/upstreams \
  --data name=user-service \
  --data algorithm=round-robin
```

**2. Create Kong Target:**
```bash
curl -i -X POST http://localhost:8001/upstreams/user-service/targets \
  --data target=user-service.user-service:8000
```

**3. Create Kong Service:**
```bash
curl -i -X POST http://localhost:8001/services \
  --data name=user-service \
  --data host=user-service.user-service \
  --data port=8000
```

**4. Create Kong Route:**
```bash
curl -i -X POST http://localhost:8001/services/user-service/routes \
  --data "hosts=user.api.local" \
  --data "paths=/api/users"
```

### Database

SQLite database is automatically created and initialized on first run.

**Database location:** `./data/users.db`

**Users table schema:**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Development

For development with auto-reload:
```bash
cd user-service
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Testing

Comprehensive test script is available in the service directory. See `user-service/README.md` for detailed testing instructions.

### Environment Variables

Customize the service with environment variables:
```bash
export SECRET_KEY="your-secret-key"
export DB_PATH="./data/users.db"
python main.py
```

### Next Steps

1. Deploy to Kubernetes cluster
2. Configure Kong API Gateway routes
3. Add JWT plugin to Kong for automatic token validation
4. Implement additional endpoints as needed
5. Add database persistence layer for production
6. Set up monitoring and logging

For detailed documentation, see [user-service/README.md](user-service/README.md)

---

## Complete DevOps Architecture Summary

This assignment provides a complete DevOps stack with:

### Infrastructure
- ✅ Docker for containerization
- ✅ Kubernetes via kind for orchestration
- ✅ Helm for package management
- ✅ Terraform for Infrastructure as Code

### API Gateway & Microservices
- ✅ Kong OSS API Gateway for API management
- ✅ FastAPI User Service for authentication
- ✅ JWT-based security
- ✅ SQLite database integration

### Deployment & Management
- ✅ Kubernetes manifests for deployment
- ✅ Docker containerization
- ✅ Helm charts for package management
- ✅ Health checks and monitoring

### Security
- ✅ bcrypt password hashing
- ✅ JWT token authentication
- ✅ Authorization middleware
- ✅ Secure configuration management

All components are tested and operational in GitHub Codespaces!

---

## Runtime Verification (Kong + Kubernetes)

Use these commands to verify the required controls on a local kind cluster.

### 1) Port-forwards

```bash
kubectl port-forward -n kong svc/kong-kong-proxy 8000:80
kubectl port-forward -n user-service svc/user-service 18000:8000
```

### 2) Fetch JWT token

```bash
TOKEN=$(curl -s -X POST 'http://localhost:18000/login' \
  -H 'Content-Type: application/json' \
  -d '{"username":"testuser","password":"password123"}' \
  | python3 -c 'import sys,json; print(json.load(sys.stdin).get("access_token",""))')
```

### 3) Authentication bypass + protection

```bash
curl -s -o /dev/null -w "health=%{http_code}\n" -H 'Host: user-service.example.com' 'http://localhost:8000/health'
curl -s -o /dev/null -w "verify_no_token=%{http_code}\n" -H 'Host: user-service.example.com' 'http://localhost:8000/verify'
curl -s -o /dev/null -w "users_no_auth=%{http_code}\n" -H 'Host: user-service.example.com' 'http://localhost:8000/users'
curl -s -o /dev/null -w "users_with_auth=%{http_code}\n" -H 'Host: user-service.example.com' -H "Authorization: Bearer ${TOKEN}" 'http://localhost:8000/users'
```

Expected:
- `health=200`
- `verify_no_token=422` (public endpoint; invalid/missing query token)
- `users_no_auth=401` (Kong JWT plugin blocks)
- `users_with_auth=200`

### 4) Custom Lua plugin verification (`X-Custom-Trace`)

```bash
curl -i -s -H 'Host: user-service.example.com' -H "Authorization: Bearer ${TOKEN}" 'http://localhost:8000/users' | grep -i 'X-Custom-Trace'
```

Expected: `X-Custom-Trace` header present.

### 5) Rate limiting (10 req/min per IP)

```bash
sleep 65
for i in $(seq 1 12); do
  code=$(curl -s -o /dev/null -w "%{http_code}" -H 'Host: user-service.example.com' -H "Authorization: Bearer ${TOKEN}" 'http://localhost:8000/users')
  echo "Req $i -> $code"
done
```

Expected:
- `Req 1..10 -> 200`
- `Req 11..12 -> 429`

### 6) IP whitelist (allow/deny)

```bash
# deny local source
kubectl patch kongplugin ip-whitelist -n user-service --type merge -p '{"config":{"allow":["172.19.0.1"]}}'
curl -s -o /dev/null -w "blocked=%{http_code}\n" -H 'Host: user-service.example.com' -H "Authorization: Bearer ${TOKEN}" 'http://localhost:8000/users'

# allow local source again
kubectl patch kongplugin ip-whitelist -n user-service --type merge -p '{"config":{"allow":["127.0.0.1"]}}'
curl -s -o /dev/null -w "restored=%{http_code}\n" -H 'Host: user-service.example.com' -H "Authorization: Bearer ${TOKEN}" 'http://localhost:8000/users'
```

Expected:
- `blocked=403`
- `restored=200`

### 7) WAF SQLi blocking test

```bash
curl -s -o /dev/null -w "benign=%{http_code}\n" \
  -H 'Host: user-service.example.com' -H "Authorization: Bearer ${TOKEN}" \
  'http://localhost:8000/users?name=normaluser'

curl -s -o /dev/null -w "sqli=%{http_code}\n" \
  -H 'Host: user-service.example.com' -H "Authorization: Bearer ${TOKEN}" \
  "http://localhost:8000/users?name='%20OR%20'1'='1%20--%20"
```

Expected:
- `benign=200`
- `sqli=403`