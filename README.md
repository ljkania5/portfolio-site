# Portfolio Site

My personal portfolio site, built as both a place to showcase my work and a hands-on exploration of cloud-native development.

**Live site:** *coming soon — deployment in progress*

## Stack

- **Backend:** Python, FastAPI, Jinja2
- **Frontend:** HTML, CSS (no framework — keeping it minimal)
- **Database:** PostgreSQL *(planned)*
- **Containerization:** Docker, Docker Compose *(planned)*
- **Infrastructure:** AWS (App Runner, RDS, Route 53), managed with Terraform *(planned)*
- **CI/CD:** GitHub Actions *(planned)*

## About This Project

This site is intentionally built from the infrastructure up. Rather than ship a static page, I'm using it as a real-world platform to learn cloud and DevOps practices: containerization, infrastructure as code, automated deployments, and observability.

I'll be writing about the journey as I go.

## Running Locally

```bash
# Clone and enter the project
git clone https://github.com/YOUR-USERNAME/portfolio-site.git
cd portfolio-site

# Set up the virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the dev server
uvicorn app.main:app --reload
```

Then visit [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Roadmap

- [x] Phase 1: FastAPI app with templated multi-page site
- [ ] Phase 2: Docker + PostgreSQL via Docker Compose
- [ ] Phase 3: Deploy to AWS App Runner with RDS
- [ ] Phase 4: Terraform IaC + GitHub Actions CI/CD
- [ ] Phase 5: ECS Fargate, monitoring, blog