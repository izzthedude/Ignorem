from gi.repository import Gtk

from ignorem.gitignore import TemplateData


class TemplatePillBox(Gtk.FlowBox):
    __gtype_name__ = "TemplatePillBox"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._pills: list[TemplatePill] = []
        self.set_selection_mode(Gtk.SelectionMode.NONE)

    @property
    def pills(self) -> list["TemplatePill"]:
        return self._pills

    def append(self, pill: "TemplatePill"):
        super().append(pill)
        pill.parent_box = self
        self.pills.append(pill)

    def remove(self, pill: "TemplatePill"):
        super().remove(pill)
        pill.parent_box = None
        self.pills.remove(pill)
        return pill.template

    def clear(self):
        for pill in self.pills:
            self.remove(pill)


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
