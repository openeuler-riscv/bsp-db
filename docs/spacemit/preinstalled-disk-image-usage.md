# 使用预安装磁盘镜像

## 使用条件

板卡应当已刷写过一次兼容的固件。

对于大多数情况，过去刷写的老版本固件仍能够支持最新版本系统镜像。

## 使用说明

下载文件列表中标记为“系统”的文件。

解压该压缩文件，将会得到一个包含分区表在内的完整磁盘镜像，可以被恢复至受支持的存储媒介。

可以使用下列以及更多未列出的工具来进行镜像还原：

- [balenaEtcher](https://etcher.balena.io/#download-etcher)
- `dd`
- `gnome-disks`

默认用户为：

```
root
```

默认密码为：

```
openEuler12#$
```

## 参考命令

##### 使用 dd 命令进行镜像还原

```shell
dd if=xxx.img of=/dev/sdx oflag=direct conv=sync status=progress bs=4096
eject /dev/sdx
```
