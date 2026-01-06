# 系统部署：SD 卡启动

本文档描述了如何使用 SD 卡系统镜像。

## 软件准备

- 电脑上需安装有压缩包解压软件
  - 需要支持下列文件格式
    - zstd

## 镜像烧写

下载并解压文件列表中标记为“SDMMC镜像”的文件，得到后缀为 `.img` 的可烧录镜像。

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
