# 手动进行固件全新安装

## 硬件准备

所需物料：

- SpacemiT MUSE Pi Pro 单板计算机
- USB Type-C 数据线缆
  - 规格 USB2.0 及以上
- \[可选] 串口适配器
  - 建议使用 3.3V 电平
- 一台能够运行 Windows、macOS 或 Linux 发行版的电脑
  - 需至少有一个兼容 USB2.0 的端口

## 软件准备

- 电脑上需安装有 fastboot 工具
  - 来自于 [Android SDK Platform-Tools](https://developer.android.com/tools/releases/platform-tools)
  - 参阅「安装 Android SDK Platform-Tools」
- 电脑上需安装有压缩包解压软件
  - 需要支持下列文件格式
    - zstd
    - zip
- 下载文件列表中标记为“固件”的文件

## 驱动程序配置

### Linux

> 在相同系统下仅需进行一次配置

需通过 udev 配置设备权限。执行下述命令：

```shell
cat << EOF | sudo tee /etc/udev/rules.d/72-spacemit-k1.rules
SUBSYSTEM=="usb", ATTR{idVendor}=="361c", ATTR{idProduct}=="1001", TAG+="uaccess"
EOF
```

将 SpacemiT K1 使用的 USB IDs 配置为用户可访问。

### macOS

无需特殊配置

### Windows

参考 「在 Windows 上配置 Android USB 驱动」

## 固件刷写

### 文件准备

解压固件压缩包，得到如下文件：

- `bootinfo_sd.bin`
- `bootinfo_spinor.bin`
- `FSBL.bin`
- `fw_dynamic.itb`
- `partition-mtd.json`
- `partition-sdmmc.json`
- `u-boot.itb`
- `u-boot-env-default.bin`

### 配置板卡进入 fastboot 模式

将板卡通过 USB 数据线连接至电脑。通过下述操作进入 fastboot 模式：

1. 摁住 FDL 按钮
2. 短摁 FDL 旁边的 RST 按钮
3. 松开 FDL 按钮

此时在电脑上执行下述命令，检查是否已经成功识别：

```shell
fastboot devices
```

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
