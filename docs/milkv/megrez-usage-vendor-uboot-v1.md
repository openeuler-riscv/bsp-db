# 操作说明

## 物料准备

- USB Type-C 数据线缆
  - 连接板载的 USB 转串口并监看板卡调试终端
  - 固件烧写
- DC5525 12V 电源适配器
- 计算机
  - 运行 Linux 发行版或 Windows
    - macOS 不被支持
  - 已安装 fastboot 工具
  - 已安装串口终端工具
    - puTTY、minicom 等
  - 已安装压缩包解压工具
    - 支持 zstd 格式
  - 具备至少一个 USB 2.0 及以上的端口

## 配置板卡进入固件烧写模式

将板卡 DC 电源口旁边的开关拨至 RECOVERY 侧。

连接 DC 电源口旁边的 Type-C 接口至计算机。操作系统应当枚举到一个 USB 串口适配器设备。该设备即为板卡的调试串口。

> 在 Linux 下该设备会被注册为 `/dev/ttyUSBx`；在 Windows 设备管理器中会被识别为「端口（COM 和 LPT）」设备。

使用计算机端的串口终端工具连接板卡的调试串口，并监看其输出。

此时给板卡接入 12V DC 电源。计算机端此时会新枚举到一个 USB 大容量存储设备。

## 烧写固件

下载文件列表中标记为「固件」的条目并解压，得到后缀为 `.bin` 的固件文件。

### 从 RAM 临时运行新固件

将该文件复制进枚举到的 USB 大容量存储设备。

在 Linux 下推荐执行手动 mount 后再 cp 拷贝的流程。假定设备识别为 `/dev/sdx`，则执行下述命令：

> 当心此处的 sudo

```shell
EIC7700_USBDEV="/dev/sda"
TMP_MNT=$(mktemp -d) && sudo mount "${EIC7700_USBDEV}" "${TMP_MNT}" && sudo cp bootloader-milkv_megrez.bin "${TMP_MNT}" && sudo umount "${TMP_MNT}" && unset TMP_MNT
```

在 Windows 下使用资源管理器复制进去即可。

macOS 由于 finder 行为的原因，无法成功进行这一步。

完成复制后，串口终端将会打印：

```
pll config ok
die_num:0,die_ordinal:0
Firmware version:1.5;disable ECC
PHY0 training process:100%
PHY1 training process:100%
DDR type:LPDDR5;Size:32GB,Data Rate:6400MT/s
DDR self test OK
```

在这里会卡顿一段时间，而后将会进入 OpenSBI 与 U-Boot：

```
eUSB:
srOrpoern SinB Is uv1b.m3i
 si  o n:__ _e_p1 2  9  -  - >   - 2 2

- U S B :  b _u_lk____in ___co__m p_l_e_t_e _-
 >   /- 2_2,_  \0 /1 3
                                      / ____|  _ \_   _|
 | |  | |_ __   ___ _ __ | (___ | |_) || |
 | |  | | '_ \ / _ \ '_ \ \___ \|  _ < | |
 | |__| | |_) |  __/ | | |____) | |_) || |_
  \____/| .__/ \___|_| |_|_____/|___/_____|
        | |
        |_|

Platform Name             : ESWIN EIC770X
Platform Features         : none
Platform HART Count       : 4
Platform IPI Device       : aclint-mswi
Platform Timer Device     : aclint-mtimer @ 1000000Hz
Platform Console Device   : uart8250
Platform HSM Device       : ---
Platform PMU Device       : ---
Platform Reboot Device    : eswin_eic770x_reset
Platform Shutdown Device  : eswin_eic770x_reset
Platform Suspend Device   : eswin_eic770x_suspend
Platform CPPC Device      : ---
Firmware Base             : 0x80000000
Firmware Size             : 344 KB
Firmware RW Offset        : 0x40000
Firmware RW Size          : 88 KB
Firmware Heap Offset      : 0x4c000
Firmware Heap Size        : 40 KB (total), 2 KB (reserved), 9 KB (used), 29 KB (free)
Firmware Scratch Size     : 4096 B (total), 736 B (used), 3360 B (free)
Runtime SBI Version       : 1.0
```

### 将固件烧写至 Flash

此时，计算机端的串口终端工具已连接至板卡上临时运行于 RAM 中的 U-Boot 的 shell。

> 下述操作在板卡串口终端中执行

```shell
fastboot usb 0
```

使板卡启动标准 fastboot 服务。

若计算机使用 Windows 操作系统，则需要为 USB 枚举到的新设备配置 fastboot 驱动程序。

在计算机端执行下述命令，将固件文件传输至板卡 RAM：

> 下述操作在计算机操作系统 shell 中执行

```shell
fastboot stage bootloader-milkv_megrez.bin
```

> 下述操作在板卡串口终端中执行

传输完成后，在板卡串口终端中摁下 `CTRL` + `C` 组合键，打断 fastboot 服务。

再在板卡串口终端中执行下述命令，完成固件烧写：

```shell
es_burn write 0x90000000 flash
```

执行完毕后，将板卡下电，并重新将板卡 DC 电源口旁边的开关拨至 NORMAL 侧。

## 系统镜像部署

Megrez 支持从下列存储设备启动:
- USB
- SATA
  - M.2 B+M Key
  - SATA 连接器
- PCIe 转 NVMe
- SD卡

下载文件列表中标为「系统镜像」的条目，解压得到后缀为 `.img` 的镜像文件。将其烧录至对应存储设备后挂载至板卡上即可启动。
