# 系统部署：Flash 启动

本文档描述了如何在使用 NOR Flash 作为固件存储器的板卡上部署系统。

## 计算机端软件准备

- fastboot 工具与驱动
  - 参阅「安装 Android SDK Platform-Tools」
  - 参阅 「fastboot 驱动配置」
- 压缩包解压软件
  - 需要支持下列文件格式
    - zip
    - zstd
- 镜像文件烧写工具
- \[可选] 串口终端工具

## 固件刷写

### 获取固件文件

下载并解压文件列表中标记为“固件”的条目，得到如下固件文件：

- `bootinfo_sd.bin`
- `bootinfo_spinor.bin`
- `FSBL.bin`
- `fw_dynamic.itb`
- `partition-mtd.json`
- `partition-sdmmc.json`
- `u-boot.itb`
- `u-boot-env-default.bin`

### 配置板卡固件加载源

参考 「物料准备」，将板卡配置为 Flash 启动。

### 配置板卡进入 fastboot 模式

参考 「物料准备」

### 执行烧写

执行下述命令将固件写入板载 NOR Flash：

```shell
fastboot stage FSBL.bin
fastboot continue
sleep 1
fastboot stage u-boot.itb
fastboot continue
sleep 1
fastboot flash mtd partition-mtd.json
fastboot flash mtd-bootinfo bootinfo_spinor.bin
fastboot flash mtd-fsbl FSBL.bin
fastboot flash mtd-opensbi fw_dynamic.itb
fastboot flash mtd-uboot u-boot.itb
fastboot flash mtd-env u-boot-env-default.bin
```

执行完毕后固件已被正确刷写。此时可以断开板卡与电脑的连接。

## 系统镜像刷写

下载文件列表中标记为“标准镜像”的文件。

### 外部 SD/NVMe/USB 作为系统盘

下载并解压文件列表中标记为“标准镜像”的条目，得到后缀为 `.img` 的可烧录镜像。

可以使用下列（或其他未列出的）工具来进行镜像还原：

- [balenaEtcher](https://etcher.balena.io/#download-etcher)
- [Win32 Disk Imager](https://sourceforge.net/projects/win32diskimager/)
- `dd`
- `gnome-disks`

典型的 dd 命令如下：

```shell
dd if=xxx.img of=/dev/sdx oflag=direct conv=sync status=progress bs=4096
eject /dev/sdx
```

### 板载 eMMC 作为系统盘

尚未支持。
