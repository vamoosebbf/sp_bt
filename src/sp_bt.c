#include "sp_bt.h"
#include <string.h>
#include "bsp.h"
#include "uart.h"
#include "syslog.h"

void bt_test(void)
{
    char* hel = "hello world!\r\n";
    char rcv_buf[50],send_buf[50],at_order[50];
    int ret,times = 200;
    while(times--) //set the name of sp_bt module
    {
        sprintf(at_order,"AT+NAME%s\r\n",SP_BT_NAME);
        strcpy(send_buf,at_order);
        uart_send_data(UART_NUM, send_buf, strlen(send_buf));
        msleep(100);
        ret = uart_receive_data(UART_NUM, rcv_buf, sizeof(rcv_buf));
        printk(LOG_COLOR_W "seting name...\r\n");
        if(ret != 0 && strstr(rcv_buf, "OK"))
        {
            printk(LOG_COLOR_W "set name success!\r\n");
            break;
        }
    }
    while (1)
    {
        msleep(1000);
        uart_send_data(UART_NUM, hel, strlen(hel));
    }
}
