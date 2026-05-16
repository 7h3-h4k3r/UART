from machine import Pin , UART ,freq

class Shell:
    
    def __init__(self,channel,_baudrate,tx_pin,rx_pin):
        self.uart = UART(channel,baudrate=_baudrate,tx=Pin(tx_pin),rx=Pin(rx_pin))
        self.shell=b'\r\n}> '
        self.get=[]
        self.index = 0
        self.commends ={
            'clear':self.clear_screen,
            'freq' :self.get_freq,
            'hello' : self.hello,
            'help' : self.help,
            }
        self.moves = {
            'A':self.history_up,
            'B':self.history_down,
            'C':self.right,
            'D':self.left
            }
        self.history = []
        self.history_len = 0
    def help(self):
        print('demo')
    def hello(self):
        self.uart.write(b'hello i am cp21o2\r\n')
    def get_freq(self):
        freq_data = str(freq())
        self.uart.write(freq_data.encode())
    def set_history(self,data):
        self.history.append(data)
        self.history_len = len(self.history)
    def history_up(self):
        if len(self.history) <= 0:
            return
        
        if self.history_len <= 0:
            self.history_len = len(self.history)
        
        self.history_len -=1
        cmd = self.history[self.history_len]

        self.get_shell(True)
        self.uart.write(cmd.encode())
        
        self.get = list(cmd)

  
    def insert_char(self, ch_decode):

        self.get = (
            self.get[:self.index]
            + [ch_decode]
            + self.get[self.index:]
        )

        
        self.index += 1

        self.redraw_input()


    def redraw_input(self):
        self.get_shell(True)

        text = ''.join(self.get)
        self.uart.write(text.encode())

        move_back = len(self.get) - self.index

        if move_back > 0:
            self.uart.write(f'\033[{move_back}D'.encode())
            
            
    def history_down(self):
        if not self.history:
            return

        
        if self.history_len < len(self.history) - 1:
            self.history_len += 1
            cmd = self.history[self.history_len]
        else:
            self.history_len = len(self.history)
            cmd = ""

        self.get_shell(True)
        self.uart.write(cmd.encode())
        self.get = list(cmd)
        
        
    def left(self):
        if self.index > 0:
            self.index -=1
            self.uart.write(b'\033[D')
            
    def right(self):
        
        if self.index < len(self.get):
            self.index +=1 
            self.uart.write(b'\033[C')
        
        
    def clear_screen(self):
        self.uart.write(b'\033[2J\033[H')
    
    def get_shell(self,current_line=False):
        if current_line:
            self.uart.write(b'\r\033[2K}> ' )
        else:
            self.uart.write(self.shell)
        
    def welcome_message(self):
        self.uart.write(b'Welcome to the cp21o2 mini Shell')
    def back_space(self):
        self.uart.write(b'\b \b')
    def err(self,internal=True):
        if internal:
            self.uart.write('\r\ncommend not found !!')
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
                if len(commend) != 0:
                    self.set_history(commend)
                self.index = 0 
            elif ch == b'\t':
                if not self.get:
                    return
                print(self.get)
                string = ''.join(self.get)
                start_with = [ i for i in self.commends if i.startswith(string)]
                if len(start_with) == 1:
                    self.get_shell(True)
                    self.uart.write(start_with[0].encode())
                    self.get = list(start_with[0])
                else:
                    self.uart.write(b'\r\n')
                    for i in start_with:
                        self.uart.write(i.encode())
                        self.uart.write(b'\t')
                    self.get_shell()
                    self.get = []
                    
                    
                
                
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
                self.insert_char(ch_decode)
        
            if debug:
                print('Decode Message ' ,ch.decode(),'Byte format',ch)

    def run(self,debug):
        self.clear_screen()
        self.welcome_message()
        self.get_shell()
        self.uart.irq(handler=lambda u:self.control(u,debug),trigger=UART.IRQ_RXIDLE)
        
        
if __name__ =='__main__':
    Shell(0,9600,0,1).run(debug=True)
