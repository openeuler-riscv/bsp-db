# A210 固件升级

## 前置条件

### 硬件

参阅对应的板卡配件要求。

### 软件

- 电脑端已安装 Android ADB 工具。

## 操作流程

### 获取固件文件

下载本镜像关联的固件压缩包，解压得到如下三个文件：

- `bootzero-rvbl.bin`
- `binman-spl-with-fit-rvbl.bin`
- `binman-emmc_boot-loader.img`

### 启动板卡至 Fastboot 模式

1. 使用对应的 USB 线缆连接板卡至电脑
2. 板卡接入 DC12V 电源
3. 短摁 K3 (PWR) 按钮
4. 摁住 K1 (LOAD) 按钮
5. 短摁 K2 (RESET) 按钮
6. 松开 K1 (LOAD) 按钮

此时在电脑端执行如下命令：

```shell
fastboot devices
```

应当得到如下输出（或有不同）：

```
????????????	 fastboot
```

### 配置驱动程序

#### Linux

同一台电脑只需配置一次。

执行下述命令完成 udev 配置：

```shell
cat << EOF | sudo tee /etc/udev/rules.d/99-zhihe-a210.rules
SUBSYSTEM=="usb", ATTR{idVendor}=="37f2", ATTR{idProduct}=="d00d", MODE="0660", GROUP="plugdev", TAG+="uaccess"
EOF
```

完成后重新插拔 USB线以使配置生效。

#### Windows

TBD

### 烧写固件

确保当前目录下存在上述固件文件。

执行下述命令完成烧写：

```shell
fastboot flash ram bootzero-rvbl.bin && fastboot reboot && fastboot flash ram binman-spl-with-fit-rvbl.bin && fastboot reboot
sleep 3
fastboot flash mmc0boot0 binman-emmc_boot-loader.img
```

### 烧写系统镜像

此步骤为可选。此时也可以完成系统镜像烧写。

#### 解压系统镜像

下载得到的镜像经过了压缩，无法直接烧录至设备。

##### Linux

可使用命令行 zstd 工具完成解压：

```shell
zstd -d openEuler-*.img.sparse.zstd
```

#### 烧写系统镜像

确保当前目录下存在 `openEuler-*.img.sparse` 文件

执行下述命令：

```shell
# Replace FILENAME.img.sparse with actual system image file name
fastboot flash mmc0 FILENAME.img.sparse
```

> 得到的镜像如果烧录不进去可能需要经过 `img2simg` 转换成 Android 的压缩格式.

### 完成烧录

此时可以对设备下电。

也可以短摁 K2 (RESET) 按钮正常开机并进入系统。

默认用户名为 `root`

默认密码为 `openEuler12#$`
