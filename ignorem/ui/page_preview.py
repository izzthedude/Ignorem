from typing import Any

from gi.repository import Adw, GObject, Gtk

from ignorem.controller import AppController
from ignorem.gitignoreio.models import TemplateModel
from ignorem.ui.widgets import TemplatePill, TemplatePillBox
from ignorem.utils import ui, worker


@Gtk.Template(resource_path="/com/github/izzthedude/Ignorem/ui/page-preview")
class PreviewPage(Adw.NavigationPage):  # type: ignore
    __gtype_name__: str = "PreviewPage"

    preview_stack: Adw.ViewStack = Gtk.Template.Child()
    preview_page: Adw.ViewStackPage = Gtk.Template.Child()
    selected_pillbox: TemplatePillBox = Gtk.Template.Child()
    template_textview: Gtk.TextView = Gtk.Template.Child()

    loading_page: Adw.ViewStackPage = Gtk.Template.Child()
    preview_status_page: Adw.ViewStackPage = Gtk.Template.Child()

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._is_loading: bool = False
        self._controller = AppController.instance()

        self.bind_property(
            "is-loading",
            self.preview_stack,
            "visible-child-name",
            GObject.BindingFlags.DEFAULT | GObject.BindingFlags.SYNC_CREATE,
            lambda *_: self.loading_page.get_name()
            if self.is_loading
            else self.preview_page.get_name(),
        )

    @GObject.Property(type=bool, default=False, nick="is-loading")
    def is_loading(self) -> bool:
        return self._is_loading

    @is_loading.setter  # type: ignore
    def is_loading(self, value: bool) -> None:
        self._is_loading = value

    @Gtk.Template.Callback()
    def on_preview_showing(self, _: Any) -> None:
        self.request_template()

    def request_template(self) -> None:
        worker.run(
            self,
            self._controller.request_template,
            callback=self.on_request_template_finished,
            error_callback=self.on_request_template_error,
        )
        self.is_loading = True

    def on_request_template_finished(self, result: None) -> None:
        self.is_loading = False
        self.populate_selected_pills(self._controller.selected())
        self.populate_textview(self._controller.template_text)

    def on_request_template_error(self, error: BaseException) -> None:
        self.is_loading = False
        print(error)

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
