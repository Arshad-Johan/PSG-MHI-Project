import requests
import random
import time
from datetime import datetime

url = "http://127.0.0.1:5000/api/receive_machine_data"

parts = ["NEXON", "NEXON SV", "NEXON A", "XYZ"]
operators = ["XYZ", "ABC", "PQR", "LMN"]
status_choices = ["RUNNING", "IDLE", "LOAD UNLOAD"]

base = 1800
ideal_cycle_time = 1.2  # seconds
planned_production_time = 8 * 60 * 60  # 8 hours in seconds

while True:
    for machine_id in range(1, 5):
        status = random.choice(status_choices)
        part = parts[machine_id-1]
        operator = operators[machine_id-1]
        actual = random.randint(1500, 1800)
        operating_time = random.randint(5*60*60, planned_production_time)  # 5-8 hours
        total_count = actual
        good_count = random.randint(int(0.95*total_count), total_count)
        data = {
            "machine_id": machine_id,
            "status": status,
            "part": part,
            "operator": operator,
            "base": base,
            "actual": actual,
            "planned_production_time": planned_production_time,
            "operating_time": operating_time,
            "ideal_cycle_time": ideal_cycle_time,
            "total_count": total_count,
            "good_count": good_count,
            "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        try:
            r = requests.post(url, json=data)
            print(f"Posted mock data for Machine {machine_id}: {r.status_code}")
        except Exception as e:
            print(f"Error posting data: {e}")
    time.sleep(5) 