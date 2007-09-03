from argtypes import ArgType, matcher
import reversewrapper

class RectanglePtrArg(ArgType):

    def write_param(self, ptype, pname, pdflt, pnull, info):
        if pdflt:
            info.varlist.add('PyObject', '*py_' + pname + " = " + pdflt)
        else:
            info.varlist.add('PyObject', '*py_' + pname)
        if pnull:
            info.add_parselist('O', ['&py_'+pname], [pname])
            info.codebefore.append(
                '    if (!(py_%(name)s == NULL || py_%(name)s == Py_None || \n'
                '        PyObject_IsInstance(py_%(name)s, (PyObject *) &PyPopplerRectangle_Type))) {\n'
                '        PyErr_SetString(PyExc_TypeError, "parameter %(name)s must be poppler.Rectangle or None");\n'
                '        return NULL;\n'
                '    }\n' % dict(name=pname))
            info.arglist.append("(py_%s == NULL || py_%s == Py_None)? NULL :"
                                " ((PyPopplerRectangle *) py_%s)->rect" % (pname, pname, pname))
        else:
            info.add_parselist('O!', ['&PyPopplerRectangle_Type', '&py_'+pname], [pname])
            info.arglist.append("(py_%s == NULL)? NULL :"
                                " ((PyPopplerRectangle *) py_%s)->rect" % (pname, pname))

    def write_return(self, ptype, ownsreturn, info):
        info.varlist.add('PopplerRectangle', '*ret')
        info.codeafter.append('   return pypoppler_rectangle_new(ret);\n');

matcher.register('PopplerRectangle*', RectanglePtrArg())
matcher.register('const-PopplerRectangle*', RectanglePtrArg())

class PopplerRectanglePtrReturn(reversewrapper.ReturnType):
    def get_c_type(self):
        return self.props.get('c_type')
    def write_decl(self):
        self.wrapper.add_declaration("%s retval;" % self.get_c_type())
        self.wrapper.add_declaration("PyObject *py_rect;")
    def write_error_return(self):
        self.wrapper.write_code("return NULL;")
    def write_conversion(self):
        self.wrapper.add_pyret_parse_item("O!", "&PyPopplerRectangle_Type, &py_rect", prepend=True)
        self.wrapper.write_code((
            " /* FIXME: this leaks memory */\n"
            "retval = g_new(PopplerRectangle, 1);\n"
            "*retval = ((PyPopplerRectangle*) py_rect)->rect;"),
                                code_sink=self.wrapper.post_return_code)

matcher.register_reverse_ret("PopplerRectangle*", PopplerRectanglePtrReturn)

class PopplerRectanglePtrParam(reversewrapper.Parameter):
    def get_c_type(self):
        return self.props.get('c_type').replace('const-', 'const ')
    def convert_c2py(self):
        self.wrapper.add_declaration("PyObject *py_%s;" % self.name)
        self.wrapper.write_code(
            code=('py_%s = pypoppler_rectangle_new(%s);' %
                  (self.name, self.name)),
            cleanup=("Py_DECREF(py_%s);" % self.name))
        self.wrapper.add_pyargv_item("py_%s" % self.name)

matcher.register_reverse("PopplerRectangle*", PopplerRectanglePtrParam)
matcher.register_reverse("const-PopplerRectangle*", PopplerRectanglePtrParam)
