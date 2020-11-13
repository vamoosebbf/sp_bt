<img src="img/icon_sipeed2.png" style="zoom: 80%;" />

# SP_BT 模块使用说明

[English](README.md)

## 目录结构

|  目录  | 描述           |
| :----: | :------------- |
|  doc   | 参考文档       |
|  img   | 图片           |
| script | MaixPy脚本示例 |
|  src   | C裸机程序示例  |

## 介绍

SP_BT 是一款蓝牙串口透传模块，具备超低功率特性和高可靠性。

* 蓝牙版本：支持 BLE 5.0（兼容BLE4.0、BLE4.2）

* 默认串口波特率：9600

  <img src="img/sp_bt.png" alt="SP_BT" height="400"/>

  *详细特性参考[SP-BT 规格书 V1.0.pdf](doc/SP-BT规格书V1.0.pdf)*

## 接线方式
<img src="img/connection.png" height="200">

|  MCU:FUN(IO)  | SP_BT |
| :-----------: | :---: |
| UART:TX(IO_7) |  RX   |
| USRT:RX(IO_6) |  TX   |
|   1.8-3.3V    | 3.3V  |
|      GND      |  GND  |

## 引脚图

<img src="img/sp_bt_back.jpg" height="250" />

## 指示灯

|   模式   |       状态       |
| :------: | :--------------: |
| 等待连接 |  ACT慢闪，STA灭  |
|  已连接  | ACT常亮，STA常亮 |

## MCU 端口配置

### IO 口配置

将原理图对应的IO口配置为串口收发功能号。

* C 示例

  ```c
  // set uart rx/tx func to io_6/7
  fpioa_set_function(6, FUNC_UART1_RX + UART_NUM * 2);
  fpioa_set_function(7, FUNC_UART1_TX + UART_NUM * 2);
  ```

* MaixPy 示例

  ```python
  # set uart rx/tx func to io_6/7
  fm.register(6,fm.fpioa.UART1_RX)
  fm.register(7,fm.fpioa.UART1_TX)
  ```

### UART  初始化

UART 初始化波特率必须与 SP_BT 波特率一致，可以使用AT指令改变 SP_BT 的波特率，这里默认为9600。

* C 示例

  ```c
  uart_init(UART_DEVICE_1);
  uart_configure(UART_DEVICE_1, 9600, 8, UART_STOP_1, UART_PARITY_NONE);
  ```

* MaixPy 示例

  ```python
  uart = UART(UART.UART1,9600,8,1,0,timeout=1000, read_buf_len=4096)
  ```

## SP_BT 配置

### AT 指令列表

|       指令        |               功能                |
| :---------------: | :-------------------------------: |
| AT+BAUD\<Param\>  | 波特率（0-6）分别代表不同的波特率 |
| AT+NAME\<Param\>  |              广播名               |
| AT+SLEEP\<param\> |               睡眠                |

*更多AT指令请参考[JDY-23-V2.1.pdf](doc/JDY-23-V2.1.pdf)*

### AT 指令使用

* 流程
  1. 发送 AT 指令
  2. 接收数据
  3. 判断是否设置成功

* C 示例

  ```c
  //change the name of sp_bt module to MAIXCUBE
  uart_send_data(UART_NUM, "AT+NAMEMAIXCUBE\r\n", strlen("AT+NAMEMAIXCUBE\r\n")); //send AT order
  msleep(100);
  ret = uart_receive_data(UART_NUM, rcv_buf, sizeof(rcv_buf)); //receive response
  if(ret != 0 && strstr(rcv_buf, "OK"))
  {
     printk(LOG_COLOR_W "set name success!\r\n");
  }
  
  // get the name of sp_bt module
  uart_send_data(UART_NUM, "AT+NAME\r\n", strlen("AT+NAME\r\n")); //send AT order
  msleep(100);
  ret = uart_receive_data(UART_NUM, rcv_buf, sizeof(rcv_buf)); //receive response
  if(ret != 0 && strstr(rcv_buf, "NAME"))
  {
     printk(LOG_COLOR_W "get name success!\r\n");
  }
  ```

* MaixPy 示例

  ```python
  #change the name of sp_bt module to MAIXCUBE
  uart.write("AT+NAMEMAIXCUBE\r\n") #send AT order
  time.sleep_ms(100)
  read_data = uart.read() #receive response
  if read_data:
      read_str = read_data.decode('utf-8')
      count = read_str.count("OK")
      if count != 0:
          uart.write("set name success\r\n")
  
  # get the name of sp_bt module
  uart.write("AT+NAME\r\n") #send AT order
  time.sleep_ms(100)
  read_data = uart.read() #receive response
  if read_data:
      read_str = read_data.decode('utf-8')
      count = read_str.count("NAME")
      if count != 0:
          uart.write("get name success\r\n")
  ```

*注意发送AT指令后一定要加上\r\n*

## 运行结果

使用[BLE Utility](bledebugger.apk)连接设备后进行收发测试结果如下:

<center class="third">
	<img src="img/res.png" height="250"/><img src="img/res1.png" height="250"/>
</center>

## 运行环境

|  语言  |  开发板  |          SDK/固件版本          |
| :----: | :------: | :----------------------------: |
|   C    | MaixCube | kendryte-standalone-sdk v0.5.6 |
| MaixPy | MaixCube |         maixpy v0.5.1          |

## 许可

请查看 [LICENSE](LICENSE.md) 文件.

## 相关信息

| 版本号 |   编辑人   |
| :----: | :--------: |
|  v0.1  | vamoosebbf |
