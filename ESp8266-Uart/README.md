# ESP8266-01S + CP2102 MicroPython Flashing & UART Connection

## Overview

This project demonstrates how to connect an **ESP8266-01S WiFi module** with a **CP2102 USB to UART converter** for:

* Flashing MicroPython firmware
* Accessing the REPL terminal
* Learning UART communication
* Building low-level embedded networking projects

The setup was tested successfully using:

* Ubuntu Linux
* Thonny IDE
* CP2102 USB UART
* ESP8266-01S (1MB Flash)

---

# Hardware Used

## Components

* ESP8266-01S
* CP2102 USB to UART Converter
* Jumper wires
* Breadboard (optional)
* USB cable

---

# Connection Diagram

## ESP8266-01S ↔ CP2102 Wiring

| CP2102 | ESP8266-01S                    |
| ------ | ------------------------------ |
| 3V3    | VCC (3V3)                      |
| GND    | GND                            |
| TXD    | RX                             |
| RXD    | TX                             |
| 3V3    | EN                             |
| GND    | GPIO0 *(only during flashing)* |

---

# Flash Mode Explanation

To enter flashing mode:

* Connect **GPIO0 → GND**
* Power ON the ESP8266
* EN pin must stay HIGH (3.3V)

This puts the ESP8266 into bootloader mode.

After flashing:

* Disconnect GPIO0 from GND
* Restart the board
* ESP8266 boots normally into MicroPython

---

# Real Hardware Setup

## ESP8266 + CP2102 Connection

![Image](https://github.com/7h3-h4k3r/UART/blob/main/ESp8266-Uart/images/photo.jpg)

![Image](https://github.com/7h3-h4k3r/UART/blob/main/ESp8266-Uart/images/schematic.png)

![Image](https://github.com/7h3-h4k3r/UART/blob/main/ESp8266-Uart/images/shell.png)
---

# Flashing MicroPython using Thonny

## Step 1 — Open Thonny

Install Thonny:

```bash
sudo apt install thonny
```

Open:

```bash
thonny
```

---

## Step 2 — Configure Interpreter

Go to:

```text
Tools → Options → Interpreter
```

Select:

```text
Interpreter: MicroPython (ESP8266)
Port: /dev/ttyUSB0
```

---

## Step 3 — Query Device

Click:

```text
Install or update MicroPython
```

Then:

```text
Query device
```

You should see:

* ESP8266 detected
* Flash size (example: 1MB)

---

## Step 4 — Download Firmware

Choose firmware matching your flash size.

Example:

```text
ESP8266_GENERIC-1M.bin
```

---

## Step 5 — Flash Firmware

Click:

```text
Install
```

Wait until flashing completes.

---

# Successful Boot Output

After flashing and rebooting:

```python
MPY: soft reboot
MicroPython v1.28.0 on 2026-04-06; ESP module (1M) with ESP8266
Type "help()" for more information.
>>>
```

This means:

* Firmware installed correctly
* UART communication working
* REPL shell active

---

# UART Concepts Learned

This setup helps explore:

* Serial communication
* TX/RX crossover
* Boot modes
* Flash memory detection
* REPL interaction
* Embedded Python development

---

# Common Problems

## `Failed to connect to Espressif device`

### Causes

* GPIO0 not connected to GND
* Wrong TX/RX wiring
* Insufficient power
* Busy serial port

---

## `Could not open /dev/ttyUSB0`

Close other serial programs:

```bash
sudo fuser -k /dev/ttyUSB0
```

Or close:

* minicom
* screen
* picocom
* Thonny duplicate sessions

---

# Verify USB UART

Check CP2102 detection:

```bash
lsusb
```

Expected:

```text
Silicon Labs CP210x UART Bridge
```

Check serial port:

```bash
ls /dev/ttyUSB*
```

---

# Simple REPL Test

Inside Thonny shell:

```python
print("Hello ESP8266")
```

LED blink test:

```python
from machine import Pin
import time

led = Pin(2, Pin.OUT)

while True:
    led.toggle()
    time.sleep(1)
```

---

# Why This Setup Is Powerful

The ESP8266 + MicroPython combination is excellent for learning:

* IoT
* Networking
* UART internals
* Embedded Linux workflows
* Firmware flashing
* Low-level debugging
* MQTT
* WiFi automation

---

# Moto

Built for learning embedded systems, UART communication, and MicroPython exploration using ESP8266-01S.
