# Honeycomb - Repeatable Workflows via Natural Language

[Devpost](https://devpost.com/software/coeus-pfvn7c)

Our project enables **_Repeatable Workflows via Natural Language_**, automating multi-step processes with ease. It connects to a number of data sources and uses agents to take actions during execution. Workflows are saved as checkpointed graphs for reliability. RAG-powered memory preserves context for adaptive automation.

Refer to the [Devpost](https://devpost.com/software/coeus-pfvn7c) for more details.

## Running the Project

### Requirements

- Docker & Docker Compose [(installable via Docker Desktop)](https://www.docker.com/products/docker-desktop/)
- `Python >= 3.12`

### Setup & Startup

All of the following commands should be run from the root `honeycomb/` directory.

```sh
# Create a virtual environment and install Python dependencies
./scripts/create_python_env.sh

# Activate the venv
source .venv/bin/activate

# Spin up a local ElasticSearch database
docker compose up

# Start the API
./scripts/start_api.sh
```

### Starting the web app

From `honeycomb/apps/coeus-fe/`

```sh
npm i
npm run start
```
