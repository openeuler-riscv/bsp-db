# 操作说明

## 物料准备

- DC5525 12V 电源
- USB Type-C 数据线缆
  - 连接至板卡调试串口
- USB A to A 公对公连接线
  - 固件刷写
- 计算机
  - 运行 Linux 发行版或 Windows
    - macOS 不被支持
  - 已安装 fastboot 工具
  - 已安装串口终端工具
    - puTTY、minicom 等
  - 已安装压缩包解压工具
    - 支持 zstd 格式
  - 具备至少两个 USB 2.0 及以上的端口

## 硬件准备

调节板卡上标记为 SW2 的 4 位拨码开关。

将 1、2 位拨至背离 ON 标记的一侧；将 3、4 位拨至靠近 ON 标记的一侧。

> 板卡默认未开启 security mode。将 boot cpu 配置为 SCPU，执行片上 BootROM，并使能 USB 烧录功能。

将板卡上的 Type-C 接口使用数据线缆连接至计算机。计算机将会识别到 4 个 USB 串口适配器设备。其中第三个为板卡的调试串口。使用计算机端的串口终端工具监看其输出。

> 在 Linux 下，若第一个串口适配器被注册为 `/dev/ttyUSB0` ，则板卡调试串口会被注册为 `/dev/ttyUSB2`

> 在 Windows 设备管理器中会被识别为「端口（COM 和 LPT）」设备。需计算并使用正确的 COM 号。

将板卡上靠近以太网口的蓝色 USB A 端口通过数据线缆连接至计算机。

使用 DC 12V 电源为板卡供电，并将板卡上的电源开关拨至 On。此时计算机将枚举到一个 USB 大容量存储设备。

## 烧写固件

下载文件列表中标记为「固件」的条目并解压，得到后缀为 `.bin` 的固件文件。

### 从 RAM 临时运行新固件

将该文件复制进枚举到的 USB 大容量存储设备。

在 Linux 下推荐执行手动 mount 后再 cp 拷贝的流程。假定设备识别为 `/dev/sdx`，则执行下述命令：

> 当心此处的 sudo

```shell
EIC7700_USBDEV="/dev/sda"
TMP_MNT=$(mktemp -d) && sudo mount "${EIC7700_USBDEV}" "${TMP_MNT}" && sudo cp bootloader-eswin_eic7700_evb_a2.bin "${TMP_MNT}" && sudo umount "${TMP_MNT}" && unset TMP_MNT
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
DDR type:LPDDR5;Size:16GB,Data Rate:6400MT/s
DDR self test OK
```

在这里会卡顿一段时间，而后将会进入 OpenSBI 与 U-Boot：

```
eUSB:
srOrpore niSnB I svub1.m3i
 s i o n:_ __e_p 1 2 9   - - >   - 2 2

- U S B :   b_u_l_k___i n___c_o_m p_l_e_t_e_
 - >  -/2 2_,_  \0 /1 3
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
fastboot stage bootloader-eswin_eic7700_evb_a2.bin
```

> 下述操作在板卡串口终端中执行

传输完成后，在板卡串口终端中摁下 `CTRL` + `C` 组合键，打断 fastboot 服务。

再在板卡串口终端中执行下述命令，完成固件烧写：

```shell
es_burn write 0x90000000 flash
```

执行完毕后，关闭板卡电源开关。

重新调节板卡上标记为 SW2 的 4 位拨码开关。

将 2 位拨至背离 ON 标记的一侧；将 1、3、4 位拨至靠近 ON 标记的一侧。

> 板卡默认未开启 security mode。将 boot cpu 配置为 SCPU，执行片上 BootROM，并从 Flash 加载固件。

## 系统镜像部署

EVB A2 支持从下列存储设备加载操作系统：

- USB
- SATA
  - M.2 M Key
- PCIe 转 NVMe
- SD 卡

下载文件列表中标为「系统镜像」的条目，解压得到后缀为 `.img` 的镜像文件。将其烧录至 SD 卡后挂载至板卡上即可启动。
