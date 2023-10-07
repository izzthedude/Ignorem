from __future__ import annotations

from typing import Any, Optional

from gi.repository import GObject, Gtk

from ignorem.gitignoreio.models import TemplateModel


class TemplatePillBox(Gtk.FlowBox):
    __gtype_name__: str = "TemplatePillBox"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._pills: list[TemplatePill] = []
        self.set_selection_mode(Gtk.SelectionMode.NONE)

    def pills(self) -> list[TemplatePill]:
        return self._pills

    def append(self, pill: TemplatePill) -> None:
        super().append(pill)
        pill.parent_box = self
        self._pills.append(pill)

    def remove(self, pill: TemplatePill) -> None:
        super().remove(pill)
        pill.parent_box = None
        self._pills.remove(pill)

    def clear(self) -> None:
        while len(self._pills) > 0:
            self.remove(self._pills[0])


class TemplatePill(Gtk.Box):
    __gtype_name__: str = "TemplatePill"

    def __init__(
        self,
        template: TemplateModel,
        parent_box: Optional[TemplatePillBox] = None,
        action_button: Optional[Gtk.Button] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.template = template
        self.parent_box = parent_box
        self.action_button = action_button

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
            self.action_button.add_css_class("circular")

            button_box = Gtk.Box(hexpand=True, halign=Gtk.Align.END)
            button_box.append(self.action_button)
            self._overlay.add_overlay(button_box)

            label = self._transform_label(self.template.name, True)
            self._label_button.set_label(label)

    def set_label(self, text: str) -> None:
        label = self._transform_label(text)
        self._label_button.set_label(label)

    def _transform_label(self, text: str, has_action_button: bool = False) -> str:
        start_space = 5
        end_space = 14 if has_action_button else start_space
        final_text = " " * start_space + text + " " * end_space
        return final_text


class AddablePill(TemplatePill):
    __gtype_name__: str = "AddablePill"

    def __init__(self, template: TemplateModel) -> None:
        super().__init__(
            template, action_button=Gtk.Button(icon_name="list-add-symbolic")
        )
        self.action_button: Gtk.Button


class DeletablePill(TemplatePill):
    __gtype_name__: str = "DeletablePill"

    def __init__(self, template: TemplateModel) -> None:
        super().__init__(
            template, action_button=Gtk.Button(icon_name="edit-delete-symbolic")
        )
        self.action_button: Gtk.Button


GObject.type_register(TemplatePillBox)
GObject.type_register(TemplatePill)
GObject.type_register(AddablePill)
GObject.type_register(DeletablePill)
