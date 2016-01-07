#!/usr/bin/env python
'''Single Channel Window

The GUI Framework for the Single-Channel Computer Application for Acoustic Ruler

Based on the demos of PyGTK'''

import pygtk
pygtk.require('2.0')
import gtk

class DialogAndMessageBox(gtk.Window):
        counter = 1
        def __init__(self, parent=None):
                # Create the toplevel window
                gtk.Window.__init__(self)
                try:
                        self.set_screen(parent.get_screen())
                except AttributeError:
                        self.connect('destroy', lambda *w: gtk.main_quit())

                self.set_title(self.__class__.__name__)
                self.set_border_width(8)

                frame = gtk.Frame("Single Channel")
                self.add(frame)

                vbox = gtk.VBox(False, 8)
                vbox.set_border_width(8)
                frame.add(vbox)

                #Message Dialog
                hbox = gtk.HBox(False, 8)
                vbox.pack_start(hbox)
                button = gtk.Button("_Measure!")
                button.connect('clicked', self.on_message_dialog_clicked)
                hbox.pack_start(button, False, False, 0)
                vbox.pack_start(gtk.HSeparator(), False, False, 0)

                table = gtk.Table(2,2)
                table.set_row_spacings(4)
                table.set_col_spacings(4)
                hbox.pack_start(table, False, False, 0)

                label = gtk.Label("path:")
                label.set_use_underline(True)
                table.attach(label, 0, 1, 0, 1)

                self.path = gtk.Entry()
                table.attach(self.path, 1, 2, 0, 1)
                label.set_mnemonic_widget(self.path)
                
                self.show_all()

        def on_message_dialog_clicked(self, button):
                dialog = gtk.MessageDialog(self,
                                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                gtk.MESSAGE_INFO, gtk.BUTTONS_OK,
                                "You have made %d measurement%s." %
                                        (self.counter, self.counter >1 and 's' or ''))
                dialog.run()
                dialog.destroy()
                self.counter += 1

def main():
        DialogAndMessageBox()
        gtk.main()

if __name__ == '__main__':
        main()

