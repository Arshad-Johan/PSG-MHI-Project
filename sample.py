import requests
import json
import time
from datetime import datetime
from pyModbusTCP.client import ModbusClient

# URLs for the post and get session

url_event = "http://127.0.0.1:5000/api/receive_machine_data"

# Add your own cloud server URL here
url_my_cloud = "https://smiling-memory-450310-d2.uc.r.appspot.com/api/receive_machine_data"
# Variable to store the previous data

winding_previous_data = None
winding_previous_data1=None

winding_ar1_previous_value = 0
winding_ar1_current_value = 0

slot_inserter_previous_data = None
slot_inserter_previous_data1 = None

slot_inserter_previous_value = 0
slot_inserter_current_value =0

Hot_Stacking_previous_data = None
Hot_Stacking_previous_data1 = None

Hot_Stacking_previous_value = 0
Hot_Stacking_current_value = 0

Wedge_Inserter_previous_data = None
Wedge_Inserter_previous_data1 = None

Wedge_Inserter_previous_value = 0
Wedge_Inserter_current_value = 0
# Function to fetch winding values from Modbus

def fetch_winding_values_1():
    ModbusBMS = ModbusClient(host="192.168.3.200", port=502, unit_id=1, auto_open=True, auto_close=True)
    values = ModbusBMS.read_holding_registers(6707, 1) #m20 machine idle
    return values

def fetch_winding_values_2():
    ModbusBMS = ModbusClient(host="192.168.3.200", port=502, unit_id=1, auto_open=True, auto_close=True)
    values_2 = ModbusBMS.read_holding_registers(6351, 1) #m924 cycle Start stop register bit
    return values_2

def fetch_winding_values_3():
    ModbusBMS = ModbusClient(host="192.168.3.200", port=502, unit_id=1, auto_open=True, auto_close=True)
    values_3 = ModbusBMS.read_holding_registers(7720, 6) #alarm
    return values_3

def fetch_winding_values_4():
    ModbusBMS = ModbusClient(host="192.168.3.200", port=502, unit_id=1, auto_open=True, auto_close=True)
    values_4 = ModbusBMS.read_holding_registers(6000, 125) #starting parameters
    if values_4:
        values_4 = [0 if value is None else value for value in values_4]
        # Create a string representation of the values
        values_str = ", ".join(map(str, values_4))
        return values_str
    return None
    #return values_4
    
# Function to fetch slot_inserter values from Modbus

def fetch_slot_inserter_values_1():
    ModbusBMS = ModbusClient(host="192.168.3.200", port=502, unit_id=1, auto_open=True, auto_close=True)
    values = ModbusBMS.read_holding_registers(6706, 1) #m20 machine idle
    return values

def fetch_slot_inserter_values_2():
    ModbusBMS = ModbusClient(host="192.168.3.200", port=502, unit_id=1, auto_open=True, auto_close=True)
    values_2 = ModbusBMS.read_holding_registers(6705,1)#924cycle Start stop register bit
    return values_2

def fetch_slot_inserter_values_3():
    ModbusBMS = ModbusClient(host="192.168.3.200", port=502, unit_id=1, auto_open=True, auto_close=True)
    values_3 = ModbusBMS.read_holding_registers(7726, 6) #alarm
    return values_3
def fetch_slot_inserter_values_4():
    ModbusBMS = ModbusClient(host="192.168.3.200", port=502, unit_id=1, auto_open=True, auto_close=True)
    values_4 = ModbusBMS.read_holding_registers(6000, 125) #starting parameters
    if values_4:
        values_4 = [0 if value is None else value for value in values_4]
        # Create a string representation of the values
        values_str = ", ".join(map(str, values_4))
        return values_str
    return None
    #return values_4
    
# Function to fetch Hot_Stacking values from Modbus

def fetch_Hot_Stacking_values_1():
    ModbusBMS = ModbusClient(host="192.168.3.200", port=502, unit_id=1, auto_open=True, auto_close=True)
    values = ModbusBMS.read_holding_registers(6712, 1) #m20 machine idle
    return values

def fetch_Hot_Stacking_values_2():
    ModbusBMS = ModbusClient(host="192.168.3.200", port=502, unit_id=1, auto_open=True, auto_close=True)
    values_2 = ModbusBMS.read_holding_registers(6711,1)#924cycle Start stop register bit
    return values_2

def fetch_Hot_Stacking_values_3():
    ModbusBMS = ModbusClient(host="192.168.3.200", port=502, unit_id=1, auto_open=True, auto_close=True)
    values_3 = ModbusBMS.read_holding_registers(7732, 6) #alarm
    return values_3
def fetch_Hot_Stacking_values_4():
    ModbusBMS = ModbusClient(host="192.168.3.200", port=502, unit_id=1, auto_open=True, auto_close=True)
    values_4 = ModbusBMS.read_holding_registers(6000, 125) #starting parameters
    if values_4:
        values_4 = [0 if value is None else value for value in values_4]
        # Create a string representation of the values
        values_str = ", ".join(map(str, values_4))
        return values_str
    return None
    #return values_4
    
# Function to fetch Wedge_Inserter values from Modbus

