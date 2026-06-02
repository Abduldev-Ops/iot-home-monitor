from flask import Flask, render_template, jsonify, abort, redirect, url_for
from flask_cors import CORS
import database
#import alerts
import threading
import time

app = Flask("__name__")
CORS(app)

db = database.SensorDatabase()

arduino_connected = False
arduino_thread = None

def run_arduino_reader():
    """Run Arduino reader in background thread"""
    global arduino_connected
    try:
        import arduino_reader
        print("🔌 Starting Arduino reader in background...")
        arduino_connected = True
        arduino_reader.read_arduino_continuous()
    except Exception as e:
        print(f"Arduino reader error: {e}")
        arduino_connected = False

@app.route('/api/sensor')
def sensor():
    # abort(401)
    try:
        data = db.get_latest_reading()
        if not data:
            with open('fake_sensor.csv', 'r') as file:
                header = file.readline()
                line = file.readline()
                last_line = None
                while line:
                    if line.strip():
                        last_line = line.strip()
                    line = file.readline()

            if not last_line:
                return jsonify({'error': 'No data yet!'}), 404

            parts = last_line.split(',')
            data = {
                'timestamp': parts[0].strip(),
                'temperature': float(parts[1].strip()),
                'humidity': float(parts[2].strip()),
                'motion': parts[3].strip() == 'True'
            }
        
        #alerts.check_and_alert(data['temperature'], data['humidity'], data['motion'], data['timestamp'])
        return jsonify(data)

    except FileNotFoundError:
        return jsonify({'error': 'fake_sensor.csv file not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sensor/history')
def sensor_history():
    """Get recent sensor readings for charts"""
    try:
        limit = 20
        readings = db.get_recent_readings(limit)
        return jsonify(readings)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sensor/all')
def all_sensors():
    """Get all sensor readings"""
    try:
        readings = db.get_all_readings()
        return jsonify(readings)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# @app.route('/api/alerts/settings', methods=['GET'])
# def get_alert_settings():
#     """Get current alert settings"""
#     try:
#         settings = alerts.get_alert_settings()
#         return jsonify(settings)
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/alerts/settings', methods=['POST'])
# def update_alert_settings():
#     """Update alert settings"""
#     try:
#         data = request.json
#         temp_enabled = data.get('temp_enabled', True)
#         motion_enabled = data.get('motion_enabled', True)
#         temp_threshold = data.get('temp_threshold', 35.0)
        
#         alerts.set_alert_settings(temp_enabled, motion_enabled, temp_threshold)
        
#         return jsonify({
#             'success': True,
#             'settings': alerts.get_alert_settings()
#         })
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health():
    return jsonify({'status': 'ok'})

# using app.get and app.post when doing the authentiCcation later
# https://developer.mozilla.org/en-US/


if __name__ == '__main__':  
    arduino_thread = threading.Thread(target=run_arduino_reader, daemon=True)
    arduino_thread.start()
    
    # Give Arduino reader time to connect
    time.sleep(3)
    print("\n" + "="*50)
    print("IoT Dashboard Backend Running")
    print("="*50)
    print(f"Arduino: {'Connected' if arduino_connected else 'Disconnected'}")
    print(f"Database: Initialized")
    print(f"Alerts: Enabled")
    print(f"API: http://localhost:5000")
    print("="*50 + "\n")

    app.run(debug = True, port=5000, use_reloader=False)

