EULACEUIA_DIR := $(fetch_last_dir)

DISTROS += $(EULACEUIA_DIR)/distro.yml

include $(EULACEUIA_DIR)/23h1/release.mk
