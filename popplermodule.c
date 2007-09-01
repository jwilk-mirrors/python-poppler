#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

/* include this first, before NO_IMPORT_PYGOBJECT is defined */

#include <pygobject.h>
#include <pygtk/pygtk.h>
#include <glib/poppler.h>

#include <pycairo.h>
Pycairo_CAPI_t *Pycairo_CAPI;

void py_poppler_register_classes (PyObject *d);

extern PyMethodDef py_poppler_functions[];

DL_EXPORT(void)
initpoppler(void)
{
    PyObject *m, *d;

    Pycairo_IMPORT;

    init_pygobject ();

    m = Py_InitModule ("poppler", py_poppler_functions);
    d = PyModule_GetDict (m);

    py_poppler_register_classes (d);

    if (PyErr_Occurred ()) {
        Py_FatalError ("can't initialise module globalkeys");
    }
}
