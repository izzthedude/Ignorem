from gi.repository import Adw, Gtk


@Gtk.Template(resource_path="/com/github/izzthedude/Ignorem/ui/page-preview")
class PreviewPage(Adw.NavigationPage):
    __gtype_name__ = "PreviewPage"
