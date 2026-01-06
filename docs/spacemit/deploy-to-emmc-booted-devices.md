# 系统部署：eMMC 启动

本文档描述了如何在使用 eMMC 同时作为固件和操作系统存储器的板卡上部署系统。

## 计算机端软件准备

- fastboot 工具与驱动
  - 参阅「安装 Android SDK Platform-Tools」
  - 参阅 「fastboot 驱动配置」
- 压缩包解压软件
  - 需要支持下列文件格式
    - zip
    - zstd
- \[可选] 串口终端工具

## 固件与系统刷写

### 文件准备

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

参考 「物料准备」，将板卡配置为 eMMC 启动。

### 配置板卡进入 fastboot 模式

参考 「物料准备」

### 执行烧写

执行下述命令将固件写入 eMMC：

```shell
fastboot stage FSBL.bin
fastboot continue
sleep 1
fastboot stage u-boot.itb
fastboot continue
sleep 1
fastboot flash bootinfo bootinfo_sd.bin
fastboot flash fsbl FSBL.bin
```

下载并解压文件列表中标记为“SDMMC镜像”的文件。

执行下述命令烧写系统镜像。需要替换为正确的文件名：

```shell
fastboot flash mmc2 xxx-sdmmc.img
```
