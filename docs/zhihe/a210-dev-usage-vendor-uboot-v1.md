# 操作说明

## 物料准备

- DC5525 12V 电源
- USB A to A 公对公连接线
  - 固件刷写
- \[可选] 串口适配器
  - 建议使用 1.8V 逻辑电平
  - 监看 Bootloader 的调试输出、选择系统启动项
  - 操作系统默认串口终端
- 计算机
  - 运行 Linux 发行版、macOS 或 Windows
  - 已安装 fastboot 工具
  - \[可选] 已安装串口终端工具
    - puTTY、minicom 等
  - 已安装压缩包解压工具
    - 支持 zstd、zip 格式
  - 具备至少一个 USB 2.0 及以上的端口

## 硬件准备

将板卡上靠近 DC12V 电源插口的 USB A 口通过公对公数据线连接至计算机。

使用 DC12V 电源为板卡供电。

## 烧写固件

下载文件列表中标记为「固件」的条目并解压，得到下列文件：

- `binman-emmc_boot-loader.img`
- `binman-spl-with-fit-rvbl.bin`
- `bootzero-rvbl.bin`

执行下述操作使板卡进入 fastboot 刷写状态：

1. 短摁 K3 (PWR) 按钮，2.54mm 排针附近的红色 LED 熄灭，板卡进入正常启动流程
2. 摁住 K1 (LOAD) 按钮
3. 短摁 K2 (RESET) 按钮
4. 松开 K1 (LOAD) 按钮

此时计算机端应当能识别到 fastboot 设备。

在计算机端执行下述命令：

```shell
fastboot flash ram bootzero-rvbl.bin && \
  fastboot reboot && \
  fastboot flash ram binman-spl-with-fit-rvbl.bin && \
  fastboot reboot
sleep 3
fastboot flash mmc0boot0 binman-emmc_boot-loader.img
```

此时已完成固件刷写。若想继续部署系统镜像则不要将板卡下电。

## 系统镜像部署

A210 目前仅支持从 eMMC 启动。继续执行下述命令完成系统镜像刷写。需要替换为正确的文件名：

```shell
fastboot flash mmc0 xxxx-Zhihe-A210-extlinux.img
```
