  #   #               #
  #   #               #
### # # ### ### ### ###
# # # # # # # # # # # #
### # # ### ###  ## ###
            #
            #

"""\
PyGTK interface module.

@author: Aaron Mavrinac
@contact: mavrinac@gmail.com
@license: GPL-3
"""

import pygtk
pygtk.require('2.0')
import gtk

from .device import Circuit


class Pad(gtk.DrawingArea):
    """\
    Drawing area widget.
    """
    __gsignals__ = {'expose-event': 'override'}

    def __init__(self):
        super(Pad, self).__init__()
        self.circuit = Circuit()

    def do_expose_event(self, event):
        cr = self.window.cairo_create()
        cr.rectangle(event.area.x, event.area.y, event.area.width, event.area.height)
        cr.clip()
        self.draw(cr, *self.window.get_size())

    def draw(self, cr, width, height):
        # background
        cr.set_source_rgb(0, 0, 0)
        cr.rectangle(0, 0, width, height)
        cr.fill()
        # grid
        cr.set_source_rgb(0.0, 0.0, 0.1)
        for x in range(width // 10 + 1):
            cr.move_to(x * 10, 0)
            cr.rel_line_to(0, height)
            cr.stroke()
        for y in range(height // 10 + 1):
            cr.move_to(0, y * 10)
            cr.rel_line_to(width, 0)
            cr.stroke()


class Interface(gtk.Window):
    """\
    PyGTK interface window class.
    """
    def __init__(self):
        """\
        Constructor.
        """
        super(Interface, self).__init__()
        
        # basics
        self.set_title('Dilopad')
        self.set_border_width(0)
        self.connect('delete_event', self._delete_event)
        self.connect('destroy', self._destroy)

        # pad
        self.pad = Pad()
        self.add(self.pad)

        self.show_all()

    @staticmethod
    def main():
        """\
        Main event loop.
        """
        gtk.main()

    def _delete_event(self, widget, data=None):
        return False

    def _destroy(self, widget, data=None):
        gtk.main_quit()
