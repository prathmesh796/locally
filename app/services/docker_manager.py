import os
import subprocess
import platform
import shutil
from typing import List
from app.utils.logger import logger, console
from app.services.registry import SERVICE_CONFIG

def check_docker_installed() -> bool:
    """Check if docker and docker-compose are installed."""
    has_docker = shutil.which("docker") is not None
    if not has_docker:
        return False
    
    # Check if docker compose is available
    try:
        subprocess.run(["docker", "compose", "version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            subprocess.run(["docker-compose", "version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

def ensure_docker_running() -> bool:
    """Ensure docker daemon is running. Try to start it if it is not."""
    try:
        subprocess.run(["docker", "info"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        logger.warning("Docker daemon is not running. Attempting to start it...")
        console.print("[yellow]Docker daemon is not running. Attempting to start it...[/yellow]")
        
        system = platform.system().lower()
        try:
            if system == "windows":
                # Attempt to start Docker Desktop on Windows
                subprocess.run(["powershell", "-Command", "Start-Process 'C:\\Program Files\\Docker\\Docker\\Docker Desktop.exe'"])
            elif system == "linux":
                # Attempt to start via systemctl
                subprocess.run(["sudo", "systemctl", "start", "docker"], check=True)
            elif system == "darwin": # macOS
                subprocess.run(["open", "-a", "Docker"], check=True)
            else:
                logger.error(f"Unsupported OS for automatic docker start: {system}")
                return False
                
            # Wait a bit for it to start
            console.print("[dim]Waiting for Docker to start...[/dim]")
            import time
            for _ in range(15):
                time.sleep(2)
                try:
                    subprocess.run(["docker", "info"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                    console.print("[green]Docker daemon started successfully![/green]")
                    return True
                except subprocess.CalledProcessError:
                    continue
            return False
        except Exception as e:
            logger.error(f"Failed to start Docker daemon: {e}")
            return False

def generate_compose(services: List[str], target_path: str) -> str:
    """
    Generate a docker-compose.generated.yml in the target_path.
    Returns the path to the generated file.
    """
    compose_path = os.path.join(target_path, "docker-compose.generated.yml")
    
    # Manual YAML construction to avoid adding pyyaml dependency
    yaml_lines = [
        "version: '3.8'",
        "services:"
    ]
    
    for service in services:
        if service not in SERVICE_CONFIG:
            logger.warning(f"Service {service} not found in registry.")
            continue
            
        config = SERVICE_CONFIG[service]
        yaml_lines.append(f"  {service}:")
        yaml_lines.append(f"    image: {config['image']}")
        yaml_lines.append(f"    container_name: locally796_{service}_dev")
        
        if config.get("ports"):
            yaml_lines.append("    ports:")
            for port in config["ports"]:
                yaml_lines.append(f"      - \"{port}\"")
                
        if config.get("env"):
            yaml_lines.append("    environment:")
            for k, v in config["env"].items():
                yaml_lines.append(f"      - {k}={v}")
                
        yaml_lines.append("    restart: unless-stopped")
        
    with open(compose_path, "w") as f:
        f.write("\n".join(yaml_lines) + "\n")
        
    logger.info(f"Generated docker-compose at {compose_path}")
    return compose_path

def run_compose(compose_path: str, target_path: str) -> bool:
    """Run the generated docker-compose file."""
    console.print(f"[bold blue]Starting services via Docker Compose...[/bold blue]")
    try:
        # Check if we should use `docker compose` or `docker-compose`
        cmd = ["docker", "compose"]
        try:
            subprocess.run(cmd + ["version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            cmd = ["docker-compose"]
            
        cmd.extend(["-f", compose_path, "up", "-d"])
        
        process = subprocess.run(cmd, cwd=target_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if process.returncode != 0:
            logger.error(f"Failed to start compose: {process.stderr}")
            console.print(f"[bold red]Failed to start services:[/bold red] {process.stderr}")
            return False
            
        console.print("[bold green]Services started successfully in the background![/bold green]")
        return True
    except Exception as e:
        logger.error(f"Error running compose: {e}")
        console.print(f"[bold red]Error running compose:[/bold red] {e}")
        return False
