import typer
import os
from typing import Optional
from rich.console import Console

from app.services.repo import clone_repo
from app.services.detector import detect_stack
from app.core.agent import run_setup_and_start
from app.utils.logger import logger

app = typer.Typer(help="Locally - AI powered CLI tool to clone and run any repo.", add_completion=False)
console = Console()

@app.command()
def set_key(api_key: str = typer.Argument(..., help="Your Groq API Key")):
    """Sets the global Groq API key for Locally."""
    home_dir = os.path.expanduser("~/.locally")
    os.makedirs(home_dir, exist_ok=True)
    env_file = os.path.join(home_dir, ".env")
    
    with open(env_file, "w") as f:
        f.write(f"GROQ_API_KEY={api_key}\n")
    
    console.print("[bold green]✅ API Key saved successfully![/bold green] You can now run `locally` from anywhere.")

@app.command()
def clone_and_run(
    repo_url: str = typer.Argument(..., help="The GitHub repository URL to process"),
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Destination path for cloning"),
):
    """
    Clone a repository, detect stack, install dependencies, and run it.
    """
    console.print(f"[bold blue]Starting Locally for:[/bold blue] {repo_url}")
    if path:
        target_path = path
    else:
        # Predict the repo name from the url
        base_name = repo_url.rstrip('/').split('/')[-1]
        if base_name.endswith('.git'):
            base_name = base_name[:-4]
        target_path = os.path.join(os.getcwd(), base_name)
    
    console.print(f"[bold blue]Target path:[/bold blue] {target_path}")

    # Step 1: Clone Repo
    success = clone_repo(repo_url, target_path)
    if not success:
        console.print("[bold red]Aborting due to clone failure.[/bold red]")
        raise typer.Exit(code=1)

    # Step 2: Detect Stack
    detected_stacks = detect_stack(target_path)

    # Step 3: Run Setup Agent
    run_setup_and_start(target_path, detected_stacks)
    
if __name__ == "__main__":
    app()
