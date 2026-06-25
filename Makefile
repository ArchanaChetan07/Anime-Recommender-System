.PHONY: install build run docker-build docker-run clean lint format help

PYTHON   := python
IMAGE    := anisage-app
PORT     := 8501

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

install:  ## Install Python dependencies
	pip install --upgrade pip
	pip install -e .

build:  ## Build the vector store (run once before starting the app)
	$(PYTHON) -m pipeline.build_pipeline

run:  ## Start the Streamlit app locally
	streamlit run app/app.py --server.port=$(PORT)

lint:  ## Lint with ruff
	ruff check .

format:  ## Format with ruff
	ruff format .

docker-build:  ## Build Docker image
	docker build -t $(IMAGE):latest .

docker-run:  ## Run the Docker container locally
	docker run --rm -p $(PORT):$(PORT) \
		--env-file .env \
		$(IMAGE):latest

k8s-deploy:  ## Deploy to Kubernetes (Minikube)
	eval $$(minikube docker-env) && docker build -t $(IMAGE):latest .
	kubectl apply -f k8s/anisage-k8s.yaml

k8s-status:  ## Check Kubernetes pod status
	kubectl get pods -n anisage
	kubectl get svc  -n anisage

clean:  ## Remove build artefacts and caches
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc"     -delete 2>/dev/null || true
	rm -rf .ruff_cache dist build *.egg-info
