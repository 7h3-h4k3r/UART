from machine import UART, Pin

uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
led_pin = Pin(2,Pin.OUT)

uart.write(b'\033[2J')
uart.write(b'\033[H')
uart.write(b'\033[?25l')

uart.write(b'Welcome to The UART Exploit Class Room\r\n')

SHELL = b'=> '
uart.write(SHELL)

command = []

def toggle_led():
    if led_pin.value():
        led_pin.off()
        return 'off'
    
    led_pin.on()
    return 'on'
    
while True:
    if uart.any():
        ch = uart.read(1) 
        if ch == b'\r' or ch == b'\n':
            uart.write(b'\r\n')

            cmd = ''.join(command)
            
            if cmd == 'led':
                value = toggle_led()
                uart.write(b'led is '+value+'\r\n')
            else:
                uart.write(b'commend not found !!\r\n')

            command = []
            uart.write(SHELL)
        elif ch == b'\x08' or ch == b'\x7f':
            if len(command) > 0:
                command.pop()
                uart.write(b'\b \b')
        else:
            try:
                char = ch.decode()
                command.append(char)
                uart.write(ch)
            except:
                pass
