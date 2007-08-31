
AUTOMAKE_OPTIONS = 1.7


DEFS=/usr/share/pygtk/2.0/defs

INCLUDES =                                      \
        $(PYTHON_INCLUDES)                      \
        $(POPPLER_CFLAGS)

GTK_CFLAGS=`pkg-config --cflags gtk+-2.0`
PYGTK_CFLAGS=`pkg-config --cflags pygtk-2.0`
CAIRO_CFLAGS=`pkg-config --cflags cairo`
PYCAIRO_CFLAGS=`pkg-config --cflags pycairo`

pkgpyexecdir = $(pythondir)

pkgpyexec_LTLIBRARIES = poppler.la

poppler_la_LDFLAGS = $(POPPLER_LIBS) -lpoppler-glib -module -avoid-version $(POPPLER_LDFLAGS)
poppler_la_LIBADD = $(POPPLER_LIBS)
poppler_la_CFLAGS = $(GTK_CFLAGS) $(PYGTK_CFLAGS) $(CAIRO_CFLAGS) $(PYCAIRO_CFLAGS) $(POPPLER_CFLAGS)
poppler_la_SOURCES = \
	popplermodule.c

nodist_poppler_la_SOURCES = poppler.c
CLEANFILES = poppler.c
EXTRA_DIST = poppler.override poppler.defs


banana:
	echo $(GTK_CFLAGS)

.defs.c:
	 $(PYGTK_CODEGEN) \
	    --override $*.override \
		--register $(DEFS)/gdk-types.defs \
        --register $(DEFS)/pango-types.defs \
        --register $(DEFS)/gtk-types.defs \
	    --prefix py_poppler $*.defs > gen-$*.c \
	&& cp gen-$*.c $*.c \
	&& rm -f gen-$*.c
