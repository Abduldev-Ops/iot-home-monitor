import alerts

# Test sending an SMS
print("Testing SMS alerts...")

# Send a test message
success = alerts.send_sms("Test alert from ACE IoT Monitor! If you received this, alerts are working!")

if success:
    print("SMS sent successfully! Check your phone.")
else:
    print("SMS failed. Check your Twilio credentials.")

# Test alert logic
print("\nTesting alert logic...")
alerts.check_and_alert(
    temperature=40.0,  # Above threshold
    humidity=50.0,
    motion=True,       # Motion detected
    timestamp="2025-01-01 15:30:45"
)