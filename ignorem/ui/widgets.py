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


class TemplatePill(Gtk.Box):
    __gtype_name__ = "TemplatePill"

    def __init__(self, text: str, deletable: bool = False, **kwargs):
        super().__init__(**kwargs)
        self._text_start_offset: int = 5
        self._text_end_offset: int = 14 if deletable else 5
        final_text = (
            (" " * self._text_start_offset) + text + (" " * self._text_end_offset)
        )

        overlay = Gtk.Overlay()
        self.append(overlay)

        label_button = Gtk.Button(label=final_text)
        label_button.add_css_class("suggested-action")
        label_button.add_css_class("circular")
        label_box = Gtk.Box(vexpand=False)
        label_box.append(label_button)
        overlay.set_child(label_box)

        self.delete_button = Gtk.Button(icon_name="edit-delete-symbolic")
        self.delete_button.add_css_class("circular")
        delete_box = Gtk.Box(vexpand=False, hexpand=True, halign=Gtk.Align.END)
        delete_box.append(self.delete_button)
        if deletable:
            overlay.add_overlay(delete_box)
