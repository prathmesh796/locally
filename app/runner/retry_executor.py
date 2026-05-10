from typing import Dict, Any
from app.services.executor import execute_command
from app.orchestrator.service_manager import handle_missing_services
from app.utils.logger import logger, console

def execute_with_retry(command: str, cwd: str, timeout: int = 60, auto_services: bool = False) -> Dict[str, Any]:
    """
    Executes a command. If it fails, checks logs for missing services.
    If missing services are detected and started, retries the command once.
    """
    # First attempt
    result = execute_command(command, cwd, timeout)
    
    if result["status"] == "error" or result["return_code"] != 0:
        # Combine stdout and stderr for detection
        logs = f"{result.get('stdout', '')}\n{result.get('stderr', '')}"
        
        # Check if we can handle it by starting missing services
        handled = handle_missing_services(logs, target_path=cwd, auto_services=auto_services)
        
        if handled:
            console.print(f"[bold cyan]Retrying command after starting services:[/bold cyan] {command}")
            logger.info("Retrying command after starting services.")
            # Second attempt
            result = execute_command(command, cwd, timeout)
            
    return result
