from twilio.rest import Client
import os
from datetime import datetime

# Twilio credentials (you'll add your own)
TWILIO_ACCOUNT_SID = "YOUR_ACCOUNT_SID_HERE"
TWILIO_AUTH_TOKEN = "YOUR_AUTH_TOKEN_HERE"
TWILIO_PHONE_NUMBER = "YOUR_TWILIO_PHONE_NUMBER_HERE"
YOUR_PHONE_NUMBER = "YOUR_PERSONAL_PHONE_NUMBER_HERE"  # Where to send alerts

# Alert settings
TEMP_THRESHOLD = 35.0  # Alert if temp > 35°C
MOTION_ALERTS_ENABLED = True
TEMP_ALERTS_ENABLED = True

# Initialize Twilio client
try:
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    print("✅ Twilio client initialized")
except Exception as e:
    print(f"⚠️ Twilio initialization failed: {e}")
    client = None

# Track last alert time to avoid spam
last_motion_alert = None
last_temp_alert = None
ALERT_COOLDOWN = 300  # 5 minutes between alerts (in seconds)

def send_sms(message):
    """Send an SMS using Twilio"""
    if not client:
        print("⚠️ Twilio client not initialized. Cannot send SMS.")
        return False
    
    try:
        message = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=YOUR_PHONE_NUMBER
        )
        print(f"✅ SMS sent! SID: {message.sid}")
        return True
    except Exception as e:
        print(f"❌ Failed to send SMS: {e}")
        return False

def should_send_alert(alert_type):
    """Check if enough time has passed since last alert (cooldown)"""
    global last_motion_alert, last_temp_alert
    
    now = datetime.now()
    
    if alert_type == "motion":
        if last_motion_alert is None:
            last_motion_alert = now
            return True
        
        time_diff = (now - last_motion_alert).total_seconds()
        if time_diff >= ALERT_COOLDOWN:
            last_motion_alert = now
            return True
        return False
    
    elif alert_type == "temperature":
        if last_temp_alert is None:
            last_temp_alert = now
            return True
        
        time_diff = (now - last_temp_alert).total_seconds()
        if time_diff >= ALERT_COOLDOWN:
            last_temp_alert = now
            return True
        return False
    
    return False

def check_and_alert(temperature, humidity, motion, timestamp):
    """Check sensor data and send alerts if needed"""
    alerts_sent = []
    
    # Check temperature threshold
    if TEMP_ALERTS_ENABLED and temperature > TEMP_THRESHOLD:
        if should_send_alert("temperature"):
            message = f"🌡️ HIGH TEMPERATURE ALERT!\n\nTemp: {temperature:.1f}°C (Threshold: {TEMP_THRESHOLD}°C)\nTime: {timestamp}\n\n- ACE IoT Monitor"
            if send_sms(message):
                alerts_sent.append("temperature")
                print(f"🚨 Temperature alert sent: {temperature:.1f}°C")
    
    # Check motion detection
    if MOTION_ALERTS_ENABLED and motion:
        if should_send_alert("motion"):
            message = f"👁️ MOTION DETECTED!\n\nMotion sensor triggered\nTime: {timestamp}\n\n- ACE IoT Monitor"
            if send_sms(message):
                alerts_sent.append("motion")
                print(f"🚨 Motion alert sent")
    
    return alerts_sent

def set_alert_settings(temp_enabled, motion_enabled, temp_threshold):
    """Update alert settings"""
    global TEMP_ALERTS_ENABLED, MOTION_ALERTS_ENABLED, TEMP_THRESHOLD
    
    TEMP_ALERTS_ENABLED = temp_enabled
    MOTION_ALERTS_ENABLED = motion_enabled
    TEMP_THRESHOLD = temp_threshold
    
    print(f"✅ Alert settings updated:")
    print(f"   - Temp alerts: {'ON' if temp_enabled else 'OFF'} (Threshold: {temp_threshold}°C)")
    print(f"   - Motion alerts: {'ON' if motion_enabled else 'OFF'}")

def get_alert_settings():
    """Get current alert settings"""
    return {
        'temp_enabled': TEMP_ALERTS_ENABLED,
        'motion_enabled': MOTION_ALERTS_ENABLED,
        'temp_threshold': TEMP_THRESHOLD
    }