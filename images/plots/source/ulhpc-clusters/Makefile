export SHELL=/usr/bin/bash

TARGETS=$(patsubst %.tex, %, $(wildcard *.tex))

BUILD_DIR=build
OUTPUT_DIR=$(BUILD_DIR)/output
AUXILIA_DIR=$(BUILD_DIR)/auxilia
SCRATCH_DIR=$(BUILD_DIR)/_scratch_

LATEXMK=latexmk $(LATEXMK_FLAGS) -emulate-aux-dir -output-directory=$(OUTPUT_DIR) -aux-directory=$(AUXILIA_DIR)
#LATEXMK=latexmk -jobname=$(OUTPUT_PATH) # Do not use to redirect output to new directory
ARGS='$$pdflatex=q/xelatex %O -synctex=1 -shell-escape %S/'
PREVIEW='$$pdf_previewer=q/start evince %S/'

.PHONY: all
all: $(TARGETS)

.PHONY: build_dir
build_dir: | $(BUILD_DIR)
build_dir: scratch_dir

$(BUILD_DIR):
	mkdir -p "$(BUILD_DIR)"

.PHONY: scratch_dir
scratch_dir: | $(BUILD_DIR)/_scratch_ $(BUILD_DIR)/_scratch_/tikz $(AUXILIA_DIR)/$(BUILD_DIR)/_scratch_/tikz

$(BUILD_DIR)/_scratch_: | $(BUILD_DIR)
	mkdir "$(BUILD_DIR)/_scratch_"

$(BUILD_DIR)/_scratch_/tikz: | $(BUILD_DIR)/_scratch_
	mkdir "$(BUILD_DIR)/_scratch_/tikz"

# Directory to hold the md5 hashes; must mirror location of tikzexternalize prefix option
$(AUXILIA_DIR)/$(BUILD_DIR)/_scratch_/tikz: | $(AUXILIA_DIR)/$(BUILD_DIR)/_scratch_
	mkdir "$(AUXILIA_DIR)/$(BUILD_DIR)/_scratch_/tikz"

$(AUXILIA_DIR)/$(BUILD_DIR)/_scratch_: | $(AUXILIA_DIR)/$(BUILD_DIR)
	mkdir "$(AUXILIA_DIR)/$(BUILD_DIR)/_scratch_"

$(AUXILIA_DIR)/$(BUILD_DIR): | $(AUXILIA_DIR)
	mkdir "$(AUXILIA_DIR)/$(BUILD_DIR)"

$(AUXILIA_DIR) : | $(BUILD_DIR)
	mkdir "$(AUXILIA_DIR)"

.PHONY: $(TARGETS)
$(TARGETS): % : $(OUTPUT_DIR)/%.pdf

define latexmk=
	$(eval TARGET=$(1))
	$(eval DEPENDENCY_LIST_FILE=$(2))
	$(eval OPTIONS=$(subst $$, $$$$, $(3)))
	$(LATEXMK) $(OPTIONS) -pdf -M -MP -MF $(DEPENDENCY_LIST_FILE) $(TARGET)
endef

.PHONY: $(patsubst %, $(OUTPUT_DIR)/%.pdf, $(TARGETS))
$(patsubst %, $(OUTPUT_DIR)/%.pdf, $(TARGETS)) : | build_dir
$(patsubst %, $(OUTPUT_DIR)/%.pdf, $(TARGETS)) : $(OUTPUT_DIR)/%.pdf : %.tex
	$(call latexmk, $<, $(patsubst %.tex, $(SCRATCH_DIR)/%.depends, $<), -e $(ARGS))

.PHONY: install
install: $(patsubst %, install-%, $(TARGETS))

.PHONY: uninstall
uninstall: $(patsubst %, uninstall-%, $(TARGETS))

define install_target=
$(eval TARGET=$(1))

.PHONY: install-$(TARGET)
install-$(TARGET): $(TARGET).pdf

$(TARGET).pdf: $(OUTPUT_DIR)/$(TARGET).pdf
	cp $(OUTPUT_DIR)/$(TARGET).pdf $(TARGET).pdf
endef

define uninstall_target=
$(eval TARGET=$(1))

.PHONY: uninstall-$(TARGET)
uninstall-$(TARGET):
	if [ -f $(TARGET).pdf ]; then rm $(TARGET).pdf; fi
endef

$(foreach target, $(TARGETS), $(eval $(call install_target, $(target))))
$(foreach target, $(TARGETS), $(eval $(call uninstall_target, $(target))))

define view_target=
$(eval TARGET=$(1))

.PHONY: view-$(TARGET)
view-$(TARGET): $(OUTPUT_DIR)/$(TARGET).pdf
	okular $(OUTPUT_DIR)/$(TARGET).pdf 1>/dev/null 2>&1 &
endef

$(foreach target, $(TARGETS), $(eval $(call view_target, $(target))))

define track_target=
$(eval TARGET=$(1))

.PHONY: track-$(TARGET)
track-$(TARGET) : | build_dir
track-$(TARGET) : $(TARGET).tex
	$(call 	latexmk, $(TARGET).tex, $(SCRATCH_DIR)/$(TARGET).depends, -e $$(ARGS) -pvc)
endef

$(foreach target, $(TARGETS), $(eval $(call track_target, $(target))))

define trackview_target=
$(eval TARGET=$(1))

.PHONY: trackview-$(TARGET)
trackview-$(TARGET) : | build_dir
trackview-$(TARGET) : $(TARGET).tex
	$(call 	latexmk, $(TARGET).tex, $(SCRATCH_DIR)/$(TARGET).depends, -e $$(ARGS) -e $$(PREVIEW) -pvc)
endef

$(foreach target, $(TARGETS), $(eval $(call trackview_target, $(target))))

.PHONY: remove-output
remove-output: $(patsubst %, remove-%, $(TARGETS))

define remove_target=
$(eval TARGET=$(1))

.PHONY: remove-$(TARGET)
remove-$(TARGET):
	if [ -f $(OUTPUT_DIR)/$(TARGET).pdf ]; then rm $(OUTPUT_DIR)/$(TARGET).pdf; fi
endef

$(foreach target, $(TARGETS), $(eval $(call remove_target, $(target))))

.PHONY: remove-intermediary
remove-intermediary:
	$(LATEXMK) -C

.PHONY: remove-all
remove-all:
	$(LATEXMK) -c

.PHONY: clean
clean:
	@echo "Removing files:"
	@if [ -d $(BUILD_DIR) ]; then \
		 find $(BUILD_DIR) -type f -print0 | xargs -0I % bash -c '{ echo "%"; rm "%"; }'; \
		 rm -r $(BUILD_DIR); \
	fi
	@echo 'Removing gnuplottex scratch directory:'
	@if [ -d gnuplottex ]; then \
		ls -d gnuplottex; \
		rm -r gnuplottex; \
	fi
