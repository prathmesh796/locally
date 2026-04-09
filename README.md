# Locally796

**Locally796** is an AI-powered CLI tool that automatically clones any GitHub repository and sets it up on your local machine — no manual configuration needed. Powered by a LangChain agent, it detects the project stack, installs dependencies, configures environment variables, and runs the project for you.

---

## Features

- 🤖 **AI-Driven Setup** — A LangChain agent acts as a senior DevOps engineer, analysing the repository, running the right install commands, and resolving errors automatically.
- 🔍 **Stack Detection** — Automatically identifies the project stack (Node.js, Python, Go, etc.) and applies the appropriate setup steps.
- ⚙️ **Dependency Installation** — Runs `npm install`, `pip install -r requirements.txt`, `go mod tidy`, and similar commands as needed.
- 🌿 **Environment Configuration** — Detects `.env.example` files and sets up environment variables for you.
- 🚀 **Project Launch** — Starts the project after setup and confirms it is running.
- 📦 **pip Package** — Distributed as a Python package, so you can install and use it anywhere with a single command.

---

## Requirements

- Python 3.11 or higher
- A [Groq](https://console.groq.com/) API key to power the AI agent.

---

## Installation

You can install `locally796` globally using `pip`:

```bash
pip install locally796
```

*(Alternatively, to install from source: clone this repo and run `pip install -e .` inside the folder.)*

### Setup Your API Key

Before using `locally796` for the first time, you need to configure your Groq API key. The agent defaults to `llama-3.3-70b-versatile`, which is available for any standard Groq account.

```bash
locally796 set-key <YOUR_GROQ_API_KEY>
```

This securely saves your key in a global config file (`~/.locally796/.env`), meaning you can run the tool from anywhere on your system without having to set up `.env` files manually.

---

## Usage

```bash
locally796 [GITHUB_REPO_URL] --path [CLONING_PATH]
```

### Arguments

| Argument | Description |
|---|---|
| `GITHUB_REPO_URL` | The full URL of the GitHub repository to clone and set up |
| `--path` / `-p` | *(Optional)* Local directory path where the repo will be cloned. Defaults to a folder named after the repo in the current directory |

### Example

```bash
locally796 https://github.com/prathmesh796/pubsubs --path ./test-clone
```

This single command will autonomously:
1. Clone the repository into `./test-clone`
2. Detect the technology stack (e.g. Node.js, Python)
3. Launch the LangChain Agent to investigate the codebase.
4. Install all required dependencies (`npm install`, `pip install`, etc.)
5. Configure environment variables (if `.env.example` is present)
6. Start the local development server (e.g., `npm run dev`)
7. Automatically detect and fix any deployment errors if the server fails to start!

---

## How It Works

1. **Clone** — The repo is cloned to the specified (or auto-generated) local path using GitPython.
2. **Detect** — The stack detector inspects the repository files to identify languages and frameworks.
3. **Agent Setup** — A LangChain agent equipped with shell, file-read, and file-write tools executes the full setup autonomously. If a command fails or crashes, the agent reads the error output, figures out the fix, and retries until success!
4. **Done** — The agent reports `SETUP_COMPLETE` and leaves the server running for you.

---

## License

MIT
   