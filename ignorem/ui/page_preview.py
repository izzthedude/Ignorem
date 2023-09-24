from pathlib import Path

from gi.repository import Adw, GObject, Gdk, Gtk

from ignorem.controller import AppController
from ignorem.ui.widgets import TemplatePill, TemplatePillBox
from ignorem.utils import ui


@Gtk.Template(resource_path="/com/github/izzthedude/Ignorem/ui/page-preview")
class PreviewPage(Adw.NavigationPage):
    __gtype_name__ = "PreviewPage"

    preview_stack: Adw.ViewStack = Gtk.Template.Child()
    preview_page: Adw.ViewStackPage = Gtk.Template.Child()
    preview_selected_box: TemplatePillBox = Gtk.Template.Child()
    preview_textview: Gtk.TextView = Gtk.Template.Child()

    loading_page: Adw.ViewStackPage = Gtk.Template.Child()
    preview_status_page: Adw.ViewStackPage = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._is_loading: bool = False
        self._controller = AppController.instance()
        self._init()

    @Gtk.Template.Callback()
    def on_preview_showing(self, _):
        if self._controller.selected_templates():
            ui.run_async(self, self.fetch_template, self.on_fetch_template_finished)
            ui.run_async(self, self.populate_selected_pills)
            self.is_loading = True

        else:
            self.preview_status_page.set_title("No templates were selected.")
            self.preview_stack.set_visible_child_name(
                self.preview_status_page.get_name()
            )

    def fetch_template(self):
        result = self._controller.request_template()
        buffer = Gtk.TextBuffer(text=result)
        self.preview_textview.set_buffer(buffer)

    def on_fetch_template_finished(self):
        self.is_loading = False

    def populate_selected_pills(self):
        templates = self._controller.selected_templates()
        for template in templates:
            self.preview_selected_box.append(TemplatePill(template))

    @Gtk.Template.Callback()
    def on_copy_template(self, button: Gtk.Button):
        text = self.preview_textview.get_buffer().props.text
        clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())
        clipboard.set(text)

    @Gtk.Template.Callback()
    def on_save_template(self, button: Gtk.Button):
        dialog = Gtk.FileChooserNative(
            action=Gtk.FileChooserAction.SAVE,
            title="Save template",
            accept_label="Save",
            cancel_label="Cancel",
        )
        dialog.set_current_name(".gitignore")
        dialog.connect("response", self.on_save_response)
        dialog.show()

    def on_save_response(self, dialog: Gtk.FileChooserNative, response: int):
        if response == Gtk.ResponseType.ACCEPT:
            file = dialog.get_file()
            ui.run_async(self, self.save_template, func_args=(file.get_path(),))

    def save_template(self, path: str):
        path = Path(path)
        text = self.preview_textview.get_buffer().props.text
        path.write_text(text)

    @Gtk.Template.Callback()
    def on_preview_hiding(self, _):
        ui.run_async(self, self.reset_page)

    def reset_page(self):
        self._controller.reset()
        self.preview_textview.get_buffer().props.text = ""
        self.preview_selected_box.clear()

    @GObject.Property(type=bool, default=False, nick="is-loading")
    def is_loading(self) -> bool:
        return self._is_loading

    @is_loading.setter
    def is_loading(self, value: bool):
        self._is_loading = value

    def _init(self):
        self.bind_property(
            "is-loading",
            self.preview_stack,
            "visible-child-name",
            GObject.BindingFlags.DEFAULT | GObject.BindingFlags.SYNC_CREATE,
            lambda *_: self.loading_page.get_name()
            if self.is_loading
            else self.preview_page.get_name(),
        )
