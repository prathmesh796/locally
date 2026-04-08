import subprocess
import sys
from typing import Dict, Any
from app.utils.logger import logger, console

def execute_command(command: str, cwd: str, timeout: int = 60) -> Dict[str, Any]:
    """Execute a shell command and return its output. Includes a timeout for long-running processes."""
    logger.info(f"Executing: `{command}` in {cwd} with timeout {timeout}s")
    console.print(f"[dim]Running:[/dim] {command}")
    
    try:
        process = subprocess.Popen(
            command,
            cwd=cwd,
            shell=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        try:
            stdout, stderr = process.communicate(timeout=timeout)
            return {
                "command": command,
                "return_code": process.returncode,
                "stdout": stdout.strip() if stdout else "",
                "stderr": stderr.strip() if stderr else "",
                "status": "completed"
            }
        except subprocess.TimeoutExpired:
            logger.warning(f"Execution timed out after {timeout} seconds.")
            
            if sys.platform == "win32":
                subprocess.run(f"taskkill /F /T /PID {process.pid}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                process.kill()
                
            try:
                stdout, stderr = process.communicate(timeout=2)
            except subprocess.TimeoutExpired:
                stdout, stderr = "Process is still running (Timeout reached). Likely a server started successfully.", ""
                
            return {
                "command": command,
                "return_code": 0,
                "stdout": stdout.strip() if stdout else "Process is still running (Timeout reached). Likely a server started successfully.",
                "stderr": stderr.strip() if stderr else "",
                "status": "timeout"
            }
    except Exception as e:
        logger.error(f"Execution failed: {e}")
        return {
            "command": command,
            "return_code": -1,
            "stdout": "",
            "stderr": str(e),
            "status": "error"
        }
