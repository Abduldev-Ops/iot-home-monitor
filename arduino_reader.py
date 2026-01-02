from serial import Serial, SerialException
import time
from datetime import datetime
import database
import serial.tools.list_ports

SERIAL_PORT = 'COM4'  
BAUD_RATE = 9600
TIMEOUT = 2

latest_reading = {
    'timestamp': '--',
    'temperature': 0.0,
    'humidity': 0.0,
    'motion': False
}

def find_arduino_port():
    
    import serial.tools.list_ports
    
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if 'Arduino' in port.description or 'USB' in port.description:
            print(f"✅ Found Arduino on port: {port.device}")
            return port.device
    
    return None

def connect_arduino(port=None): 
    if port is None:
        port = find_arduino_port()
        if port is None:
            print("Could not find Arduino automatically.")
            print("Available ports:")
            
            for p in serial.tools.list_ports.comports():
                print(f"  - {p.device}: {p.description}")
            return None
    
    try:
        ser = serial.Serial(port, BAUD_RATE, timeout=TIMEOUT)
        time.sleep(2) 
        print(f"✅ Connected to Arduino on {port}")
        
       
        ser.reset_input_buffer()
        
        return ser
    except serial.SerialException as e:
        print(f"Failed to connect to Arduino: {e}")
        return None

def parse_arduino_data(line):
    
    try:
        parts = line.strip().split(',')
        if len(parts) != 3:
            return None
        
        temperature = float(parts[0])
        humidity = float(parts[1])
        motion = parts[2].lower() == 'true'
        
        return {
            'temperature': temperature,
            'humidity': humidity,
            'motion': motion
        }
    except (ValueError, IndexError) as e:
        print(f"Failed to parse data: {line} | Error: {e}")
        return None

def read_arduino_continuous(port=None):
    
    global latest_reading
    
    
    db = database.SensorDatabase()
    
   
    ser = connect_arduino(port)
    if not ser:
        print("Cannot start - Arduino not connected")
        return
    
    print("Reading from Arduino...")
    print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            if ser.in_waiting > 0:
                try:
                    line = ser.readline().decode('utf-8').strip()
                    
                    
                    if not line or line.startswith('Arduino'):
                        continue
                    
                    
                    data = parse_arduino_data(line)
                    if data:
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        
                        latest_reading = {
                            'timestamp': timestamp,
                            'temperature': data['temperature'],
                            'humidity': data['humidity'],
                            'motion': data['motion']
                        }
                        
                        
                        db.insert_readings(
                            timestamp,
                            data['temperature'],
                            data['humidity'],
                            data['motion']
                        )
                        
                       
                        motion_status = "Motion Detected" if data['motion'] else "No Motion"
                        print(f"[{timestamp}] Temp: {data['temperature']:.1f}°C | "
                              f"Humidity: {data['humidity']:.1f}% | {motion_status}")
                        print(f"✅ Saved to database")
                    
                except UnicodeDecodeError:
                    continue
                except Exception as e:
                    print(f" Error reading data: {e}")
                    continue
            
            time.sleep(0.2) 
    
    except KeyboardInterrupt:
        print("\n\nStopping Arduino reader...")
        ser.close()
        print(" Disconnected from Arduino")

def get_latest_reading():
    """Get the most recent reading from Arduino"""
    return latest_reading

def main():
    """Main function to run Arduino reader"""
    import sys
    
    # Check if port was provided as argument
    port = sys.argv[1] if len(sys.argv) > 1 else None
    
    if port:
        print(f"Using specified port: {port}")
    else:
        print("No port specified. Will try to auto-detect Arduino...")
    
    read_arduino_continuous(port)

if __name__ == "__main__":
    main()