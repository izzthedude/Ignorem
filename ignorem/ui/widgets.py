from gi.repository import Gtk

from ignorem.gitignore import TemplateData


class TemplatePillBox(Gtk.FlowBox):
    __gtype_name__ = "TemplatePillBox"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_selection_mode(Gtk.SelectionMode.NONE)

    def append(self, pill: "TemplatePill") -> TemplateData:
        pill.delete_button.connect("clicked", lambda _: self.remove(pill))
        super().append(pill)
        return pill.template

    def remove(self, child: "TemplatePill") -> TemplateData:
        super().remove(child)
        return child.template


class TemplatePill(Gtk.Box):
    __gtype_name__ = "TemplatePill"

    def __init__(self, template: TemplateData, deletable: bool = True, **kwargs):
        super().__init__(**kwargs)
        self.template = template

        self._text_start_offset: int = 5
        self._text_end_offset: int = 14 if deletable else 5
        final_text = (
            (" " * self._text_start_offset)
            + self.template.name
            + (" " * self._text_end_offset)
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
