from gi.repository import Adw, Gtk


@Gtk.Template(resource_path="/com/github/izzthedude/Ignorem/ui/page-preview")
class PreviewPage(Adw.NavigationPage):
    __gtype_name__ = "PreviewPage"

    @Gtk.Template.Callback()
    def on_copy_template(self, button: Gtk.Button):
        print("copy")

    @Gtk.Template.Callback()
    def on_save_template(self, button: Gtk.Button):
        print("save")
