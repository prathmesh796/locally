import os
import re
from typing import List
from rich.prompt import Confirm
from app.utils.logger import logger, console
from app.detector.error_parser import detect_services
from app.services.docker_manager import check_docker_installed, ensure_docker_running, generate_compose, run_compose
from app.services.health_check import wait_for_services
from app.services.registry import SERVICE_CONFIG

def pre_detect_services(target_path: str) -> List[str]:
    """
    Scan common files in the repository to detect required services beforehand.
    """
    detected = set()
    files_to_check = {
        ".env": ["postgres", "redis", "mongodb", "mysql", "rabbitmq", "kafka", "memcached", "mariadb", "neo4j", "elasticsearch"],
        ".env.example": ["postgres", "redis", "mongodb", "mysql", "rabbitmq", "kafka", "memcached", "mariadb", "neo4j", "elasticsearch"],
        "docker-compose.yml": list(SERVICE_CONFIG.keys()),
        "docker-compose.yaml": list(SERVICE_CONFIG.keys()),
        "requirements.txt": {
            "psycopg2": "postgres", "redis": "redis", "pymongo": "mongodb", 
            "mysqlclient": "mysql", "elasticsearch": "elasticsearch", "pika": "rabbitmq",
            "confluent-kafka": "kafka", "pymemcache": "memcached", "neo4j": "neo4j"
        },
        "package.json": {
            "pg": "postgres", "redis": "redis", "ioredis": "redis", "mongodb": "mongodb",
            "mongoose": "mongodb", "mysql": "mysql", "mysql2": "mysql", "@elastic/elasticsearch": "elasticsearch",
            "amqplib": "rabbitmq", "kafkajs": "kafka", "neo4j-driver": "neo4j"
        }
    }
    
    for filename, indicators in files_to_check.items():
        filepath = os.path.join(target_path, filename)
        if not os.path.exists(filepath):
            continue
            
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read().lower()
                
                if isinstance(indicators, list):
                    for service in indicators:
                        # Simple string check
                        if service in content:
                            detected.add(service)
                elif isinstance(indicators, dict):
                    for keyword, service in indicators.items():
                        if keyword in content:
                            detected.add(service)
        except Exception as e:
            logger.warning(f"Failed to read {filepath} for pre-detection: {e}")
            
    # Add zookeeper if kafka is found
    if "kafka" in detected:
        detected.add("zookeeper")
        
    return list(detected)

def process_services(services: List[str], target_path: str, ask_permission: bool = True) -> bool:
    """
    Common flow for bringing up services: check, prompt, start, wait.
    """
    if not services:
        return False
        
    console.print(f"\n[bold magenta]🚀 Local Services Needed:[/bold magenta] {', '.join(services)}")
    
    if ask_permission:
        # Prompt user
        if not Confirm.ask("[bold yellow]Do you want Locally796 to automatically start these services via Docker Compose?[/bold yellow]"):
            console.print("[dim]Skipping auto-services setup.[/dim]")
            return False
            
    if not check_docker_installed():
        console.print("[bold red]Docker or Docker Compose is not installed! Cannot start services.[/bold red]")
        return False
        
    if not ensure_docker_running():
        console.print("[bold red]Docker daemon could not be started. Please start Docker manually.[/bold red]")
        return False
        
    compose_path = generate_compose(services, target_path)
    success = run_compose(compose_path, target_path)
    
    if success:
        wait_for_services(services)
        return True
        
    return False

def handle_missing_services(logs: str, target_path: str, auto_services: bool = False) -> bool:
    """
    Detect missing services from execution logs, ask for permission, and bring them up.
    Returns True if services were detected and successfully brought up.
    """
    services = detect_services(logs)
    if not services:
        return False
        
    # If auto_services flag is False, we might want to ask or we might just skip.
    # We will ask permission if it was not explicitly skipped
    logger.info(f"Detected missing services from logs: {services}")
    
    return process_services(services, target_path, ask_permission=True)
