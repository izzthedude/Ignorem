from gi.repository import GObject, Gtk

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

    def __init__(self, template: TemplateData, deletable: bool = False, **kwargs):
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


class SearchSuggestionsBox(Gtk.ScrolledWindow):
    __gtype_name__ = "SearchSuggestionsBox"

    def __init__(self, **kwargs):
        super().__init__()
        self.set_propagate_natural_height(True)
        self.set_propagate_natural_height(True)
        self.set_valign(Gtk.Align.START)
        self.set_halign(Gtk.Align.CENTER)
        self.set_visible(False)
        self.add_css_class("card")
        self.add_css_class("view")

        content_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            valign=Gtk.Align.START,
            halign=Gtk.Align.START,
        )
        self.set_child(content_box)

        box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            margin_top=10,
            margin_bottom=10,
            margin_start=10,
            margin_end=10,
            spacing=20,
            valign=Gtk.Align.START,
            halign=Gtk.Align.START,
        )
        content_box.append(box)

        self.templatepill_box: TemplatePillBox = TemplatePillBox()
        box.append(self.templatepill_box)

        self.no_results_label = Gtk.Label(
            label="No templates found",
            visible=False,
            margin_top=10,
            margin_start=10,
        )
        self.no_results_label.bind_property(
            "visible",
            box,
            "visible",
            GObject.BindingFlags.DEFAULT
            | GObject.BindingFlags.SYNC_CREATE
            | GObject.BindingFlags.BIDIRECTIONAL
            | GObject.BindingFlags.INVERT_BOOLEAN,
        )
        content_box.append(self.no_results_label)

    def set_results_found(self, found: bool):
        self.no_results_label.set_visible(not found)
