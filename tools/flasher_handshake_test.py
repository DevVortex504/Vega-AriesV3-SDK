import serial
import sys
import time

PORT = '/dev/cu.usbserial-130'
BAUD = 115200

ser = serial.Serial(PORT, BAUD, timeout=0.1)
ser.reset_input_buffer()

print("=" * 60)
print("Handshake Diagnostic Tool")
print(f"Monitoring port: {PORT} at {BAUD} baud")
print("Make sure BOOT-SEL jumper is CLOSED, then press RESET on Aries V3.")
print("=" * 60)

handshake_sent = False

try:
    while True:
        raw_byte = ser.read(1)
        if not raw_byte:
            continue

        # Print all incoming raw serial output
        try:
            char = raw_byte.decode('ascii', errors='replace')
            sys.stdout.write(char)
            sys.stdout.flush()
        except Exception:
            pass

        # Detect the trigger '<' (0x3C)
        if raw_byte == b'<' and not handshake_sent:
            # Send '>' (0x3E) immediately
            ser.write(b'>')
            ser.flush()
            handshake_sent = True
            print("\n" + "#" * 50)
            print("[+] DETECTED '<' -> TRANSMITTED '>' TO BOARD")
            print("[+] Now listening for 'C' (0x43) / Erase response...")
            print("#" * 50)

        # Detect the XMODEM CRC prompt 'C' (0x43)
        if raw_byte == b'C' and handshake_sent:
            print("\n" + "=" * 50)
            print("[SUCCESS] Handshake verified! Board is in XMODEM receive mode.")
            print("=" * 50)
            break

except KeyboardInterrupt:
    print("\nDiagnostic stopped by user.")

finally:
    ser.close()