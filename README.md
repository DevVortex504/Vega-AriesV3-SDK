# VEGA Aries V3 Modern SDK & Native Toolchain

A modern, open-source bare-metal SDK, build system, and native flashing workflow for the **C-DAC VEGA Aries V3** board (RISC-V 32-bit, Thejas32 SoC, Vega ET1031 core). 

This repository solves common roadblocks when developing on modern host environments (such as macOS Apple Silicon M1/M2/M3/M4 and modern Linux distributions with GCC 12+) (Tested on M1).

---

## ✨ Features

- **Modern RISC-V Toolchain Support:** Fully compatible with modern xPack GCC 14/15 (`riscv-none-elf-gcc`).
- **Native Cross-Platform Flashing:** Includes a standalone Python SPI Flash flasher (`vega_flash.py`) supporting macOS.
- **Standard CMake Workflow:** Clean, standard-compliant CMake integration for building bare-metal applications.

---

## 📂 Repository Structure

```text
vega-aries-modern-sdk/
├── README.md
├── LICENSE
├── tools/
│   ├── vega_flash.py         # Native Python XMODEM/SPI flasher
│   └── requirements.txt      # Python dependencies (pyserial)
├── sdk/                      # Patched Taurus SDK tree
│   ├── CMakeLists.txt
│   ├── setup.sh
│   ├── common/               
│   └── ...
└── Examples/
    └── Timer/        # Starter project template
        ├── CMakeLists.txt    
        └── main.c            # Starter code 
```

---

## 🛠️ Prerequisites

1. **RISC-V GCC Toolchain:** Download and install the modern xPack RISC-V GCC toolchain (e.g., GCC 15.2.0) and ensure `riscv-none-elf-gcc` is in your system `PATH`.
2. **Build Tools:** `cmake` and `make` (or `ninja`).
3. **Python 3 & Serial Library:**
   ```bash
   pip3 install pyserial
   ```

---

## 🚀 Quickstart Guide

### 1. Build & Install the SDK
Clone the repository and install the patched Taurus SDK into your local system paths:
```bash
cd sdk
./setup.sh -tb ARIES_V3 -tt riscv-none-elf
```

### 2. Compile Your Application
Navigate to your application or template folder, create a build directory, and compile:
```bash
cd Examples/LED
cmake -B build -DCMAKE_TOOLCHAIN_FILE=/usr/local/lib/cmake/taurus/taurusToolchain.cmake
cmake --build build
```
This produces `app.elf` and automatically extracts the raw binary image `app.bin`.

### 3. Permanently Flash to SPI Memory
1. Connect your VEGA Aries V3 board via USB.
2. Ensure the **BOOT-SEL jumper is CLOSED** (bridged) so the board enters SPI bootloader mode.
3. Run the Python flasher script:
   ```bash
   python3 ../../tools/vega_flash.py build/app.bin
   ```
4. When prompted by the script, press and release the physical **RESET** button on the Aries V3 board.
5. The script will automatically catch the `<` $\rightarrow$ `>` handshake, upload the binary via XMODEM CRC-16, burn it into permanent SPI Flash, and open a live serial console.

---

## ⚙️ Technical Highlights

### The SPI Flash Handshake
The Aries V3 secondary bootloader (`FLASHER`) listens for a host response over serial:
- **Board outputs:** `<` (`0x3C`)
- **Host replies:** `>` (`0x3E`)
- **Board initiates:** `C` (`0x43`, XMODEM-CRC synchronization prompt)
- **Host transmits:** 128-byte packets with CRC-16 CCITT validation.

### GCC 15 TLS Resolution
Modern GCC 15 enforces strict section typing. To prevent `_tdata_end` type mismatches between assembler sections and C references, boundary markers are explicitly defined as standard non-TLS memory symbols in `mbl.lds`:
```ld
.tdata : {
    _tls_data = .;
    _tdata_begin = .;
    *(.tdata.begin)
    *(.tdata)
    *(.tdata.end)
    _tdata_end = .;
}
```

---

## 📜 License
See the [LICENSE](LICENSE) file for details. Based on Taurus SDK architecture.