def fetch_Wedge_Inserter_values_1():
    ModbusBMS = ModbusClient(host="192.168.3.200", port=502, unit_id=1, auto_open=True, auto_close=True)
    values = ModbusBMS.read_holding_registers(6714, 1) #m20 machine idle
    return values

def fetch_Wedge_Inserter_values_2():
    ModbusBMS = ModbusClient(host="192.168.3.200", port=502, unit_id=1, auto_open=True, auto_close=True)
    values_2 = ModbusBMS.read_holding_registers(6713,1)#924cycle Start stop register bit
    return values_2

def fetch_Wedge_Inserter_values_3():
    ModbusBMS = ModbusClient(host="192.168.3.200", port=502, unit_id=1, auto_open=True, auto_close=True)
    values_3 = ModbusBMS.read_holding_registers(7738, 6) #alarm
    return values_3
def fetch_Wedge_Inserter_values_4():
    ModbusBMS = ModbusClient(host="192.168.3.200", port=502, unit_id=1, auto_open=True, auto_close=True)
    values_4 = ModbusBMS.read_holding_registers(6000, 125) #starting parameters
    if values_4:
        values_4 = [0 if value is None else value for value in values_4]
        # Create a string representation of the values
        values_str = ", ".join(map(str, values_4))
        return values_str
    return None
    #return values_4

# Function to get the current date and time

def get_current_datetime():
    return datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

# Function to post winding data to the local web app

def post_winding_data_to_cloud(event_id, data_values):
    current_datetime = get_current_datetime()
    # No auth key needed for local dev

    payload = {
        "did": "NAVTATblrMachine1",
        "eid": event_id,
        "cid": "1",
        "dt": current_datetime,
        "einfo": {"e1": data_values} if data_values is not None else {}
    }

    print(f"Current Date and Time: {current_datetime}")
    print(f"Data to post: {payload}")

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url_event, headers=headers, json=payload)
        response.raise_for_status()
        print("Winding Data posted to local web app successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to post winding data to '{url_event}'. Error: {e}\n{response.text if 'response' in locals() else ''}")

# NOTE: This file is now configured to send data to the local Flask web app at http://127.0.0.1:5000/api/receive_machine_data
# Function to post slot_inserter data to the local web app

def post_slot_inserter_data_to_cloud(event_id, data_values):
    current_datetime = get_current_datetime()
    payload = {
        "did": "NAVTATblrMachine1",
        "eid": event_id,
        "cid": "1",
        "dt": current_datetime,
        "einfo": {"e1": data_values} if data_values is not None else {}
    }
    print(f"Current Date and Time: {current_datetime}")
    print(f"Data to post: {payload}")
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(url_event, headers=headers, json=payload)
        response.raise_for_status()
        print("slot_inserter Data posted to local web app successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to post slot_inserter data to '{url_event}'. Error: {e}\n{response.text if 'response' in locals() else ''}")

# Function to post Hot_Stacking data to the local web app

def post_Hot_Stacking_data_to_cloud(event_id, data_values):
    current_datetime = get_current_datetime()
    payload = {
        "did": "NAVTATblrMachine1",
        "eid": event_id,
        "cid": "1",
        "dt": current_datetime,
        "einfo": {"e1": data_values} if data_values is not None else {}
    }
    print(f"Current Date and Time: {current_datetime}")
    print(f"Data to post: {payload}")
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(url_event, headers=headers, json=payload)
        response.raise_for_status()
        print("Hot_Stacking Data posted to local web app successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to post Hot_Stacking data to '{url_event}'. Error: {e}\n{response.text if 'response' in locals() else ''}")

# Function to post Wedge_Inserter data to the local web app

def post_Wedge_Inserter_data_to_cloud(event_id, data_values):
    current_datetime = get_current_datetime()
    payload = {
        "did": "NAVTATblrMachine1",
        "eid": event_id,
        "cid": "1",
        "dt": current_datetime,
        "einfo": {"e1": data_values} if data_values is not None else {}
    }
    print(f"Current Date and Time: {current_datetime}")
    print(f"Data to post: {payload}")
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(url_event, headers=headers, json=payload)
        response.raise_for_status()
        print("Wedge_Inserter Data posted to local web app successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to post Wedge_Inserter data to '{url_event}'. Error: {e}\n{response.text if 'response' in locals() else ''}")

# Function to post data to your own cloud server
def post_data_to_my_cloud(event_id, data_values, machine_type):
    current_datetime = get_current_datetime()
    payload = {
        "did": "NAVTATblrMachine1",
        "eid": event_id,
        "cid": "1",
        "dt": current_datetime,
        "machine_type": machine_type,  # Add machine type for better organization
        "einfo": {"e1": data_values} if data_values is not None else {}
    }
    print(f"Current Date and Time: {current_datetime}")
    print(f"Data to post to cloud: {payload}")
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(url_my_cloud, headers=headers, json=payload)
        response.raise_for_status()
        print(f"{machine_type} Data posted to cloud server successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to post {machine_type} data to cloud server '{url_my_cloud}'. Error: {e}\n{response.text if 'response' in locals() else ''}")
            


# Alarm bit check

