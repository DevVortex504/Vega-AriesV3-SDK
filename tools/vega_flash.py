import serial
import sys
import time
import os

PORT = '/dev/cu.usbserial-130'
BAUD = 115200
BIN_FILE = './Examples/LED/build/app.bin'

if not os.path.exists(BIN_FILE):
    print(f"Error: {BIN_FILE} not found! Compile with 'cmake --build build' first.")
    sys.exit(1)

with open(BIN_FILE, 'rb') as f:
    payload = f.read()

print(f"[*] Loaded {BIN_FILE} ({len(payload)} bytes)")

def crc16_ccitt(data):
    crc = 0
    for byte in data:
        crc ^= (byte << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return crc

ser = serial.Serial(PORT, BAUD, timeout=0.1)
ser.reset_input_buffer()
ser.reset_output_buffer()

print("[*] Jumper requirement: BOOT-SEL must be CLOSED (connected).")
print("[*] Press and release the physical RESET button on the Aries V3...")

# Phase 1: Detect '<' and respond immediately with '>'
while True:
    b = ser.read(1)
    if not b:
        continue
    try:
        sys.stdout.write(b.decode('ascii', errors='replace'))
        sys.stdout.flush()
    except:
        pass

    if b == b'<':
        ser.write(b'>')
        ser.flush()
        print("\n[+] Captured '<' -> Handshake '>' transmitted!")
        break

# Phase 2: Await XMODEM CRC synchronization ('C')
print("[*] Awaiting 'C' synchronization from board...")
ser.timeout = 1.0
c_received = 0
while True:
    ch = ser.read(1)
    if ch == b'C':
        c_received += 1
        if c_received >= 1:
            print("\n[+] 'C' received. Starting XMODEM block transmission...")
            break
    elif ch:
        try:
            sys.stdout.write(ch.decode('ascii', errors='replace'))
            sys.stdout.flush()
        except:
            pass

# Phase 3: Transmit 128-byte XMODEM CRC blocks
packet_size = 128
total_packets = (len(payload) + packet_size - 1) // packet_size
pkt_num = 1

for i in range(0, len(payload), packet_size):
    chunk = payload[i:i + packet_size]
    if len(chunk) < packet_size:
        chunk = chunk + b'\xff' * (packet_size - len(chunk))

    crc = crc16_ccitt(chunk)
    header = bytes([0x01, pkt_num & 0xFF, (~pkt_num) & 0xFF])
    crc_bytes = bytes([(crc >> 8) & 0xFF, crc & 0xFF])
    packet = header + chunk + crc_bytes

    # Transmit with ACK verification
    for attempt in range(10):
        ser.write(packet)
        ser.flush()
        resp = ser.read(1)
        if resp == b'\x06':  # ACK
            break
        time.sleep(0.02)

    sys.stdout.write(f"\rFlashing SPI: Block {pkt_num}/{total_packets} ({(pkt_num/total_packets)*100:.1f}%)")
    sys.stdout.flush()
    pkt_num = (pkt_num + 1) % 256

# Phase 4: End of Transmission (EOT)
print("\n[*] Sending End of Transmission (EOT)...")
for _ in range(5):
    ser.write(b'\x04')  # EOT
    ser.flush()
    if ser.read(1) == b'\x06':
        break

print("\n[SUCCESS] Flash complete! Opening live serial output...\n" + "-" * 50)

# Phase 5: Live monitor
ser.timeout = 0.1
while True:
    try:
        line = ser.read(ser.in_waiting or 1)
        if line:
            sys.stdout.write(line.decode('utf-8', errors='replace'))
            sys.stdout.flush()
    except KeyboardInterrupt:
        print("\nDisconnected.")
        break

ser.close()