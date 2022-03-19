# \ var
MODULE  = $(notdir $(CURDIR))
OS      = $(shell uname -o|tr / _)
NOW     = $(shell date +%d%m%y)
REL     = $(shell git rev-parse --short=4 HEAD)
BRANCH  = $(shell git rev-parse --abbrev-ref HEAD)
PEPS    = E26,E302,E305,E401,E402,E701,E702
# / var

# \ version
JQUERY_VER = 3.6.0
# / version

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

.PHONY: web
web: $(PY) $(MODULE).meta.py
	$^ $@
	$(MAKE) tmp/format_py
	$(MAKE) -C $@ gz
# / all

# \ format
tmp/format_py: $(Y)
	$(PEP) $? && touch $@
# / format

# \ install
.PHONY: install update
install: $(OS)_install gz
	$(MAKE) update

update: $(OS)_update
	$(PIP) install --user -U pip autopep8 pytest

.PHONY: GNU_Linux_install GNU_Linux_update
GNU_Linux_install GNU_Linux_update:
	sudo apt update
	sudo apt install -u `cat apt.txt`

# \ gz
.PHONY: gz
gz: static/jquery.js

CDNJS = https://cdnjs.cloudflare.com/ajax/libs

static/jquery.js:
	$(CURL) $@ $(CDNJS)/jquery/$(JQUERY_VER)/jquery.min.js
# / gz
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
