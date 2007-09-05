#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

/* include this first, before NO_IMPORT_PYGOBJECT is defined */

#include <pygobject.h>
#include <pygtk/pygtk.h>
#include <glib/poppler.h>

#include <pycairo.h>
Pycairo_CAPI_t *Pycairo_CAPI;

void pypoppler_register_classes (PyObject *d);
void pypoppler_add_constants (PyObject *module, const gchar *strip_prefix);

extern PyMethodDef pypoppler_functions[];

DL_EXPORT(void)
initpoppler(void)
{
    PyObject *m, *d;

    Pycairo_IMPORT;

    init_pygobject ();

    m = Py_InitModule ("poppler", pypoppler_functions);
    d = PyModule_GetDict (m);

    pypoppler_register_classes (d);
    
    pypoppler_add_constants(m, "POPPLER_");

    PyModule_AddObject(m, "pypoppler_version",
                       Py_BuildValue("iii",
                                     PYPOPPLER_MAJOR_VERSION,
                                     PYPOPPLER_MINOR_VERSION,
                                     PYPOPPLER_MICRO_VERSION));
    
    if (PyErr_Occurred ()) {
        Py_FatalError ("can't initialise module globalkeys");
    }
}
