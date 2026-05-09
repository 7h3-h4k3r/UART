# UART LED Command Shell

A simple UART-based command shell built using MicroPython.
This project demonstrates how UART communication works on a microcontroller by creating a small terminal interface that accepts commands and responds through serial communication.

---

# Features

* UART communication using MicroPython
* Terminal-style command interface
* LED command handling
* Custom shell prompt
* Clear terminal screen using ANSI escape sequences
* Backspace support
* Beginner-friendly embedded systems project

---

# Hardware Required

* Raspberry Pi Pico / Pico W
* CP2102 USB to UART converter (optional)
* Jumper wires
* LED (optional for real LED control)
* Breadboard

---

# UART Wiring

| Pico Pin | UART Converter |
| -------- | -------------- |
| GP0 (TX) | RX             |
| GP1 (RX) | TX             |
| GND      | GND            |

> TX connects to RX and RX connects to TX.

---

# Project Idea

The project creates a mini serial shell.
When the user types commands in a UART terminal:

* `led` → LED ON message
* any other command → LED OFF / command not found message

This helps beginners understand:

* Serial communication
* Event loops
* UART buffers
* Command parsing
* Terminal interaction
* Embedded system basics

---

# Example Output

```text
Welcome to The UART Explore Classroom

=> led
led is On

=> hello
command not found !!

=> led
led is off
```

---

# MicroPython Code

```python
from machine import UART, Pin

uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

uart.write(b'\033[2J')
uart.write(b'\033[H')
uart.write(b'\033[?25l')

art = 'Welcome to The UART Explore Classroom\r'
uart.write(art.encode())

SHELL = '\r\n=> '
uart.write(SHELL)

command = []

while True:
    if uart.any():
        uart_value = uart.read()

        if uart_value.decode() == '\r':

            if ''.join(command) == 'led':
                print('led is On')
            else:
                print('led is off')

            command = []
            uart.write(SHELL.encode())

        elif uart_value.decode() == '\x08':
            uart.write('\b \b')

        else:
            command.append(uart_value.decode())
```

---

# How It Works

## UART Initialization

```python
UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
```

Creates UART channel 0 using:

* GP0 as TX
* GP1 as RX
* 9600 baud rate

---

## Terminal Escape Sequences

```python
b'\033[2J'
```

Clears the terminal screen.

```python
b'\033[H'
```

Moves cursor to home position.

```python
b'\033[?25l'
```

Hides the cursor.

---

## Command Handling

Characters are collected one-by-one into a list.
When Enter (`\r`) is pressed:

* the command is joined
* checked against known commands
* response is printed
* shell prompt appears again


---

# Learning Outcomes

After completing this project you will understand:

* UART communication basics
* Serial terminal interaction
* Embedded event loops
* Input parsing
* ANSI terminal control
* MicroPython UART programming

---

# Author

Built as a UART learning experiment using MicroPython and Raspberry Pi Pico.
