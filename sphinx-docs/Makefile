# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
# -j auto enables parallel builds (override with SPHINXOPTS= for serial)
SPHINXOPTS    ?= -j auto
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Build Spanish HTML: compile .po to .mo first, then build with language=es
html-es:
	sphinx-intl build -d locale
	$(SPHINXBUILD) -b html -D language=es "$(SOURCEDIR)" "$(BUILDDIR)/html-es" $(SPHINXOPTS) $(O)

.PHONY: help html-es Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
