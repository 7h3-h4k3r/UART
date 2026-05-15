from machine import Pin , UART ,freq

class Shell:
    
    def __init__(self,channel,_baudrate,tx_pin,rx_pin):
        self.uart = UART(channel,baudrate=_baudrate,tx=Pin(tx_pin),rx=Pin(rx_pin))
        self.shell=b'\r\n}> '
        self.get=[]
        self.commends ={
            'clear':self.clear_screen,
            'freq' :self.get_freq,
            'hello' : self.hello,
            }
        self.moves = {
            'A':self.history_up,
            'B':self.history_down,
            }
        self.history = []
        self.history_len = 0
    def hello(self):
        self.uart.write(b'hello i am cp21o2\r\n')
    def get_freq(self):
        freq_data = str(freq())
        self.uart.write(freq_data.encode())
    def set_history(self,data):
        self.history.append(data)
        self.history_len = len(self.history)
    def history_up(self):
        
        if len(self.history) < 0:
            return
        
        if len(self.history) > self.history_len:
            return
        self.uart.write(self.history[-self.history_len])
        self.history_len-=1
            
    
    def history_down(self):
        if len(self.history) < 0:
            return
        
        if len(self.history) > self.history_len:
            return
        print('yes iam call')
        self.uart.write(self.history[self.history_len])
        self.history_len+=1
    def clear_screen(self):
        self.uart.write(b'\033[2J\033[H')
    
    def get_shell(self):
        self.uart.write(self.shell)
        
    def welcome_message(self):
        self.uart.write(b'Welcome to the cp21o2 mini Shell')
    def back_space(self):
        self.uart.write(b'\b \b')
    def err(self,internal=True):
        if internal:
            self.uart.write('commend not found !!')
        else:
            self.uart.write('somewent is wrong')
        
    def control(self,u,debug):
        while self.uart.any():
            ch = self.uart.read(1)
            
            if ch == b'\r':
                commend = ''.join(self.get)
                if commend in self.commends:
                    self.commends[commend]()
                else:
                    self.err()
                
                self.get = []
                self.get_shell()
                self.set_history(commend)
                
            elif ch  in (b'\x08' , b'\x7f'):
                print(self.get)
                if len(self.get) > 0:
                    self.get.pop()
                self.back_space()
              
            elif ch in (b'\x1b'):
                move = self.uart.read(2).decode()[1]
                
                if move in self.moves:
                    self.moves[move]()
                
            else:
                ch_decode=ch.decode()
                self.get.append(ch_decode)
                self.uart.write(ch)
            
            if debug:
                print('Decode Message ' ,ch.decode(),'Byte format',ch)

    def run(self,debug):
        self.clear_screen()
        self.welcome_message()
        self.get_shell()
        self.uart.irq(handler=lambda u:self.control(u,debug),trigger=UART.IRQ_RXIDLE)
        
        
if __name__ =='__main__':
    Shell(0,9600,0,1).run(debug=True)
