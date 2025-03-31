from datetime import datetime
import os

def save_log(tool_name, result):
    os.makedirs("logs", exist_ok=True)
    with open("logs/calculation_history.csv", "a") as file:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{now},{tool_name},{result}\n")
