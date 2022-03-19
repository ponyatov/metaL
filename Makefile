# \ var
MODULE  = $(notdir $(CURDIR))
OS      = $(shell uname -o|tr / _)
NOW     = $(shell date +%d%m%y)
REL     = $(shell git rev-parse --short=4 HEAD)
BRANCH  = $(shell git rev-parse --abbrev-ref HEAD)
PEPS    = E26,E302,E305,E401,E402,E701,E702
# / var

# \ tool
CURL    = curl -L -o
CF      = clang-format-11 -style=file -i
PY      = $(shell which python3)
PIP     = $(shell which pip3)
PEP     = $(shell which autopep8) --ignore=$(PEPS) --in-place
# / tool

# \ src
Y += $(MODULE).py
Y += $(MODULE).meta.py metaL.py
S += $(Y)
# / src

# \ all
all: $(PY) $(MODULE).py
	$^
	$(MAKE) tmp/format_py

meta: $(PY) $(MODULE).meta.py
	$^
	$(MAKE) tmp/format_py
# / all

# \ format
tmp/format_py: $(Y)
	$(PEP) $? && touch $@
# / format

# \ install
.PHONY: install update
install: $(OS)_install
	$(MAKE) update

update: $(OS)_update
	$(PIP) install --user -U pip autopep8 pytest

.PHONY: GNU_Linux_install GNU_Linux_update
GNU_Linux_install GNU_Linux_update:
	sudo apt update
	sudo apt install -u `cat apt.txt`
# / install

# \ merge
MERGE  = Makefile README.md .gitignore apt.txt .clang-format $(S)
MERGE += .vscode bin doc lib src tmp
MERGE += requirements.txt

.PHONY: dev shadow release zip

dev:
	git push -v
	git checkout $@
	git pull -v
	git checkout shadow -- $(MERGE)

shadow:
	git push -v
	git checkout $@
	git pull -v

ZIP = tmp/$(MODULE)_$(BRANCH)_$(NOW)_$(REL).src.zip
zip:
	git archive --format zip --output $(ZIP) HEAD
	$(MAKE) doxy ; zip -r $(ZIP) docs
# / merge
