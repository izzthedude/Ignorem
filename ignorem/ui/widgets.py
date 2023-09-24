from gi.repository import GObject, Gtk

from ignorem.gitignore import TemplateData


class TemplatePillBox(Gtk.FlowBox):
    __gtype_name__ = "TemplatePillBox"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pills: list[TemplatePill] = []
        self.set_selection_mode(Gtk.SelectionMode.NONE)

    def append(self, pill: "TemplatePill"):
        pill.parent_box = self
        self.pills.append(pill)
        super().append(pill)

    def remove(self, pill: "TemplatePill"):
        pill.parent_box = None
        self.pills.remove(pill)
        super().remove(pill)
        return pill.template


class TemplatePill(Gtk.Box):
    __gtype_name__ = "TemplatePill"

    def __init__(
        self,
        template: TemplateData,
        action_button: Gtk.Button | None = None,
        parent_box: TemplatePillBox | None = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.template = template
        self.action_button = action_button
        self.parent_box = parent_box

        self._overlay = Gtk.Overlay()
        self.append(self._overlay)

        label = self._transform_label(self.template.name)
        self._label_button = Gtk.Button(label=label)
        self._label_button.add_css_class("suggested-action")
        self._label_button.add_css_class("circular")
        label_box = Gtk.Box(vexpand=False)
        label_box.append(self._label_button)
        self._overlay.set_child(label_box)

        if self.action_button:
            self._init_action_button()

    def set_label(self, text: str):
        label = self._transform_label(text)
        self._label_button.set_label(label)

    def _init_action_button(self):
        self.action_button.add_css_class("circular")

        button_box = Gtk.Box(hexpand=True, halign=Gtk.Align.END)
        button_box.append(self.action_button)
        self._overlay.add_overlay(button_box)

        label = self._transform_label(self.template.name, True)
        self._label_button.set_label(label)

    def _transform_label(self, text: str, has_action_button: bool = False) -> str:
        start_space = 5
        end_space = 14 if has_action_button else start_space
        final_text = " " * start_space + text + " " * end_space
        return final_text


class AddablePill(TemplatePill):
    __gtype_name__ = "AddablePill"

    def __init__(self, template: TemplateData):
        super().__init__(template, Gtk.Button(icon_name="list-add-symbolic"))


class DeletablePill(TemplatePill):
    __gtype_name__ = "DeletablePill"

    def __init__(self, template: TemplateData):
        super().__init__(template, Gtk.Button(icon_name="edit-delete-symbolic"))
        self.action_button.connect("clicked", lambda _: self.parent_box.remove(self))


class SearchSuggestionsBox(Gtk.ScrolledWindow):
    __gtype_name__ = "SearchSuggestionsBox"

    def __init__(self, **kwargs):
        super().__init__()
        self.set_propagate_natural_height(True)
        self.set_propagate_natural_height(True)
        self.set_valign(Gtk.Align.START)
        self.set_halign(Gtk.Align.CENTER)
        self.set_margin_top(160)
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
