import gtk
import poppler
import sys
import cairo

class Poprender(object):
    def __init__(self):
        uri = "file://" + sys.argv[1]
        
        self.document = poppler.document_new_from_file (uri, None)
        self.n_pages = self.document.get_n_pages()
        self.current_page = self.document.get_page(1)
        self.scale = 1
        self.width, self.height = self.current_page.get_size()
        self.surface = cairo.ImageSurface(cairo.FORMAT_RGB24,
                                          int(self.width),
                                          int(self.height))
        
        win = gtk.Window(gtk.WINDOW_TOPLEVEL)
        win.set_default_size(600, 600)
        win.set_title ("Poppler GLib Demo")
        win.connect("delete-event", gtk.main_quit)
        
        adjust = gtk.Adjustment(1, 1, self.n_pages, 1)
        page_selector = gtk.SpinButton(adjust, 0, 0);
        page_selector.connect("value-changed", self.on_changed)

        lab = gtk.Label('Page Number:')

        hbox = gtk.HBox(False, 0)

        vbox = gtk.VBox(False, 0)
        vbox.pack_start(hbox, False, False, 0)
        
        hbox.pack_start(lab, False, False, 4)
        hbox.pack_start(page_selector, False, False, 0)
        
        adjust = gtk.Adjustment(1, 1, 5, 1)
        scale_selector = gtk.SpinButton(adjust, 0, 0);
        scale_selector.connect("value-changed", self.on_scale_changed)
        
        lab = gtk.Label('Scale:')

        hbox.pack_start(lab, False, False, 4)
        hbox.pack_start(scale_selector, False, False, 0)

        b_scan_fonts = gtk.Button('Scan Fonts')
        b_scan_fonts.connect("clicked", self.on_scan_fonts)
        
        hbox.pack_start(b_scan_fonts, False, False, 4)

        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        
        self.dwg = gtk.DrawingArea()
        self.dwg.set_size_request(int(self.width), int(self.height))
        self.dwg.connect("expose-event", self.on_expose)
        
        sw.add_with_viewport(self.dwg)
        
        vbox.pack_start(sw, True, True, 0)
        
        win.add(vbox)
        
        win.show_all()
    
    def on_changed(self, widget):
        self.current_page = self.document.get_page(widget.get_value_as_int())
        self.dwg.set_size_request(int(self.width)*self.scale,
                                  int(self.height)*self.scale)
        self.dwg.queue_draw()
    
    def on_scale_changed(self, widget):
        self.scale = widget.get_value_as_int()
        self.dwg.set_size_request(int(self.width)*self.scale,
                                  int(self.height)*self.scale)
        self.dwg.queue_draw()
    
    def on_expose(self, widget, event):
        cr = widget.window.cairo_create()
        cr.set_source_surface(self.surface)
        cr.set_source_rgb(1, 1, 1)
        
        if self.scale != 1:
            cr.scale(self.scale, self.scale)
        
        cr.rectangle(0, 0, self.width, self.height)
        cr.fill()
        self.current_page.render(cr)
    
    def on_scan_fonts(self, widget):
        font_info = poppler.FontInfo(self.document)
        iter = font_info.scan(self.n_pages)
        
        print iter.get_full_name()
        
        while iter.next():
            print iter.get_full_name()

    def main(self):
        gtk.main()

if __name__ == '__main__':
    pop = Poprender()
    pop.main()
