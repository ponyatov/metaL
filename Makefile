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
