import socket
import time
from typing import List
from app.utils.logger import logger, console
from app.services.registry import SERVICE_CONFIG

def is_port_open(port: int) -> bool:
    """Check if a local port is open and accepting connections."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        result = s.connect_ex(("127.0.0.1", port))
        return result == 0
    except Exception:
        return False
    finally:
        s.close()

def wait_for_services(services: List[str], timeout: int = 30) -> bool:
    """
    Wait for all specified services to become ready by checking their ports.
    """
    if not services:
        return True
        
    console.print(f"[dim]Waiting up to {timeout}s for services to be ready...[/dim]")
    
    ports_to_check = []
    for service in services:
        if service in SERVICE_CONFIG and "ports" in SERVICE_CONFIG[service]:
            for port_mapping in SERVICE_CONFIG[service]["ports"]:
                # Extracts the host port from "host:container" mapping
                host_port = int(port_mapping.split(":")[0])
                ports_to_check.append((service, host_port))
                
    if not ports_to_check:
        return True
        
    start_time = time.time()
    ready_ports = set()
    
    while time.time() - start_time < timeout:
        all_ready = True
        
        for service, port in ports_to_check:
            if port in ready_ports:
                continue
                
            if is_port_open(port):
                ready_ports.add(port)
                logger.info(f"Service {service} is ready on port {port}.")
            else:
                all_ready = False
                
        if all_ready:
            console.print("[bold green]All services are ready![/bold green]")
            return True
            
        time.sleep(2)
        
    missing = [f"{s} (port {p})" for s, p in ports_to_check if p not in ready_ports]
    logger.warning(f"Timeout waiting for services: {', '.join(missing)}")
    console.print(f"[bold yellow]Warning: Some services might not be fully ready: {', '.join(missing)}[/bold yellow]")
    
    return False
