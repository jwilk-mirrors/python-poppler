
AUTOMAKE_OPTIONS = 1.7


DEFS=/usr/share/pygtk/2.0/defs

INCLUDES =                                      \
        $(PYTHON_INCLUDES)                      \
        $(POPPLER_CFLAGS)

pkgpyexecdir = $(pythondir)

pkgpyexec_LTLIBRARIES = poppler.la

poppler_la_LDFLAGS = $(POPPLER_LIBS) -lpoppler-glib -module -avoid-version $(POPPLER_LDFLAGS)
poppler_la_LIBADD = $(POPPLER_LIBS)
poppler_la_CFLAGS = -I/usr/lib/gtk-2.0/include -I/usr/include/gtk-2.0 -I/usr/include/cairo -I/usr/include/pycairo -I/usr/include/pango-1.0 -I/usr/include/pygtk-2.0 -I/usr/include/atk-1.0 $(POPPLER_CFLAGS)
poppler_la_SOURCES = \
	popplermodule.c

nodist_poppler_la_SOURCES = poppler.c
CLEANFILES = poppler.c
EXTRA_DIST = poppler.override poppler.defs

.defs.c:
	 $(PYGTK_CODEGEN) \
	    --override $*.override \
		--register $(DEFS)/gdk-types.defs \
        --register $(DEFS)/pango-types.defs \
        --register $(DEFS)/gtk-types.defs \
	    --prefix py_poppler $*.defs > gen-$*.c \
	&& cp gen-$*.c $*.c \
	&& rm -f gen-$*.c
