# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile files

files: source/_static/dash.svg  source/_static/dash.pdf source/_static/arrows.svg  source/_static/arrows.pdf

%.py: ; 
source/_static/%.tex: %.py
	python3 -B $< --tex

source/_static/%.svg: %.py
	python3 -B $< 

source/_static/%.pdf: source/_static/%.tex
	pdflatex --output-directory source/_static/ $<  && rm source/_static/$*.log source/_static/$*.aux

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile 
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
