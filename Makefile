ROOT_DIR := $(patsubst %/,%,$(dir $(lastword $(MAKEFILE_LIST))))
ifdef O
OUTPUT_DIR := $(O)
else
OUTPUT_DIR := ./build
endif

.PHONY: default
default: all

dir_guard=@mkdir -p $(@D)

# Provided by *.mk from subdirectories
BOARDS =
SOCS =
VENDORS =
DISTROS =
DISTRO_RELEASES =
IMAGESUITES =

include $(ROOT_DIR)/products/products.mk
include $(ROOT_DIR)/distros/distros.mk

# Intermediate target definition for yaml schema validating
ALL_BOARDS_VALIDATION := $(addsuffix .board.validate,$(BOARDS))
ALL_SOCS_VALIDATION := $(addsuffix .soc.validate,$(SOCS))
ALL_VENDORS_VALIDATION := $(addsuffix .vendor.validate,$(VENDORS))
ALL_DISTRO_REL_VALIDATION := $(addsuffix .distro_rel.validate,$(DISTRO_RELEASES))
ALL_DISTROS_VALIDATION := $(addsuffix .distros.validate,$(DISTROS))
ALL_IMAGESUITES_VALIDATION := $(addsuffix .imagesuite.validate,$(IMAGESUITES))

.PHONY: $(ALL_BOARDS_VALIDATION)
$(ALL_BOARDS_VALIDATION): %.board.validate: %
	./scripts/validate.py -s schema/board.yml $^
.PHONY: $(ALL_SOCS_VALIDATION)
$(ALL_SOCS_VALIDATION): %.soc.validate: %
	./scripts/validate.py -s schema/soc.yml $^
.PHONY: $(ALL_VENDORS_VALIDATION)
$(ALL_VENDORS_VALIDATION): %.vendor.validate: %
	./scripts/validate.py -s schema/vendor.yml $^
.PHONY: $(ALL_DISTRO_REL_VALIDATION)
$(ALL_DISTRO_REL_VALIDATION): %.distro_rel.validate: %
	./scripts/validate.py -s schema/distro_release.yml $^
.PHONY: $(ALL_DISTROS_VALIDATION)
$(ALL_DISTROS_VALIDATION): %.distros.validate: %
	./scripts/validate.py -s schema/distro.yml $^
.PHONY: $(ALL_IMAGESUITES_VALIDATION)
$(ALL_IMAGESUITES_VALIDATION): %.imagesuite.validate: %
	./scripts/validate.py -s schema/imagesuite.yml $^

.PHONY: validate
validate:	$(ALL_BOARDS_VALIDATION) \
			$(ALL_SOCS_VALIDATION) \
			$(ALL_VENDORS_VALIDATION) \
			$(ALL_DISTRO_REL_VALIDATION) \
			$(ALL_IMAGESUITES_VALIDATION) \
			$(ALL_DISTROS_VALIDATION)

ALL_BOARDS_JSON := $(patsubst %.yml,%.json,$(addprefix $(OUTPUT_DIR)/,$(BOARDS)))
# Always rebuild board level json, to satisfy imagesuite.parse
.PHONY: $(ALL_BOARDS_JSON)
$(ALL_BOARDS_JSON): $(OUTPUT_DIR)/%.json: %.yml
	$(dir_guard)
	./scripts/gen_board_json.py -i $^ -o $@
.PHONY: per_board_info
per_board_info: $(ALL_BOARDS_JSON)
ALL_IMAGESUITE_PARSE := $(addsuffix .imagesuite.parse,$(IMAGESUITES))
.PHONY: $(ALL_IMAGESUITE_PARSE)
$(ALL_IMAGESUITE_PARSE): %.imagesuite.parse : % per_board_info
	./scripts/parse_imagesuite.py -i $* -j $(OUTPUT_DIR)
.PHONY: per_imagesuite_info
per_imagesuite_info: $(ALL_IMAGESUITE_PARSE)
	rm -f $(addsuffix .lock,$(ALL_BOARDS_JSON))
.PHONY: per_board_json
per_board_json: per_board_info per_imagesuite_info
.PHONY: per_board_json_clean
per_board_json_clean:
	rm -f $(ALL_BOARDS_JSON)

$(OUTPUT_DIR)/boards.json: per_board_json
	$(dir_guard)
	./scripts/gen_board_list_json.py -o $(OUTPUT_DIR)/boards.json -r $(OUTPUT_DIR) $(ALL_BOARDS_JSON)
.PHONY: boards_list_json
boards_list_json: $(OUTPUT_DIR)/boards.json
.PHONY: boards_list_json_cleanup
boards_list_json_cleanup: per_board_json_clean
	rm -f $(OUTPUT_DIR)/boards.json

.PHONY: json
json: boards_list_json per_board_json
.PHONY: json_cleanup
json_cleanup: boards_list_json_cleanup

.PHONY: resources
resources:
	rsync -avh ./resources $(OUTPUT_DIR)
.PHONY: resource_cleanup
resource_cleanup:
	rm -rf "$(OUTPUT_DIR)/resources"

.PHONY: docs
docs:
	rsync -avh ./docs $(OUTPUT_DIR)
.PHONY: docs_cleanup
docs_cleanup:
	rm -rf "$(OUTPUT_DIR)/docs"

.PHONY: clean
clean: json_cleanup resource_cleanup docs_cleanup

.PHONY: all
all: json resources docs
