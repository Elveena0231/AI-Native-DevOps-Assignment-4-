# AI Usage Notes

This repository contains auto-generated scaffolding and some components produced
with AI assistance. Use the components as a starting point and review code for
security and correctness before deployment.

## AI tools used

- GitHub Copilot (Chat) in VS Code / GitHub Codespaces
- AI-assisted prompt-to-code generation for:
	- FastAPI microservice scaffolding
	- Dockerfile creation
	- Helm chart templates and values
	- Kong configuration and custom Lua plugin scaffolding
	- Terraform starter files
	- Test command generation (curl / validation scripts)

## Prompt interactions and history

The exact prompt history used during setup and development is captured below.

Suggested next steps:
- Review `kong/` Dockerfile and build process for custom plugins.
- Replace placeholder secrets and images with secure, production-ready values.
- Add CI to validate Helm templates and Terraform plans on PRs.

## User-provided prompt history (verbatim)

Environment Setup Prompts  

Step 1: Install Docker
Code Prompt: "Generate installation steps for Docker inside GitHub Codespaces (Ubuntu-based). Ensure Docker daemon runs correctly and verify with `docker run hello-world`."

Step 2: Install Kubernetes (kind or k3d for local cluster)
Code Prompt: "Provide installation steps for kind (Kubernetes in Docker) inside GitHub Codespaces. Include cluster creation command and verification with `kubectl get nodes`."

Step 3: Install kubectl
Code Prompt: "Generate installation steps for kubectl inside GitHub Codespaces. Verify installation with `kubectl version --client`."

Step 4: Install Helm
Code Prompt: "Provide installation steps for Helm inside GitHub Codespaces. Verify installation with `helm version`."

Step 5: Install Terraform (optional but required by assignment)
Code Prompt: "Generate installation steps for Terraform inside GitHub Codespaces. Verify installation with `terraform -version`."

Step 6: Install Kong Gateway (OSS)
Code Prompt: "Provide Helm-based installation steps for Kong OSS Gateway on Kubernetes cluster created with kind. Include namespace creation, Helm repo add, and Helm install commands."

⚙️ Application Build Prompts
Now the actual application scaffolding. Each of these prompts can be fed into Copilot to generate code/config.

Step 1: Microservice (User Service)
Code Prompt: "Generate a Python FastAPI microservice with SQLite database. APIs: POST /login (returns JWT), GET /verify (validates JWT), GET /users (JWT required), GET /health (public, no auth). Use secure password hashing with bcrypt. Auto-initialize SQLite DB with sample user."

Step 2: Dockerize Microservice
Code Prompt: "Write a Dockerfile for the FastAPI microservice. Use python:3.11-slim, install dependencies from requirements.txt, expose port 8000, run with uvicorn."

Step 3: Helm Chart for Microservice
Code Prompt: "Generate Helm chart for user-service microservice. Include Deployment, Service, ConfigMap for environment variables, and parameterized values.yaml."

Step 4: Kong Configuration
Code Prompt: "Generate kong.yaml declarative config for routing traffic to user-service. Enable JWT plugin for /users, bypass auth for /health and /verify. Externalize JWT secrets via Kubernetes Secret."

Step 5: Kong Custom Lua Plugin
Code Prompt: "Write a custom Kong Lua plugin that injects a response header `X-Custom-Trace` with request ID. Place code in kong/plugins/custom.lua and reference it in kong.yaml."

Step 6: Rate Limiting
Code Prompt: "Configure Kong rate-limiting plugin for IP-based limits: 10 requests per minute per IP. Add this to kong.yaml."

Step 7: IP Whitelisting
Code Prompt: "Configure Kong IP restriction plugin to allow only CIDR ranges defined in values.yaml. Block all other inbound traffic."

Step 8: DDoS Protection
Code Prompt: "Integrate ModSecurity with Kong Gateway on Kubernetes. Explain why ModSecurity is chosen, show Helm values to enable WAF, and demonstrate blocking of malicious requests."

Step 9: Terraform Infrastructure
Code Prompt: "Write Terraform configuration to provision Kubernetes namespace `api-platform`, networking policies, and base infra for Kong + microservice. Parameterize cluster name and CIDR ranges."

📂 Repository Structure Prompt
Code Prompt: "Generate repository structure with folders: microservice/, helm/user-service/, helm/kong/, kong/plugins/, kong/kong.yaml, k8s/deployment.yaml, terraform/, README.md, ai-usage.md. Populate each with starter files."

🧪 Testing Prompts
Rate Limiting Test
Code Prompt: "Generate curl commands to test Kong rate limiting (10 requests/min per IP). Show expected 429 Too Many Requests response."

IP Whitelisting Test
Code Prompt: "Generate curl commands to test Kong IP restriction plugin. Show allowed response from whitelisted IP and forbidden response from blocked IP."

DDoS Protection Test
Code Prompt: "Generate test scenario for ModSecurity with Kong. Simulate SQL injection atte"
