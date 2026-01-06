# 参考：物料准备

## 硬件工具

- USB Type-C 电源
  - 为板卡供电
- USB A to A （公对公）数据线
  - 用于固件与系统镜像烧写
  - 反接的 A to C 线材可能不工作
- 串口适配器
  - 建议使用 3.3V 逻辑电平
  - 监看 Bootloader 的调试输出、选择系统启动项
  - 操作系统默认串口终端
- 计算机
  - 运行 Linux 发行版、macOS 或 Windows
  - 具备足够数量的 USB 2.0 及以上的端口

## 固件加载源配置

板卡固件加载源不可配置。仅能从板载 eMMC 加载固件与系统。

## 进入 fastboot 烧录模式

1. 将板卡上白色的 USB A 端口通过 Type-A 数据线连接至计算机
2. 摁住板卡上的按钮
3. 使用 Type-C 电源为板卡供电
4. 松开板卡上的按钮

若此时连接了板卡调试串口，则可以观察到如下输出：

```
sys: 0x1000
bm:2
ROM: usb download handler
usb2d_initialize : enter
Controller Run
usb rst int
SETUP: 0x80 0x6 0x100
usb rst int
SETUP: 0x0 0x5 0x20
SETUP: 0x80 0x6 0x100
SETUP: 0x80 0x6 0x200
SETUP: 0x80 0x6 0x200
SETUP: 0x80 0x6 0x300
SETUP: 0x80 0x6 0x302
SETUP: 0x80 0x6 0x301
SETUP: 0x80 0x6 0x30a
SETUP: 0x0 0x9 0x1
usb_rx_bytes : len= 4096 pBuf= 0xc0838720
SETUP: 0x80 0x6 0x302
SETUP: 0x80 0x6 0x304
```
