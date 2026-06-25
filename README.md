# ⛩️ AniSage — AI-Powered Anime Recommender

> Discover your next favourite anime with a RAG-based recommendation engine powered by LLaMA 3.1, ChromaDB, and LangChain — deployed on Kubernetes with Grafana monitoring.

---

## ✨ Features

- **Semantic search** — understands natural-language preferences, not just keywords
- **RAG pipeline** — retrieves the most relevant anime from a vector store before generating recommendations
- **LLaMA 3.1 via Groq** — fast, high-quality LLM inference
- **HuggingFace Embeddings** — `all-MiniLM-L6-v2` for lightweight, accurate embeddings
- **ChromaDB** — persistent local vector store
- **Streamlit UI** — dark anime-themed interface, mobile-friendly
- **Kubernetes-ready** — includes HPA, health probes, rolling updates, and resource limits
- **Grafana monitoring** — Kubernetes cluster observability via Helm

---

## 🏗️ Architecture

```
User Query (Streamlit)
        │
        ▼
AnimeRecommendationPipeline
        │
        ├── VectorStoreManager ──► ChromaDB (semantic retrieval)
        │        └── HuggingFace Embeddings (all-MiniLM-L6-v2)
        │
        └── AnimeRecommender
                 └── LangChain RetrievalQA
                          └── ChatGroq (LLaMA 3.1-8b-instant)
```

---

## 📁 Project Structure

```
anisage/
├── app/
│   └── app.py                  # Streamlit frontend
├── config/
│   └── settings.py             # Centralised settings (dataclass + env validation)
├── data/
│   └── anime_with_synopsis.csv # Raw MAL dataset (~268 titles)
├── pipeline/
│   ├── build_pipeline.py       # One-time ETL + vector store build
│   └── pipeline.py             # Runtime recommendation pipeline
├── src/
│   ├── data_loader.py          # Data loading & preprocessing
│   ├── vector_store.py         # ChromaDB build & retrieval
│   ├── recommender.py          # LLM chain + typed result
│   └── prompt_template.py      # AniSage system prompt
├── utils/
│   ├── logger.py               # Structured logging (console + rotating file)
│   └── exceptions.py           # AppException with file/line context
├── k8s/
│   └── anisage-k8s.yaml        # Namespace, Deployment, HPA, Service
├── .github/workflows/
│   └── ci.yml                  # Lint → Test → Docker build CI/CD
├── .env.example                # Environment variable template
├── Dockerfile                  # Multi-stage build (builder + runtime)
├── Makefile                    # Developer convenience commands
├── requirements.txt
└── setup.py
```

---

## 🚀 Quick Start

### 1. Clone & install

```bash
git clone https://github.com/data-guru0/ANIME-RECOMMENDER-SYSTEM-LLMOPS.git
cd ANIME-RECOMMENDER-SYSTEM-LLMOPS
make install
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env and fill in GROQ_API_KEY and HUGGINGFACEHUB_API_TOKEN
```

### 3. Build the vector store (once)

```bash
make build
# or: python -m pipeline.build_pipeline
```

### 4. Run the app

```bash
make run
# Open http://localhost:8501
```

---

## 🐳 Docker

```bash
make docker-build
make docker-run
```

---

## ☸️ Kubernetes (Minikube)

```bash
# Build image inside Minikube's Docker daemon
make k8s-deploy

# Create secrets
kubectl create secret generic anisage-secrets \
  --from-literal=GROQ_API_KEY="<your-key>" \
  --from-literal=HUGGINGFACEHUB_API_TOKEN="<your-token>" \
  -n anisage

# Expose via Minikube
minikube tunnel &
kubectl port-forward svc/anisage-service 8501:80 --address 0.0.0.0 -n anisage

# Check status
make k8s-status
```

---

## 📊 Grafana Cloud Monitoring

1. Create a free account at [grafana.com/cloud](https://grafana.com/cloud)
2. Go to **Observability → Kubernetes → Start sending data**
3. Follow the Helm install wizard (select cluster name `minikube`, namespace `monitoring`)
4. Apply the generated Helm chart to your cluster

```bash
kubectl create ns monitoring
helm repo add grafana https://grafana.github.io/helm-charts && helm repo update
helm upgrade --install --atomic --timeout 300s grafana-k8s-monitoring \
  grafana/k8s-monitoring --namespace monitoring --values values.yaml
```

---

## ⚙️ Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `GROQ_API_KEY` | ✅ | — | Groq API key |
| `HUGGINGFACEHUB_API_TOKEN` | ✅ | — | HuggingFace token |
| `MODEL_NAME` | ❌ | `llama-3.1-8b-instant` | Groq model name |
| `LLM_TEMPERATURE` | ❌ | `0` | LLM temperature |
| `EMBEDDING_MODEL` | ❌ | `all-MiniLM-L6-v2` | Sentence transformer model |
| `CHROMA_PERSIST_DIR` | ❌ | `chroma_db` | ChromaDB directory |
| `CHUNK_SIZE` | ❌ | `1000` | Text splitter chunk size |
| `CHUNK_OVERLAP` | ❌ | `100` | Text splitter overlap |
| `RETRIEVER_K` | ❌ | `5` | Number of docs to retrieve |

---

## 🛠️ Developer Commands

```bash
make help        # List all commands
make install     # Install dependencies
make build       # Build vector store
make run         # Start Streamlit app
make lint        # Ruff lint
make format      # Ruff format
make clean       # Remove caches
```

---

## 📜 License

MIT © Sudhanshu
