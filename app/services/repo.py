import os
import git
from app.utils.logger import logger, console

def clone_repo(repo_url: str, target_path: str) -> bool:
    try:
        if os.path.exists(target_path) and os.path.isdir(target_path):
            if os.listdir(target_path):
                logger.info(f"Target directory {target_path} already exists and is not empty.")
                console.print(f"[yellow]Skipping clone, directory not empty: {target_path}[/yellow]")
                return True
        logger.info(f"Cloning {repo_url} into {target_path}...")
        with console.status(f"[bold green]Cloning {repo_url}...[/bold green]"):
            git.Repo.clone_from(repo_url, target_path)
        logger.info("Clone completed successfully.")
        console.print("[bold green]✓ Repository cloned successfully.[/bold green]")
        return True
    except Exception as e:
        logger.error(f"Failed to clone repository: {str(e)}")
        console.print(f"[bold red]✗ Failed to clone repository: {str(e)}[/bold red]")
        return False
