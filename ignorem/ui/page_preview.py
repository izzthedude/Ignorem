from gi.repository import Adw, GObject, Gtk


@Gtk.Template(resource_path="/com/github/izzthedude/Ignorem/ui/page-preview")
class PreviewPage(Adw.NavigationPage):
    __gtype_name__ = "PreviewPage"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._is_loading: bool = False

    @Gtk.Template.Callback()
    def on_copy_template(self, button: Gtk.Button):
        print("copy")

    @Gtk.Template.Callback()
    def on_save_template(self, button: Gtk.Button):
        print("save")

    @GObject.Property(type=bool, default=False, nick="is-loading")
    def is_loading(self) -> bool:
        return self._is_loading

    @is_loading.setter
    def is_loading(self, value: bool):
        self._is_loading = value
