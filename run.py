from app import app
from app.utils import monitor_file
import threading
from pathlib import Path

if __name__ == "__main__":
    file_path = Path("data.txt")
    threading.Thread(target=monitor_file, args=(file_path,), daemon=True).start()
    app.run(debug=True)