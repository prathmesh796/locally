import os
from typing import List
from utils.constants import STACK_FILES
from utils.logger import logger, console

def detect_stack(target_path: str) -> List[str]:
    detected = []
    logger.info(f"Detecting stack in {target_path}...")
    for filename, stack_name in STACK_FILES.items():
        file_path = os.path.join(target_path, filename)
        if os.path.exists(file_path):
            detected.append(stack_name)
    
    # Deduplicate while preserving order if needed
    detected = list(set(detected))
    
    if detected:
        console.print(f"[bold green]✓ Detected Stack:[/bold green] {', '.join(detected)}")
        logger.info(f"Detected stacks: {detected}")
    else:
        console.print("[yellow]⚠ Could not automatically detect a standard stack.[/yellow]")
        logger.warning("No stack detected.")
    
    return detected
