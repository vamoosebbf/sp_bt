from machine import UART
from fpioa_manager import fm
import time

name = "MAIXCUBE"


def set_name(uart, name):
    for i in range(200):
        # change the name to MAIXDUINO
        uart.write("AT+NAME{}\r\n".format(name))
        time.sleep_ms(200)
        read_data = uart.read()
        if read_data:
            read_str = read_data.decode('utf-8')
            count = read_str.count("OK")
            if count != 0:
                print("set success")
                break


def main():
    # set uart rx/tx func to io_6/7
    fm.register(7, fm.fpioa.UART1_TX)
    fm.register(6, fm.fpioa.UART1_RX)

    # init uart
    uart = UART(UART.UART1, 9600, 8, 1, 0, timeout=1000, read_buf_len=4096)

    set_name(uart, name)

    print("wait data: ")
    while True:
        read_data = uart.read()
        if read_data:
            print("recv:", read_data)
            uart.write(read_data)  # send data
            print("wait data: ")


main()
