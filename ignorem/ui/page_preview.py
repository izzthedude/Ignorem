from typing import Any

from gi.repository import Adw, GObject, Gtk

from ignorem.controller import AppController
from ignorem.gitignoreio.models import TemplateModel
from ignorem.ui.widgets import TemplatePill, TemplatePillBox
from ignorem.utils import ui


@Gtk.Template(resource_path="/com/github/izzthedude/Ignorem/ui/page-preview")
class PreviewPage(Adw.NavigationPage):  # type: ignore
    __gtype_name__: str = "PreviewPage"

    ERROR_OCCURRED = "error-occurred"

    preview_stack: Adw.ViewStack = Gtk.Template.Child()
    preview_page: Adw.ViewStackPage = Gtk.Template.Child()
    selected_pillbox: TemplatePillBox = Gtk.Template.Child()
    template_textview: Gtk.TextView = Gtk.Template.Child()

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._controller = AppController.instance()

    @Gtk.Template.Callback()
    def on_preview_showing(self, _: Any) -> None:
        self.populate_selected_pills(self._controller.selected())
        self.populate_textview(self._controller.template_text)

    def populate_selected_pills(self, selected: list[TemplateModel]) -> None:
        for template in selected:
            self.selected_pillbox.add_pill(TemplatePill(template))

    def populate_textview(self, template: str) -> None:
        buffer = self.template_textview.get_buffer()
        buffer.props.text = template

    @Gtk.Template.Callback()
    def on_preview_hidden(self, _: Any) -> None:
        self.reset_page()

    def reset_page(self) -> None:
        self.selected_pillbox.clear()
        self.template_textview.get_buffer().props.text = ""


ui.register_type(PreviewPage)
ui.register_signal(
    PreviewPage.ERROR_OCCURRED,
    PreviewPage,
    GObject.SignalFlags.RUN_FIRST,
    GObject.TYPE_NONE,
    (
        str,  # icon_name
        str,  # title
        str,  # description
    ),
)
