# IoT Home Monitor Dashboard

A real-time IoT monitoring system that reads temperature, humidity, and motion data from Arduino sensors (or simulator) and displays them on a web dashboard with SMS alerts.

## Overview

This application is a full-stack IoT system that connects Arduino sensors to a React web interface. It stores sensor readings in a database, displays live charts, and sends SMS alerts when thresholds are exceeded. Includes a simulator mode for testing without physical hardware.

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- Twilio account (for SMS alerts)
- **Optional:** Arduino Uno with sensors (DHT11, PIR) and Arduino IDE

## Hardware Setup (Optional)

**Note:** You can run this project in **simulator mode** without any hardware. Skip to Installation if you don't have Arduino sensors.

**Required Components:**
- Arduino Uno
- DHT11 Temperature & Humidity Sensor
- PIR Motion Sensor (HC-SR501)
- Breadboard and jumper wires

**Wiring:**
```
DHT11 Sensor:
  VCC  → Arduino 5V
  GND  → Arduino GND
  DATA → Arduino Pin 2

PIR Sensor:
  VCC → Arduino 5V
  GND → Arduino GND
  OUT → Arduino Pin 7
```

## Installation

### 1. Install Python Dependencies

**For Simulator Mode (no hardware):**
```bash
pip install flask flask-cors twilio
```

**For Arduino Mode (with hardware):**
```bash
pip install flask flask-cors twilio pyserial
```

### 2. Install Frontend Dependencies

```bash
cd iot-dashboard
npm install
```

### 3. Configure Twilio (for SMS alerts)

Edit `alerts.py` and add your Twilio credentials:

```python
TWILIO_ACCOUNT_SID = "your_account_sid"
TWILIO_AUTH_TOKEN = "your_auth_token"
TWILIO_PHONE_NUMBER = "your_twilio_number"
YOUR_PHONE_NUMBER = "your_personal_number"
```

### 4. Configure Arduino Port (Arduino Mode Only)

If using real Arduino hardware, edit `arduino_reader.py` and set your Arduino's serial port:

```python
SERIAL_PORT = 'COM3'  # Windows
# SERIAL_PORT = '/dev/ttyACM0'  # Linux
# SERIAL_PORT = '/dev/tty.usbmodem14101'  # Mac
```

### 5. Upload Arduino Code (Arduino Mode Only)

1. Open Arduino IDE
2. Install DHT sensor library: Sketch → Include Library → Manage Libraries → Search "DHT sensor library" by Adafruit
3. Open the Arduino code file (`.ino`)
4. Select Board: Arduino Uno
5. Select your Arduino's port
6. Click Upload

## Running the Application

### Option 1: Simulator Mode (No Hardware Required)

**Terminal 1: Start Sensor Simulator**
```bash
python sensor_simulator.py
```

**Terminal 2: Start Backend (Flask)**
```bash
python app.py
```

**Terminal 3: Start Frontend (React)**
```bash
cd iot-dashboard
npm run dev
```

### Option 2: Arduino Mode (With Hardware)

**Terminal 1: Start Backend (Flask + Arduino Reader)**
```bash
python app.py
```
*Flask will automatically start reading from Arduino*

**Terminal 2: Start Frontend (React)**
```bash
cd iot-dashboard
npm run dev
```

### Access the Dashboard

Open your browser: **http://localhost:5173**

## Features

- **Real-time monitoring** - Live temperature, humidity, and motion data
- **Interactive charts** - Historical data visualization  
- **SMS alerts** - Get notified when temperature exceeds threshold or motion detected
- **Database storage** - All readings saved to SQLite
- **Simulator mode** - Test without physical hardware

## Project Structure

```
iot-home-monitor/
├── app.py                 # Flask backend
├── database.py            # Database operations
├── alerts.py              # SMS alert system
├── arduino_reader.py      # Arduino communication (hardware mode)
├── sensor_simulator.py    # Sensor simulator (no hardware needed)
├── sensor_data.db         # SQLite database (auto-generated)
├── fake_sensor.csv        # Simulator output file
├── iot-dashboard/         # React frontend
│   ├── src/
│   │   ├── components/
│   │   └── App.jsx
│   └── package.json
└── arduino_code/          # Arduino sensor code
```

## Switching Between Modes

### Using Simulator (Default)
The simulator generates random sensor data and saves to `fake_sensor.csv`. Flask reads from this CSV file.

### Using Real Arduino
When you run `python app.py`, it automatically detects and connects to Arduino if available. The Arduino reader runs in a background thread and writes data directly to the database.

## Troubleshooting

**Simulator mode:**
- Make sure `sensor_simulator.py` is running
- Check that `fake_sensor.csv` is being created
- Verify Flask is reading from the CSV file

**Arduino mode:**
- Check USB cable connection
- Verify correct port in `arduino_reader.py`
- Close Arduino IDE Serial Monitor before running
- Ensure `pyserial` is installed

**DHT11 reading errors:**
- Check wiring connections
- Wait 2 seconds after powering on Arduino
- May need 10kΩ pull-up resistor between DATA and VCC

**SMS not sending:**
- Verify Twilio credentials are correct
- Check phone number format includes country code: `+1234567890`
- Verify phone number is verified in Twilio console (free trial)

**React dashboard not loading:**
- Ensure Flask is running on port 5000
- Check browser console (F12) for errors
- Verify `flask-cors` is installed

## API Endpoints

- `GET /api/sensor` - Get latest sensor reading
- `GET /api/sensor/history` - Get last 20 readings
- `GET /api/alerts/settings` - Get alert configuration
- `POST /api/alerts/settings` - Update alert settings
- `GET /api/status` - Check Arduino connection status

## Technologies Used

**Backend:** Flask, SQLite, PySerial, Twilio  
**Frontend:** React, Vite, Recharts, Lucide Icons  
**Hardware:** Arduino Uno, DHT11, PIR Sensor (optional)

## Author

**Abdulrahman Akanbi**  
LinkedIn: [Your Profile](https://linkedin.com/in/AbdulrahmanAkanbi)

## License

MIT License