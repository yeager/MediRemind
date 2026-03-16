"""Widget for displaying medication pictograms."""

import os as _os

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GdkPixbuf, Gdk


class PictogramImage(Gtk.Box):
    def __init__(self, size=96):
        super().__init__()
        self._size = size
        self._picture = Gtk.Picture()
        self._picture.set_size_request(size, size)
        self._picture.set_content_fit(Gtk.ContentFit.CONTAIN)
        self.append(self._picture)

    def set_from_file(self, filepath):
        if filepath and _os.path.exists(filepath):
            try:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    filepath, self._size, self._size, True
                )
                texture = Gdk.Texture.new_for_pixbuf(pixbuf)
                self._picture.set_paintable(texture)
            except Exception:
                self._set_fallback_label()
        else:
            self._set_fallback_label()

    def _set_fallback_label(self):
        if self._picture.get_parent():
            self.remove(self._picture)
        label = Gtk.Label(label="\U0001f48a")
        label.add_css_class("pictogram-fallback")
        label.set_size_request(self._size, self._size)
        self.append(label)
