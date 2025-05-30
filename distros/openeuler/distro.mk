OPENEULER_DIR := $(fetch_last_dir)

DISTROS += $(OPENEULER_DIR)/distro.yml

# Newest should be placed first
include $(OPENEULER_DIR)/24.03sp1/release.mk
include $(OPENEULER_DIR)/24.03/release.mk
