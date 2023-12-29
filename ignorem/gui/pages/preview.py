from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from gi.repository import Adw, Gtk

from ignorem.controller import AppController
from ignorem.gui.utils import functions as gui
from ignorem.gui.widgets import TemplatePill, TemplatePillBox

if TYPE_CHECKING:
    from ignorem.gitignoreio.models import TemplateModel

logger = logging.getLogger(__name__)


@Gtk.Template(resource_path="/com/github/izzthedude/Ignorem/ui/page-preview")
class PreviewPage(Adw.NavigationPage):
    __gtype_name__: str = "PreviewPage"

    preview_stack: Adw.ViewStack = Gtk.Template.Child()
    preview_page: Adw.ViewStackPage = Gtk.Template.Child()
    selected_pillbox: TemplatePillBox = Gtk.Template.Child()
    template_textview: Gtk.TextView = Gtk.Template.Child()

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._controller = AppController.instance()

    @Gtk.Template.Callback()
    def on_preview_showing(self, _: Any) -> None:
        logger.info("Populating Preview Page")
        self.populate_selected_pills(self._controller.selected())
        self.populate_textview(self._controller.template_text)

    def populate_selected_pills(self, selected: list[TemplateModel]) -> None:
        logger.debug(
            f"Populating selected templates with keys: "
            f"{[template.key for template in selected]}"
        )
        for template in selected:
            self.selected_pillbox.add_pill(TemplatePill(template))

    def populate_textview(self, template: str) -> None:
        _lines = len(template.split("\n"))
        logger.debug(
            f"Populating text preview: {_lines} lines, {len(template)} characters"
        )
        buffer = self.template_textview.get_buffer()
        buffer.props.text = template

    @Gtk.Template.Callback()
    def on_preview_hidden(self, _: Any) -> None:
        logger.debug("Resetting Preview Page")
        self.selected_pillbox.clear()
        self.template_textview.get_buffer().props.text = ""


gui.register_type(PreviewPage)
