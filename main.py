import serial

serial_port = '/dev/ttyUSB0'
baud_rate = 9600
output_file = 'parada.data'

try:
    with serial.Serial(serial_port, baud_rate, timeout=1) as ser, open(output_file, 'a') as f:
        print(f"Loguju data z {serial_port} do {output_file}...")
        while True:
            line = ser.readline().decode('utf-8').strip()
            if line:
                print(line)
                f.write(line + '\n')
                f.flush()
except KeyboardInterrupt:
    print("\nUkonceno uzivatelem !!!!")
except Exception as e:
    print(f"Error: {e}")

