from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from core.llm import get_llm
from core.tools import run_shell_command, read_file, list_dir, write_file
from utils.logger import logger, console

AGENT_SYSTEM_PROMPT = """You are a senior DevOps engineer and setup assistant.
Your task is to properly setup and run a software project.

You have the following capabilities:
1. Examine project files and directories to understand the structure.
2. Formulate necessary setup commands (e.g. `npm install`, `pip install -r requirements.txt`, `go mod tidy`).
3. Set up environment variables if a `.env.example` exists. 
4. Execute run commands (e.g. `npm run dev`, `python app.py`) to verify it works.

If a command fails, read its output, figure out the issue, fix it, and retry.
NEVER execute obviously destructive commands (like `rm -rf /`).
Always execute commands in the correct `cwd` which the user provides as context.
Important: When running a dev server that blocks (like `npm run dev`), if it prints 'compiled successfully' or starts listening on a port, consider the step SUCCESSFUL. Our executor incorporates a 60-second timeout. If it prints a timeout error but indicates a server has started, consider the operation successful.

When you have successfully set everything up and run the project, respond with "SETUP_COMPLETE" and explain what you did.
"""

def run_setup_and_start(target_path: str, detected_stacks: list):
    try:
        llm = get_llm()
    except Exception as e:
        console.print(f"[bold red]LLM Initialization Error:[/bold red] {e}")
        return

    tools = [run_shell_command, read_file, list_dir, write_file]

    prompt = ChatPromptTemplate.from_messages([
        ("system", AGENT_SYSTEM_PROMPT),
        ("human", "Set up the project in the `{target_path}` directory.\nDetected stacks: {detected_stacks}.\nPlease execute the installation steps and then run the project. Use your tools sequentially to accomplish this."),
        ("placeholder", "{agent_scratchpad}"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

    console.print(f"[bold blue]Initializing Setup Agent for:[/bold blue] {target_path}")
    logger.info("Starting agent executor.")
    
    try:
        response = agent_executor.invoke({
            "target_path": target_path,
            "detected_stacks": ", ".join(detected_stacks) if detected_stacks else "Unknown"
        })
        console.print("[bold green]Agent completed its process.[/bold green]")
        logger.info(f"Agent response: {response.get('output', '')}")
    except Exception as e:
        console.print(f"[bold red]Agent encountered a fatal error:[/bold red] {e}")
        logger.error(f"Agent execution failed: {e}")
