# RAG_from_scratch
The following are required:
- docker
- Makefile

<br>

# How to develop backend in vscode.
## 1. Find poetry virtual env path
```shell
poetry env info --path
```
## 2. set virtualenv path to vscode global settings.
- add poetry env path to vscode `python.pythonPath`.
  - `python.pythonPath` is at setting - search `venv`
reference: https://stackoverflow.com/questions/59882884/vscode-doesnt-show-poetry-virtualenvs-in-select-interpreter-option

<br><br>

# How to run
## 1. Create `.env.dev`
You must write the `.env.dev` file as it controls the overall environment variables. <br>
Here is how you can do it.
- 1. Create `.env.dev` in the root directory.
- 2. Write the `.env.dev` file. Make sure to refer to the `.env.template` file when writing it.

## 2. Init Backend & Run Backend
`Makefile` makes it easy to initialize backend. <br>
It automates building images, create docker compose network.

### Init backend
```shell
make init_backend
```
### Run backend
```shell
make run_backend
make down_backend <- it down the backend container
```

<br><br>

# Detail running proccessing
## 1. build the images
There are two methods for building images: the basic way and the Makefile way.
### A. Basic
- In ./backend,
```shell
docker build -t rag_backend:0.1 -f backend.dockerfile .
```
### B. Makefile
- In root dir
```shell
make build_backend
```
## 2. Create docker network
You have to set docker compose network name in `.env.dev`.

### A. Basic
``` shell
docker network create {network_name}
```
### B. Makefile
```shell
make create_network
```
## 3. compose up
There are two methods to launch the compose: the basic way and the Makefile way.
### A. Basic
- In root dir
```shell
docker compose --env-file .env.dev -f docker-compose.backend.dev.yml up -d
```
### B. Makefile
- In root dir
```shell
make run_backend
make down_backend
```

<br>

# Default port
## backend
- 8000:8000
## ollama
- 11434:11434

<br>
