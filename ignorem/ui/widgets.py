from gi.repository import Adw, Gtk


class TemplateRow(Adw.ActionRow):
    __gtype_name__ = "TemplateRow"

    def __init__(self, name: str):
        super().__init__()
        self.delete_button = Gtk.Button(icon_name="user-trash-symbolic")
        self.button_box = Gtk.Box(valign=Gtk.Align.CENTER, halign=Gtk.Align.CENTER)
        self.button_box.append(self.delete_button)

        self.set_title(name)
        self.add_suffix(self.button_box)
