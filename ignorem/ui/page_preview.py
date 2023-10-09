from pathlib import Path
from typing import Any

from gi.repository import Adw, GObject, Gdk, Gtk

from ignorem.controller import AppController
from ignorem.ui.widgets import TemplatePill, TemplatePillBox
from ignorem.utils import ui, worker


@Gtk.Template(resource_path="/com/github/izzthedude/Ignorem/ui/page-preview")
class PreviewPage(Adw.NavigationPage):  # type: ignore
    __gtype_name__: str = "PreviewPage"

    preview_stack: Adw.ViewStack = Gtk.Template.Child()
    preview_page: Adw.ViewStackPage = Gtk.Template.Child()
    preview_selected_box: TemplatePillBox = Gtk.Template.Child()
    preview_textview: Gtk.TextView = Gtk.Template.Child()

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

    @Gtk.Template.Callback()
    def on_preview_showing(self, _: Any) -> None:
        if self._controller.selected_templates():
            self.fetch_template()
            self.populate_selected_pills()
            self.is_loading = True

        else:
            self.preview_status_page.set_title("No templates were selected.")
            self.preview_stack.set_visible_child_name(
                self.preview_status_page.get_name()  # type: ignore
            )

    @worker.run("on_fetch_template_finished")
    def fetch_template(self) -> None:
        result = self._controller.request_template()
        buffer = Gtk.TextBuffer(text=result)
        self.preview_textview.set_buffer(buffer)

    def on_fetch_template_finished(self, result: None) -> None:
        self.is_loading = False

    @worker.run()
    def populate_selected_pills(self) -> None:
        templates = self._controller.selected_templates()
        for template in templates:
            self.preview_selected_box.add_pill(TemplatePill(template))

    @Gtk.Template.Callback()
    def on_copy_template(self, button: Gtk.Button) -> None:
        text = self.preview_textview.get_buffer().props.text
        clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())  # type: ignore
        clipboard.set(text)

    @Gtk.Template.Callback()
    def on_save_template(self, button: Gtk.Button) -> None:
        dialog = Gtk.FileChooserNative(
            action=Gtk.FileChooserAction.SAVE,
            title="Save template",
            accept_label="Save",
            cancel_label="Cancel",
        )
        dialog.set_current_name(".gitignore")
        dialog.connect("response", self.on_save_response)
        dialog.show()

    def on_save_response(self, dialog: Gtk.FileChooserNative, response: int) -> None:
        if response == Gtk.ResponseType.ACCEPT:
            file = dialog.get_file()
            self.save_template(file.get_path())  # type: ignore

    @worker.run()
    def save_template(self, path: str) -> None:
        text = self.preview_textview.get_buffer().props.text
        file_path = Path(path)
        file_path.write_text(text)

    @Gtk.Template.Callback()
    def on_preview_hiding(self, _: Any) -> None:
        self.reset_page()

    @worker.run()
    def reset_page(self) -> None:
        self._controller.reset()
        self.preview_selected_box.clear()
        self.preview_textview.get_buffer().props.text = ""

    @GObject.Property(type=bool, default=False, nick="is-loading")
    def is_loading(self) -> bool:
        return self._is_loading

    @is_loading.setter  # type: ignore
    def is_loading(self, value: bool) -> None:
        self._is_loading = value


ui.register_type(PreviewPage)
