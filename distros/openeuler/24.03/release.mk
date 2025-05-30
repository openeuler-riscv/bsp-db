OPENEULER_24.03_DIR := $(patsubst %/,%,$(dir $(lastword $(MAKEFILE_LIST))))

DISTRO_RELEASES += $(OPENEULER_24.03_DIR)/release-info.yml
IMAGESUITES += $(OPENEULER_24.03_DIR)/imagesuites/lpi4a-official-uboot.yml
IMAGESUITES += $(OPENEULER_24.03_DIR)/imagesuites/qemu-virt.yml
IMAGESUITES += $(OPENEULER_24.03_DIR)/imagesuites/sg2042-official-linuxboot.yml
IMAGESUITES += $(OPENEULER_24.03_DIR)/imagesuites/sg2042-official-uefi.yml
