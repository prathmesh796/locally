# Locally

**Locally** is an AI-powered CLI tool that automatically clones any GitHub repository and sets it up on your local machine — no manual configuration needed. Powered by a LangChain agent, it detects the project stack, installs dependencies, configures environment variables, and runs the project for you.

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
- A [Groq](https://console.groq.com/) API key (set as `GROQ_API_KEY` in your environment or a `.env` file)

---

## Installation

```bash
pip install locally
```

---

## Usage

```bash
locally [GITHUB_REPO_URL] --path [CLONING_PATH]
```

### Arguments

| Argument | Description |
|---|---|
| `GITHUB_REPO_URL` | The full URL of the GitHub repository to clone and set up |
| `--path` / `-p` | *(Optional)* Local directory path where the repo will be cloned. Defaults to a folder named after the repo in the current directory |

### Example

```bash
locally https://github.com/prathmesh796/getlancer --path ./my-project
```

This command will:
1. Clone the repository into `./my-project`
2. Detect the technology stack
3. Install all dependencies
4. Configure environment variables (if `.env.example` is present)
5. Start the project

---

## How It Works

1. **Clone** — The repo is cloned to the specified (or auto-generated) local path using GitPython.
2. **Detect** — The stack detector inspects the repository files to identify languages and frameworks.
3. **Agent Setup** — A LangChain agent equipped with shell, file-read, and file-write tools executes the full setup autonomously. If a command fails, the agent reads the error output, figures out the fix, and retries.
4. **Done** — The agent reports `SETUP_COMPLETE` and summarises what it did.

---

## License

MIT
   