from gi.repository import Adw, Gtk

from ignorem.gitignore import TemplateData


class TemplatesList(Adw.PreferencesGroup):
    __gtype_name__ = "TemplatesList"

    def add(self, child: "TemplateRow"):
        """Leaving implementation for later"""
        super().add(child)

    def remove(self, child: "TemplateRow"):
        """Leaving implementation for later"""
        super().remove(child)

    def clear(self):
        """Leaving implementation for later"""


class TemplateRow(Adw.ActionRow):
    __gtype_name__ = "TemplateRow"

    def __init__(self, template: TemplateData, source_group: TemplatesList):
        super().__init__()
        self.template = template
        self.source_group = source_group

        self.delete_button = Gtk.Button(icon_name="user-trash-symbolic")
        self.button_box = Gtk.Box(valign=Gtk.Align.CENTER, halign=Gtk.Align.CENTER)
        self.button_box.append(self.delete_button)

        self.set_title(template.name)
        self.add_suffix(self.button_box)

        self.delete_button.connect("clicked", lambda _: self.source_group.remove(self))
