from datetime import datetime
import os
from pathlib import Path
from datetime import datetime

def save_log(tool_name, result):
    os.makedirs("logs", exist_ok=True)
    with open("logs/calculation_history.txt", "a", encoding="utf-8") as file:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{now},{tool_name},{result}\n")
        
def save_log(name, content):
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)  # Create folder if missing
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = log_dir / f"{name}_{timestamp}.txt"
    file_path.write_text(content.strip())