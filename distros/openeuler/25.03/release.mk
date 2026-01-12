OPENEULER_25.03_DIR := $(fetch_last_dir)

DISTRO_RELEASES += $(OPENEULER_25.03_DIR)/release-info.yml
IMAGESUITES += $(wildcard $(OPENEULER_25.03_DIR)/imagesuites/*.yml)
