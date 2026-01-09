# 操作说明

## 物料准备

- USB Type-C PD 电源
- microSD 卡
  - 刷写固件
- 串口适配器
  - 建议使用 3.3V 逻辑电平
  - 刷写固件
  - 监看 Bootloader 的调试输出、选择系统启动项
  - 操作系统默认串口终端
- 计算机
  - 运行 Linux 发行版、macOS 或 Windows
  - \[可选] 已安装串口终端工具
    - puTTY、minicom 等
    - 需支持 xmodem 与 ymodem 协议
  - 已安装压缩包解压工具
    - 支持 zstd、zip 格式
  - 已安装镜像烧录工具

## 固件刷写

下载文件列表中标记为「固件包」的条目，解压得到如下文件：

- `u-boot.itb`
- `u-boot-env-default.bin`
- `u-boot-spl.bin.normal.out`

下载文件列表中标记为「固件升级镜像」的条目，解压得到可烧录的 `firmware_updater.sd.img` 镜像文件。

将该镜像刷写至 microSD 卡。

### 计算机操作系统为 Linux 发行版

#### 使用 minicom 作为串口终端工具

##### 配置 minicom

假设计算机端识别到的串口适配器设备为 `/dev/ttyUSB0`。

使用如下命令启动串口终端：

```shell
minicom -D /dev/ttyUSB0 -b 115200
```

将打印出如下内容：

```
Welcome to minicom 2.9

OPTIONS: I18n 
Port /dev/ttyACM0, 18:08:24

Press CTRL-A Z for help on special keys
```

根据提示可知 minicom 使用 `CTRL` + `A` 作为转义组合键。

执行下列操作确保串口参数正确：

1. 同时摁下 `CTRL` + `A` 后松开
2. 再次摁下 `O`，打开 `[configuration]` 菜单
3. 使用方向键选中 `Serial port setup` 并摁回车进入
   - 若 `F - Hardware Flow Control : No` 存在，该项必须为 `No`；否则摁下 `F` 切换其状态
   - 若 `G - Software Flow Control : No` 存在，该项必须为 `No`；否则摁下 `G` 切换其状态
   - 若 `H -     RS485 Enable      : No` 存在，该项必须为 `No`；否则摁下 `H` 切换其状态
4. 摁下 `E` 打开 `[Comm Parameters]` 菜单
5. 摁下 `Q` 选中 `8N1`
6. 摁下回车键返回上一级菜单
7. 再次摁下回车键返回 `[configuration]` 菜单
8. 使用方向键选中 `Exit` 并按下回车，退出菜单

##### 将板卡启动至串口模式

1. 装入刷写有固件升级镜像的 microSD 卡
2. 使用 Type-C 电源为板卡供电
3. 摁住板卡 USB A 口旁边的 UART BOOT 按钮
4. 摁住 PWR ON 按钮 1 秒钟以上，旁边的红色 LED 灯将亮起

 此时串口中将会打印：

```
(C)StarFive
CCCCCCCCCCCCCCCCCCCCCCCCCCCCC
```

##### 上传 SPL 固件

1. 同时摁下 `CTRL` + `A` 后松开
2. 摁下 `S` 打开 `[Upload]` 菜单
3. 使用方向键选中 `xmodem` 并摁下回车，打开文件选择菜单
   - 使用上下方向键选择列表中的条目
   - 双击空格进入选中的目录
   - 在 `[..]` 双击空格返回上一级目录
   - 单击空格选中 `u-boot-spl.bin.normal.out` 
4. 摁下回车，开始上传
5. 弹出上传进度菜单；当完成后，摁下回车退出菜单

串口将会打印出 U-Boot SPL 信息，并尝试继续从 microSD 卡启动：

```
U-Boot SPL 2025.07-g90e3284e5c30 (Dec 29 2025 - 02:07:11 +0000)
DDR version: dc2e84f0.
Trying to boot from MMC2

OpenSBI v1.7
   ____                    _____ ____ _____
  / __ \                  / ____|  _ \_   _|
 | |  | |_ __   ___ _ __ | (___ | |_) || |
 | |  | | '_ \ / _ \ '_ \ \___ \|  _ < | |
 | |__| | |_) |  __/ | | |____) | |_) || |_
  \____/| .__/ \___|_| |_|_____/|____/_____|
        | |
        |_|

Platform Name               : OrangePi RV
Platform Features           : medeleg
Platform HART Count         : 4
```

##### 继续执行自动更新

1. 绿色 LED 灯开始闪烁
   - 总共会亮起 3 次
   - 在最后一次熄灭之前断开板卡电源可以取消升级
2. 绿色 LED 灯熄灭，开始自动升级固件
3. 绿色 LED 灯再次亮起，固件升级完成
4. 给板卡下电，并拔出 microSD 卡。

### 计算机操作系统为 Windows

TBD

## 系统镜像部署

Mars 支持从下列存储媒介上加载操作系统：

- microSD
- M.2 NVMe
- USB

下载文件列表中标记为「系统镜像」的条目，解压得到后缀为 `.img` 的可烧录镜像文件。

将该镜像烧写至对应存储设备后，挂载到板卡上即可启动。
