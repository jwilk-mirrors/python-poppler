# require automake-1.7
AUTOMAKE_OPTIONS=1.7

INCLUDES = $(PYTHON_INCLUDES)

EXTRA_DIST = poppler.defs poppler.override arg-types.py

# poppler module
pyexec_LTLIBRARIES = popplermodule.la
popplermodule_la_LDFLAGS = -module -avoid-version -export-symbols-regex initpoppler
popplermodule_la_CFLAGS = $(PYPOPPLER_CFLAGS)
popplermodule_la_LIBADD = $(PYPOPPLER_LIBS)
popplermodule_la_SOURCES = popplermodule.c 
nodist_popplermodule_la_SOURCES = poppler.c
poppler.c: poppler.defs poppler.override
CLEANFILES = poppler.c

.defs.c:
	(cd $(srcdir)\
	&& $(PYTHON) $(CODEGEN) \
		--override $*.override \
	    --register @PYGTK_DATADIR@/pygtk/2.0/defs/gdk-types.defs \
	    --register @PYGTK_DATADIR@/pygtk/2.0/defs/pango-types.defs \
	    --register @PYGTK_DATADIR@/pygtk/2.0/defs/gtk-types.defs \
		--prefix py$* $*.defs) > gen-$*.c \
	    && cp gen-$*.c $*.c \
	    && rm -f gen-$*.c
