#kde se vzal tenhle kod??
import serial
import mysql.connector
from mysql.connector import Error
from datetime import datetime

serial_port = '/dev/ttyUSB0'
baud_rate = 9600

db_config = {
    'host': 'deu-he-5.livezone.cz',
    'port': 3306,
    'user': 'u276_QKZqihQ9x7',  # or 'readonly_user' if you're using read-only
    'password': 'YOUR_DB_PASSWORD',
    'database': 's276_TelemetryData',
    'ssl_disabled': True  # because your hosting doesn't support SSL
}

def insert_scalar(cursor, sensor_type, value):
    cursor.execute("SELECT id FROM sensor_types WHERE name = %s", (sensor_type,))
    result = cursor.fetchone()
    if not result:
        print(f"⚠️ Unknown sensor type: {sensor_type}")
        return
    sensor_type_id = result[0]
    cursor.execute(
        "INSERT INTO sensor_data (sensor_type_id, value, timestamp) VALUES (%s, %s, %s)",
        (sensor_type_id, value, datetime.now())
    )
def insert_vector(cursor, sensor_type, x, y, z):
    cursor.execute("SELECT id FROM sensor_types WHERE name = %s", (sensor_type,))
    result = cursor.fetchone()
    if not result:
        print(f"⚠️ Unknown vector sensor type: {sensor_type}")
        return
    sensor_type_id = result[0]
    cursor.execute(
        "INSERT INTO vector_data (sensor_type_id, x, y, z, timestamp) VALUES (%s, %s, %s, %s, %s)",
        (sensor_type_id, x, y, z, datetime.now())
    )
try:
    ser = serial.Serial(serial_port, baud_rate, timeout=1)
    print(f"📡 Reading from {serial_port}...")

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    print("✅ Connected to MariaDB.")

    while True:
        line = ser.readline().decode('utf-8').strip()
        if not line:
            continue

        print(f"📥 Received: {line}")

        # Expected formats (example):
        # temperature:24.5
        # gyroscope:1.2,0.5,9.8
        try:
            if ':' not in line:
                continue

            sensor_type, data = line.split(':', 1)
            parts = data.split(',')

            if len(parts) == 1:
                value = float(parts[0])
                insert_scalar(cursor, sensor_type, value)
            elif len(parts) == 3:
                x, y, z = map(float, parts)
                insert_vector(cursor, sensor_type, x, y, z)
            else:
                print("⚠️ Unexpected data format.")
                continue

            conn.commit()

        except Exception as e:
            print(f"❌ Parse or DB error: {e}")

except KeyboardInterrupt:
    print("\n🛑 Interrupted by user.")
except Error as e:
    print(f"❌ MariaDB Error: {e}")
finally:
    if 'conn' in locals() and conn.is_connected():
        conn.close()
        print("🔒 Database connection closed.")
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("🔌 Serial port closed.")

