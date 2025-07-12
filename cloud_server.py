from flask import Flask, request, jsonify
from datetime import datetime
import json
import sqlite3
import os

app = Flask(__name__)

# Initialize database when app starts
def init_db():
    # Use /tmp for cloud deployment, local directory for development
    import os
    if os.environ.get('GAE_ENV', '').startswith('standard'):
        # Running on Google App Engine
        db_path = '/tmp/machine_data.db'
    else:
        # Running locally
        db_path = 'machine_data.db'
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS machine_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT,
            event_id INTEGER,
            machine_type TEXT,
            timestamp TEXT,
            data_values TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Initialize database immediately
init_db()

@app.route('/api/receive_machine_data', methods=['POST'])
def receive_machine_data():
    try:
        data = request.get_json()
        
        # Store in database
        # Use /tmp for cloud deployment, local directory for development
        import os
        if os.environ.get('GAE_ENV', '').startswith('standard'):
            # Running on Google App Engine
            db_path = '/tmp/machine_data.db'
        else:
            # Running locally
            db_path = 'machine_data.db'
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO machine_events (device_id, event_id, machine_type, timestamp, data_values)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            data.get('did'),
            data.get('eid'),
            data.get('machine_type', 'unknown'),
            data.get('dt'),
            json.dumps(data.get('einfo', {}))
        ))
        conn.commit()
        conn.close()
        
        print(f"Received data: {data}")
        return jsonify({"status": "success", "message": "Data received"}), 200
        
    except Exception as e:
        print(f"Error processing data: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/machine_data', methods=['GET'])
def get_machine_data():
    try:
        # Use /tmp for cloud deployment, local directory for development
        import os
        if os.environ.get('GAE_ENV', '').startswith('standard'):
            # Running on Google App Engine
            db_path = '/tmp/machine_data.db'
        else:
            # Running locally
            db_path = 'machine_data.db'
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM machine_events ORDER BY created_at DESC LIMIT 100')
        rows = cursor.fetchall()
        conn.close()
        
        data = []
        for row in rows:
            data.append({
                'id': row[0],
                'device_id': row[1],
                'event_id': row[2],
                'machine_type': row[3],
                'timestamp': row[4],
                'data_values': json.loads(row[5]) if row[5] else {},
                'created_at': row[6]
            })
        
        return jsonify({"status": "success", "data": data}), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/')
def home():
    return '''
    <h1>Machine Data Cloud Server</h1>
    <p>This server receives machine data from your Modbus monitoring script.</p>
    <ul>
        <li><a href="/api/machine_data">View Recent Data</a></li>
    </ul>
    '''

if __name__ == '__main__':
    init_db()
    # For production, use a proper WSGI server like gunicorn
    # Cloud Run will use the PORT environment variable
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False) 