def check_changed_bits(previous_value, current_value):
    changed_bits = []
    for i in range(16):
        previous_bit = (previous_value >> i) & 1
        current_bit = (current_value >> i) & 1
        if previous_bit != current_bit:
            changed_bits.append(i)
    return changed_bits

# Line Data Collection and Posting it in LeanWorks Platform

def cimtrix_line_data_winding():
    global winding_previous_data
    global winding_previous_data1
    global winding_ar1_previous_value
    global winding_ar1_current_value
    global slot_inserter_previous_data
    global slot_inserter_previous_data1
    global slot_inserter_previous_value
    global slot_inserter_current_value
    global Hot_Stacking_previous_data
    global Hot_Stacking_previous_data1
    global Hot_Stacking_previous_value
    global Hot_Stacking_current_value
    global Wedge_Inserter_previous_data
    global Wedge_Inserter_previous_data1
    global Wedge_Inserter_previous_value
    global Wedge_Inserter_current_value
      

    while True:
        winding_data_1 = fetch_winding_values_1()
        time.sleep(0.05)
        winding_data_2 = fetch_winding_values_2()
        time.sleep(0.05)
        winding_data_3 = fetch_winding_values_3()
        time.sleep(0.05)
        winding_data_4 = fetch_winding_values_4()
        time.sleep(0.05)
        winding_data = []
        if winding_data_1 is not None:
            winding_data.extend(winding_data_1)
            print(f"Register 6707 Value: {winding_data_1[0]}")
        if winding_data_2 is not None:
            winding_data.extend(winding_data_2)
            print(f"Register 6351 Value: {winding_data_2[0]}")
        if winding_data_3 is not None:
            winding_data.extend(winding_data_3)
        if winding_data_4 is not None:
            if isinstance(winding_data_4, list):
                winding_data.extend(winding_data_4)
            else:
                winding_data.append(winding_data_4)
        print("winding_Data ", winding_data)

        if len(winding_data) >= 2 and winding_data[1] is not None and winding_previous_data1 is not None and winding_data[1] != winding_previous_data1:
            if winding_data[1] == 0:
                post_winding_data_to_cloud(event_id=70, data_values=winding_data)
                post_data_to_my_cloud(event_id=70, data_values=winding_data, machine_type="winding")
            elif winding_data[1] == 2048:
                post_winding_data_to_cloud(event_id=71, data_values=winding_data)
                post_data_to_my_cloud(event_id=71, data_values=winding_data, machine_type="winding")
            else:
                print("Unknown value for winding cycle start/stop")
            winding_previous_data1 = winding_data[1]

        if len(winding_data) >= 3 and winding_data[2] is not None:
            winding_ar1_current_value = winding_data[2]
            changed_bits = check_changed_bits(winding_ar1_previous_value, winding_ar1_current_value)
            print("winding Previous Alarm Value:", winding_ar1_previous_value)
            print("winding Current Alarm Value:", winding_ar1_current_value)
            print("winding Changed Alarm Bits:", changed_bits)

            winding_alarm_reg1 = ["EMERGENCY STOP IS PRESSED", "AIR PRESSURE NOT OK", "RT FLYER NOT READY", "LT FLYER NOT READY","INDEXER NOT READY", "MODULES NOT READY", "R TENSNR NOT READY", "L TENSNR NOT READY","RT WIRE CUT", "LT WIRE CUT", "COLLET NOT CLOSE", "COLLET NOT OPEN","RT JAW NOT OPEN", "RT JAW NOT CLOSE", "LT JAW NOT OPEN", "LT JAW NOT CLOSE"]
            winding_alarm_reg2 = ["OS NOT EXT", "OS NOT RET", "GSLV NOT EXT", "GSLV NOT RET","RT HOOK PLT NOT EXT", "RT HOOK PLT NOT RET", "LT HOOK PLT NOT EXT", "LT HOOK PLT NOT RET","DOOR NOT CLOSED", "DOOR NOT OPENED", "R TOP CUT NOT EXT", "R TOP CUT NOT RET","L BOT CUT NOT EXT", "L BOT CUT NOT RET", "L TOP CUT NOT EXT", "L TOP CUT NOT RET"]
            winding_alarm_reg3 = ["R BOT CUT NOT EXT", "R BOT CUT NOT RET", "THIMBLE NOT EXT", "THIMBLE NOT RET","LIGHT CURTAIN INTERRUPTED", "REV INDEX NOT BLOCKED", "LOADER AXIS NOT READY", "LOADER NOT HOMED","CRADLE NOT UP", "CRADLE NOT DOWN", "RT COLLET NOT OPEN", "RT COLLET NOT CLOSE","LT COLLET NOT OPEN", "LT COLLET NOT CLOSE", "RT COLLET NOT EXT", "RT COLLET NOT RET"]
            winding_alarm_reg4 = ["LT COLLET NOT EXT", "LT COLLET NOT RET", "SLIDE NOT EXT", "SLIDE NOT RET","RH LIFT NOT UP", "RH LIFT NOT DOWN", "LH LIFT NOT UP", "LH LIFT NOT DOWN","LOAD ARMATURE", "CONVEYOR FULL", "L MOTOR POS NOT IN -4 TO -16 DEG", "COMPONENT REJECTED","REJCETION BIN FULL", "LOADER NOT IN SAFE POS", "FORM NOT EXT", "FORM NOT RET"]
            winding_alarm_reg5 = ["MANUAL LOADER NOT RET", "SELECT LESS INDEX FOR 1:2", "CONVEYOR EMPTY","FLYER / INDEXER NOT HOMED", "FLYER NOT MOVING", "FLYER POS NOT COMPLETED","INDEXER NOT MOVING", "INDEXER POS NOT COMPLETED", "MASTER NOT READY","MASTER COMMUNICATION ERROR", "MACHINE INSTABLE", "winding75","SAFE GUARD NOT CLOSE", "TOP GRIPPER ASSEMBLY NOT EXT", "TOP GRIPPER ASSEMBLY NOT RET","BOT GRIPPER ASSEMBLY NOT EXT"]
            winding_alarm_reg6 = ["BOT GRIPPER ASSEMBLY NOT RET","TOP HOOK BEND CYL NOT EXT", "TOP HOOK BEND CYL NOT RET", "BOT HOOK BEND CYL NOT EXT","BOT HOOK BEND CYL NOT RET", "GRIPPER NOT EXT", "GRIPPER NOT RET", "NA", "Message exixts", "Homed Once", "NA", "CLT CLS SW", "L I Home start", "CW/CCW", "H L Index Jog +", "H L Index Jog -"]

            if changed_bits:
                alarm_registers = [winding_alarm_reg1, winding_alarm_reg2, winding_alarm_reg3, winding_alarm_reg4, winding_alarm_reg5, winding_alarm_reg6]
                alarm_start_indices = [0, 16, 32, 48, 64, 80] # Corresponding bit start for each register

                for bit in changed_bits:
                    register_index = bit // 16
                    bit_in_register = bit % 16
                    if register_index < len(alarm_registers) and bit_in_register < len(alarm_registers[register_index]):
                        post_winding_data_to_cloud(event_id=45, data_values=alarm_registers[register_index][bit_in_register])

            if winding_ar1_current_value == 0 and winding_ar1_current_value != winding_ar1_previous_value:
                post_winding_data_to_cloud(event_id=46, data_values="Alarm Released")

            winding_ar1_previous_value = winding_ar1_current_value

        if len(winding_data) >= 1 and winding_data[0] is not None and winding_previous_data is not None and winding_data[0] != winding_previous_data:
            if winding_data[0] == 2048:
                extended_values = fetch_winding_values_4()
                post_winding_data_to_cloud(event_id=401, data_values=extended_values)
            winding_previous_data = winding_data[0]
            
        slot_inserter_data_1 = fetch_slot_inserter_values_1()
        time.sleep(0.05)
        slot_inserter_data_2 = fetch_slot_inserter_values_2()
        time.sleep(0.05)
        slot_inserter_data_3 = fetch_slot_inserter_values_3()
        time.sleep(0.05)
        slot_inserter_data_4 = fetch_slot_inserter_values_4()
        time.sleep(0.05)
        slot_inserter_data = []
        if slot_inserter_data_1 is not None:
            slot_inserter_data.extend(slot_inserter_data_1)
            print(f"Register 6707 Value: {slot_inserter_data_1[0]}")
        if slot_inserter_data_2 is not None:
            slot_inserter_data.extend(slot_inserter_data_2)
            print(f"Register 6351 Value: {slot_inserter_data_2[0]}")
        if slot_inserter_data_3 is not None:
            slot_inserter_data.extend(slot_inserter_data_3)
        if slot_inserter_data_4 is not None:
            if isinstance(slot_inserter_data_4, list):
                slot_inserter_data.extend(slot_inserter_data_4)
            else:
                slot_inserter_data.append(slot_inserter_data_4)
        print("slot_inserter_Data ", slot_inserter_data)

        if len(slot_inserter_data) >= 2 and slot_inserter_data[1] is not None and slot_inserter_previous_data1 is not None and slot_inserter_data[1] != slot_inserter_previous_data1:
            if slot_inserter_data[1] == 0:
                post_slot_inserter_data_to_cloud(event_id=70, data_values=slot_inserter_data)
            elif slot_inserter_data[1] == 2048:
                post_slot_inserter_data_to_cloud(event_id=71, data_values=slot_inserter_data)
            else:
                print("Unknown value for slot_inserter cycle start/stop")
            slot_inserter_previous_data1 = slot_inserter_data[1]

        if len(slot_inserter_data) >= 3 and slot_inserter_data[2] is not None:
            slot_inserter_ar1_current_value = slot_inserter_data[2]
            changed_bits = check_changed_bits(slot_inserter_previous_value, slot_inserter_ar1_current_value)
            print("slot_inserter Previous Alarm Value:", slot_inserter_previous_value)
            print("slot_inserter Current Alarm Value:", slot_inserter_current_value)
            print("slot_inserter Changed Alarm Bits:", changed_bits)

            slot_inserter_alarm_reg1 = ["EMERGENCY STOP IS PRESSED", "AIR PRESSURE NOT OK", "RT FLYER NOT READY", "LT FLYER NOT READY","INDEXER NOT READY", "MODULES NOT READY", "R TENSNR NOT READY", "L TENSNR NOT READY","RT WIRE CUT", "LT WIRE CUT", "COLLET NOT CLOSE", "COLLET NOT OPEN","RT JAW NOT OPEN", "RT JAW NOT CLOSE", "LT JAW NOT OPEN", "LT JAW NOT CLOSE"]
            slot_inserter_alarm_reg2 = ["OS NOT EXT", "OS NOT RET", "GSLV NOT EXT", "GSLV NOT RET","RT HOOK PLT NOT EXT", "RT HOOK PLT NOT RET", "LT HOOK PLT NOT EXT", "LT HOOK PLT NOT RET","DOOR NOT CLOSED", "DOOR NOT OPENED", "R TOP CUT NOT EXT", "R TOP CUT NOT RET","L BOT CUT NOT EXT", "L BOT CUT NOT RET", "L TOP CUT NOT EXT", "L TOP CUT NOT RET"]
            slot_inserter_alarm_reg3 = ["R BOT CUT NOT EXT", "R BOT CUT NOT RET", "THIMBLE NOT EXT", "THIMBLE NOT RET","LIGHT CURTAIN INTERRUPTED", "REV INDEX NOT BLOCKED", "LOADER AXIS NOT READY", "LOADER NOT HOMED","CRADLE NOT UP", "CRADLE NOT DOWN", "RT COLLET NOT OPEN", "RT COLLET NOT CLOSE","LT COLLET NOT OPEN", "LT COLLET NOT CLOSE", "RT COLLET NOT EXT", "RT COLLET NOT RET"]
            slot_inserter_alarm_reg4 = ["LT COLLET NOT EXT", "LT COLLET NOT RET", "SLIDE NOT EXT", "SLIDE NOT RET","RH LIFT NOT UP", "RH LIFT NOT DOWN", "LH LIFT NOT UP", "LH LIFT NOT DOWN","LOAD ARMATURE", "CONVEYOR FULL", "L MOTOR POS NOT IN -4 TO -16 DEG", "COMPONENT REJECTED","REJCETION BIN FULL", "LOADER NOT IN SAFE POS", "FORM NOT EXT", "FORM NOT RET"]
            slot_inserter_alarm_reg5 = ["MANUAL LOADER NOT RET", "SELECT LESS INDEX FOR 1:2", "CONVEYOR EMPTY","FLYER / INDEXER NOT HOMED", "FLYER NOT MOVING", "FLYER POS NOT COMPLETED","INDEXER NOT MOVING", "INDEXER POS NOT COMPLETED", "MASTER NOT READY","MASTER COMMUNICATION ERROR", "MACHINE INSTABLE", "slot_inserter75","SAFE GUARD NOT CLOSE", "TOP GRIPPER ASSEMBLY NOT EXT", "TOP GRIPPER ASSEMBLY NOT RET","BOT GRIPPER ASSEMBLY NOT EXT"]
            slot_inserter_alarm_reg6 = ["BOT GRIPPER ASSEMBLY NOT RET","TOP HOOK BEND CYL NOT EXT", "TOP HOOK BEND CYL NOT RET", "BOT HOOK BEND CYL NOT EXT","BOT HOOK BEND CYL NOT RET", "GRIPPER NOT EXT", "GRIPPER NOT RET", "NA", "Message exixts", "Homed Once", "NA", "CLT CLS SW", "L I Home start", "CW/CCW", "H L Index Jog +", "H L Index Jog -"]

            if changed_bits:
                alarm_registers = [slot_inserter_alarm_reg1, slot_inserter_alarm_reg2, slot_inserter_alarm_reg3, slot_inserter_alarm_reg4, slot_inserter_alarm_reg5, slot_inserter_alarm_reg6]
                alarm_start_indices = [0, 16, 32, 48, 64, 80] # Corresponding bit start for each register

                for bit in changed_bits:
                    register_index = bit // 16
                    bit_in_register = bit % 16
                    if register_index < len(alarm_registers) and bit_in_register < len(alarm_registers[register_index]):
                        post_slot_inserter_data_to_cloud(event_id=45, data_values=alarm_registers[register_index][bit_in_register])

            if slot_inserter_ar1_current_value == 0 and slot_inserter_ar1_current_value != slot_inserter_previous_value:
                post_slot_inserter_data_to_cloud(event_id=46, data_values="Alarm Released")

            slot_inserter_previous_value = slot_inserter_ar1_current_value

        if len(slot_inserter_data) >= 1 and slot_inserter_data[0] is not None and slot_inserter_previous_data is not None and slot_inserter_data[0] != slot_inserter_previous_data:
            if slot_inserter_data[0] == 2048:
                extended_values = fetch_slot_inserter_values_4()
                post_slot_inserter_data_to_cloud(event_id=401, data_values=extended_values)
            slot_inserter_previous_data = slot_inserter_data[0]

        Hot_Stacking_data_1 = fetch_Hot_Stacking_values_1()
        time.sleep(0.05)
        Hot_Stacking_data_2 = fetch_Hot_Stacking_values_2()
        time.sleep(0.05)
        Hot_Stacking_data_3 = fetch_Hot_Stacking_values_3()
        time.sleep(0.05)
        Hot_Stacking_data_4 = fetch_Hot_Stacking_values_4()
        time.sleep(0.05)
        Hot_Stacking_data = []
        if Hot_Stacking_data_1 is not None:
            Hot_Stacking_data.extend(Hot_Stacking_data_1)
            print(f"Register 6707 Value: {Hot_Stacking_data_1[0]}")
        if Hot_Stacking_data_2 is not None:
            Hot_Stacking_data.extend(Hot_Stacking_data_2)
            print(f"Register 6351 Value: {Hot_Stacking_data_2[0]}")
        if Hot_Stacking_data_3 is not None:
            Hot_Stacking_data.extend(Hot_Stacking_data_3)
        if Hot_Stacking_data_4 is not None:
            if isinstance(Hot_Stacking_data_4, list):
                Hot_Stacking_data.extend(Hot_Stacking_data_4)
            else:
                Hot_Stacking_data.append(Hot_Stacking_data_4)
        print("Hot_Stacking_Data ", Hot_Stacking_data)

        if len(Hot_Stacking_data) >= 2 and Hot_Stacking_data[1] is not None and Hot_Stacking_previous_data1 is not None and Hot_Stacking_data[1] != Hot_Stacking_previous_data1:
            if Hot_Stacking_data[1] == 0:
                post_Hot_Stacking_data_to_cloud(event_id=70, data_values=Hot_Stacking_data)
            elif Hot_Stacking_data[1] == 2048:
                post_Hot_Stacking_data_to_cloud(event_id=71, data_values=Hot_Stacking_data)
            else:
                print("Unknown value for Hot_Stacking cycle start/stop")
            Hot_Stacking_previous_data1 = Hot_Stacking_data[1]

        if len(Hot_Stacking_data) >= 3 and Hot_Stacking_data[2] is not None:
            Hot_Stacking_ar1_current_value = Hot_Stacking_data[2]
            changed_bits = check_changed_bits(Hot_Stacking_previous_value, Hot_Stacking_ar1_current_value)
            print("Hot_Stacking Previous Alarm Value:", Hot_Stacking_previous_value)
            print("Hot_Stacking Current Alarm Value:", Hot_Stacking_current_value)
            print("Hot_Stacking Changed Alarm Bits:", changed_bits)

            Hot_Stacking_alarm_reg1 = ["EMERGENCY STOP IS PRESSED", "AIR PRESSURE NOT OK", "RT FLYER NOT READY", "LT FLYER NOT READY","INDEXER NOT READY", "MODULES NOT READY", "R TENSNR NOT READY", "L TENSNR NOT READY","RT WIRE CUT", "LT WIRE CUT", "COLLET NOT CLOSE", "COLLET NOT OPEN","RT JAW NOT OPEN", "RT JAW NOT CLOSE", "LT JAW NOT OPEN", "LT JAW NOT CLOSE"]
            Hot_Stacking_alarm_reg2 = ["OS NOT EXT", "OS NOT RET", "GSLV NOT EXT", "GSLV NOT RET","RT HOOK PLT NOT EXT", "RT HOOK PLT NOT RET", "LT HOOK PLT NOT EXT", "LT HOOK PLT NOT RET","DOOR NOT CLOSED", "DOOR NOT OPENED", "R TOP CUT NOT EXT", "R TOP CUT NOT RET","L BOT CUT NOT EXT", "L BOT CUT NOT RET", "L TOP CUT NOT EXT", "L TOP CUT NOT RET"]
            Hot_Stacking_alarm_reg3 = ["R BOT CUT NOT EXT", "R BOT CUT NOT RET", "THIMBLE NOT EXT", "THIMBLE NOT RET","LIGHT CURTAIN INTERRUPTED", "REV INDEX NOT BLOCKED", "LOADER AXIS NOT READY", "LOADER NOT HOMED","CRADLE NOT UP", "CRADLE NOT DOWN", "RT COLLET NOT OPEN", "RT COLLET NOT CLOSE","LT COLLET NOT OPEN", "LT COLLET NOT CLOSE", "RT COLLET NOT EXT", "RT COLLET NOT RET"]
            Hot_Stacking_alarm_reg4 = ["LT COLLET NOT EXT", "LT COLLET NOT RET", "SLIDE NOT EXT", "SLIDE NOT RET","RH LIFT NOT UP", "RH LIFT NOT DOWN", "LH LIFT NOT UP", "LH LIFT NOT DOWN","LOAD ARMATURE", "CONVEYOR FULL", "L MOTOR POS NOT IN -4 TO -16 DEG", "COMPONENT REJECTED","REJCETION BIN FULL", "LOADER NOT IN SAFE POS", "FORM NOT EXT", "FORM NOT RET"]
            Hot_Stacking_alarm_reg5 = ["MANUAL LOADER NOT RET", "SELECT LESS INDEX FOR 1:2", "CONVEYOR EMPTY","FLYER / INDEXER NOT HOMED", "FLYER NOT MOVING", "FLYER POS NOT COMPLETED","INDEXER NOT MOVING", "INDEXER POS NOT COMPLETED", "MASTER NOT READY","MASTER COMMUNICATION ERROR", "MACHINE INSTABLE", "Hot_Stacking75","SAFE GUARD NOT CLOSE", "TOP GRIPPER ASSEMBLY NOT EXT", "TOP GRIPPER ASSEMBLY NOT RET","BOT GRIPPER ASSEMBLY NOT EXT"]
            Hot_Stacking_alarm_reg6 = ["BOT GRIPPER ASSEMBLY NOT RET","TOP HOOK BEND CYL NOT EXT", "TOP HOOK BEND CYL NOT RET", "BOT HOOK BEND CYL NOT EXT","BOT HOOK BEND CYL NOT RET", "GRIPPER NOT EXT", "GRIPPER NOT RET", "NA", "Message exixts", "Homed Once", "NA", "CLT CLS SW", "L I Home start", "CW/CCW", "H L Index Jog +", "H L Index Jog -"]

            if changed_bits:
                alarm_registers = [Hot_Stacking_alarm_reg1, Hot_Stacking_alarm_reg2, Hot_Stacking_alarm_reg3, Hot_Stacking_alarm_reg4, Hot_Stacking_alarm_reg5, Hot_Stacking_alarm_reg6]
                alarm_start_indices = [0, 16, 32, 48, 64, 80] # Corresponding bit start for each register

                for bit in changed_bits:
                    register_index = bit // 16
                    bit_in_register = bit % 16
                    if register_index < len(alarm_registers) and bit_in_register < len(alarm_registers[register_index]):
                        post_Hot_Stacking_data_to_cloud(event_id=45, data_values=alarm_registers[register_index][bit_in_register])

            if Hot_Stacking_ar1_current_value == 0 and Hot_Stacking_ar1_current_value != Hot_Stacking_previous_value:
                post_Hot_Stacking_data_to_cloud(event_id=46, data_values="Alarm Released")

            Hot_Stacking_previous_value = Hot_Stacking_ar1_current_value

        if len(Hot_Stacking_data) >= 1 and Hot_Stacking_data[0] is not None and Hot_Stacking_previous_data is not None and Hot_Stacking_data[0] != Hot_Stacking_previous_data:
            if Hot_Stacking_data[0] == 2048:
                extended_values = fetch_Hot_Stacking_values_4()
                post_Hot_Stacking_data_to_cloud(event_id=401, data_values=extended_values)
            Hot_Stacking_previous_data = Hot_Stacking_data[0]

        Wedge_Inserter_data_1 = fetch_Wedge_Inserter_values_1()
        time.sleep(0.05)
        Wedge_Inserter_data_2 = fetch_Wedge_Inserter_values_2()
        time.sleep(0.05)
        Wedge_Inserter_data_3 = fetch_Wedge_Inserter_values_3()
        time.sleep(0.05)
        Wedge_Inserter_data_4 = fetch_Wedge_Inserter_values_4()
        time.sleep(0.05)
        Wedge_Inserter_data = []
        if Wedge_Inserter_data_1 is not None:
            Wedge_Inserter_data.extend(Wedge_Inserter_data_1)
            print(f"Register 6707 Value: {Wedge_Inserter_data_1[0]}")
        if Wedge_Inserter_data_2 is not None:
            Wedge_Inserter_data.extend(Wedge_Inserter_data_2)
            print(f"Register 6351 Value: {Wedge_Inserter_data_2[0]}")
        if Wedge_Inserter_data_3 is not None:
            Wedge_Inserter_data.extend(Wedge_Inserter_data_3)
        if Wedge_Inserter_data_4 is not None:
            if isinstance(Wedge_Inserter_data_4, list):
                Wedge_Inserter_data.extend(Wedge_Inserter_data_4)
            else:
                Wedge_Inserter_data.append(Wedge_Inserter_data_4)
        print("Wedge_Inserter_Data ", Wedge_Inserter_data)

        if len(Wedge_Inserter_data) >= 2 and Wedge_Inserter_data[1] is not None and Wedge_Inserter_previous_data1 is not None and Wedge_Inserter_data[1] != Wedge_Inserter_previous_data1:
            if Wedge_Inserter_data[1] == 0:
                post_Wedge_Inserter_data_to_cloud(event_id=70, data_values=Wedge_Inserter_data)
            elif Wedge_Inserter_data[1] == 2048:
                post_Wedge_Inserter_data_to_cloud(event_id=71, data_values=Wedge_Inserter_data)
            else:
                print("Unknown value for Wedge_Inserter cycle start/stop")
            Wedge_Inserter_previous_data1 = Wedge_Inserter_data[1]

        if len(Wedge_Inserter_data) >= 3 and Wedge_Inserter_data[2] is not None:
            Wedge_Inserter_ar1_current_value = Wedge_Inserter_data[2]
            changed_bits = check_changed_bits(Wedge_Inserter_previous_value, Wedge_Inserter_ar1_current_value)
            print("Wedge_Inserter Previous Alarm Value:", Wedge_Inserter_previous_value)
            print("Wedge_Inserter Current Alarm Value:", Wedge_Inserter_current_value)
            print("Wedge_Inserter Changed Alarm Bits:", changed_bits)

            Wedge_Inserter_alarm_reg1 = ["EMERGENCY STOP IS PRESSED", "AIR PRESSURE NOT OK", "RT FLYER NOT READY", "LT FLYER NOT READY","INDEXER NOT READY", "MODULES NOT READY", "R TENSNR NOT READY", "L TENSNR NOT READY","RT WIRE CUT", "LT WIRE CUT", "COLLET NOT CLOSE", "COLLET NOT OPEN","RT JAW NOT OPEN", "RT JAW NOT CLOSE", "LT JAW NOT OPEN", "LT JAW NOT CLOSE"]
            Wedge_Inserter_alarm_reg2 = ["OS NOT EXT", "OS NOT RET", "GSLV NOT EXT", "GSLV NOT RET","RT HOOK PLT NOT EXT", "RT HOOK PLT NOT RET", "LT HOOK PLT NOT EXT", "LT HOOK PLT NOT RET","DOOR NOT CLOSED", "DOOR NOT OPENED", "R TOP CUT NOT EXT", "R TOP CUT NOT RET","L BOT CUT NOT EXT", "L BOT CUT NOT RET", "L TOP CUT NOT EXT", "L TOP CUT NOT RET"]
            Wedge_Inserter_alarm_reg3 = ["R BOT CUT NOT EXT", "R BOT CUT NOT RET", "THIMBLE NOT EXT", "THIMBLE NOT RET","LIGHT CURTAIN INTERRUPTED", "REV INDEX NOT BLOCKED", "LOADER AXIS NOT READY", "LOADER NOT HOMED","CRADLE NOT UP", "CRADLE NOT DOWN", "RT COLLET NOT OPEN", "RT COLLET NOT CLOSE","LT COLLET NOT OPEN", "LT COLLET NOT CLOSE", "RT COLLET NOT EXT", "RT COLLET NOT RET"]
            Wedge_Inserter_alarm_reg4 = ["LT COLLET NOT EXT", "LT COLLET NOT RET", "SLIDE NOT EXT", "SLIDE NOT RET","RH LIFT NOT UP", "RH LIFT NOT DOWN", "LH LIFT NOT UP", "LH LIFT NOT DOWN","LOAD ARMATURE", "CONVEYOR FULL", "L MOTOR POS NOT IN -4 TO -16 DEG", "COMPONENT REJECTED","REJCETION BIN FULL", "LOADER NOT IN SAFE POS", "FORM NOT EXT", "FORM NOT RET"]
            Wedge_Inserter_alarm_reg5 = ["MANUAL LOADER NOT RET", "SELECT LESS INDEX FOR 1:2", "CONVEYOR EMPTY","FLYER / INDEXER NOT HOMED", "FLYER NOT MOVING", "FLYER POS NOT COMPLETED","INDEXER NOT MOVING", "INDEXER POS NOT COMPLETED", "MASTER NOT READY","MASTER COMMUNICATION ERROR", "MACHINE INSTABLE", "Wedge_Inserter75","SAFE GUARD NOT CLOSE", "TOP GRIPPER ASSEMBLY NOT EXT", "TOP GRIPPER ASSEMBLY NOT RET","BOT GRIPPER ASSEMBLY NOT EXT"]
            Wedge_Inserter_alarm_reg6 = ["BOT GRIPPER ASSEMBLY NOT RET","TOP HOOK BEND CYL NOT EXT", "TOP HOOK BEND CYL NOT RET", "BOT HOOK BEND CYL NOT EXT","BOT HOOK BEND CYL NOT RET", "GRIPPER NOT EXT", "GRIPPER NOT RET", "NA", "Message exixts", "Homed Once", "NA", "CLT CLS SW", "L I Home start", "CW/CCW", "H L Index Jog +", "H L Index Jog -"]

            if changed_bits:
                alarm_registers = [Wedge_Inserter_alarm_reg1, Wedge_Inserter_alarm_reg2, Wedge_Inserter_alarm_reg3, Wedge_Inserter_alarm_reg4, Wedge_Inserter_alarm_reg5, Wedge_Inserter_alarm_reg6]
                alarm_start_indices = [0, 16, 32, 48, 64, 80] # Corresponding bit start for each register

                for bit in changed_bits:
                    register_index = bit // 16
                    bit_in_register = bit % 16
                    if register_index < len(alarm_registers) and bit_in_register < len(alarm_registers[register_index]):
                        post_Wedge_Inserter_data_to_cloud(event_id=45, data_values=alarm_registers[register_index][bit_in_register])

            if Wedge_Inserter_ar1_current_value == 0 and Wedge_Inserter_ar1_current_value != Wedge_Inserter_previous_value:
                post_Wedge_Inserter_data_to_cloud(event_id=46, data_values="Alarm Released")

            Wedge_Inserter_previous_value = Wedge_Inserter_ar1_current_value

        if len(Wedge_Inserter_data) >= 1 and Wedge_Inserter_data[0] is not None and Wedge_Inserter_previous_data is not None and Wedge_Inserter_data[0] != Wedge_Inserter_previous_data:
            if Wedge_Inserter_data[0] == 2048:
                extended_values = fetch_Wedge_Inserter_values_4()
                post_Wedge_Inserter_data_to_cloud(event_id=401, data_values=extended_values)
            Wedge_Inserter_previous_data = Wedge_Inserter_data[0]
        
        time.sleep(1) # Adjust sleep time as needed

if __name__ == "__main__":
    cimtrix_line_data_winding()