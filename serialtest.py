import serial

# Replace with your actual device
serial_port = '/dev/ttyUSB0'
baud_rate = 9600  # Set this according to your device
output_file = 'output.txt'

try:
    with serial.Serial(serial_port, baud_rate, timeout=1) as ser, open(output_file, 'w') as f:
        print(f"Reading from {serial_port} and writing to {output_file}...")
        while True:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                print(line)
                f.write(line + '\n')
                f.flush()
except KeyboardInterrupt:
    print("\nStopped by user.")
except Exception as e:
    print(f"Error: {e}")

