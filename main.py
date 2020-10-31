from machine import UART
from fpioa_manager import fm
import time

fm.register(7,fm.fpioa.UART1_TX)
fm.register(6,fm.fpioa.UART1_RX)

uart = UART(UART.UART1,9600,8,1,0,timeout=1000, read_buf_len=4096)

for i in range(200):
    uart.write("AT+NAMEMAIXDUINO\r\n")
    time.sleep_ms(200)
    read_data = uart.read()
    if read_data:
        read_str = read_data.decode('utf-8')
        count = read_str.count("OK")
        if count != 0:
            uart.write("set success")
            
while True:
           uart.write("hello world!\r\n")
