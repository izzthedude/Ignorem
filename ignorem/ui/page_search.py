from gi.repository import Adw, Gtk


@Gtk.Template(resource_path="/com/github/izzthedude/Ignorem/ui/page-search")
class SearchPage(Adw.NavigationPage):
    __gtype_name__ = "SearchPage"

    # TODO: Figure out how to give search suggestions

    @Gtk.Template.Callback()
    def on_search_changed(self, entry: Gtk.SearchEntry):
        text = entry.get_text()
        print(text)

    @Gtk.Template.Callback()
    def on_clear_list(self, button: Gtk.Button):
        print("clear")

    @Gtk.Template.Callback()
    def on_create_clicked(self, button: Gtk.Button):
        print("clear")

    @Gtk.Template.Callback()
    def on_debug_clicked(self, button: Gtk.Button):
        print("debug")
