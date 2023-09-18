from gi.repository import Adw, GObject, Gtk

from ignorem import utils
from ignorem.controller import AppController


@Gtk.Template(resource_path="/com/github/izzthedude/Ignorem/ui/page-search")
class SearchPage(Adw.NavigationPage):
    __gtype_name__ = "SearchPage"

    refresh_button: Gtk.Button = Gtk.Template.Child()
    # TODO: Figure out how to give search suggestions

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._controller = AppController.instance()
        self._refreshing: bool = False

        # Fetch list on page init
        utils.ui.run_async(self, self._controller.fetch_list, self.on_refresh_finished)
        self.refreshing = True

    @Gtk.Template.Callback()
    def on_refresh(self, button: Gtk.Button):
        if not self._refreshing:
            utils.ui.run_async(
                self,
                self._controller.fetch_list,
                self.on_refresh_finished,
                func_args=(True,),
            )
            self.refreshing = True

    def on_refresh_finished(self):
        self.refreshing = False

    @GObject.Property(type=bool, default=False, nick="refreshing")
    def refreshing(self) -> bool:
        return self._refreshing

    @refreshing.setter
    def refreshing(self, value: bool):
        self._refreshing = value

    @Gtk.Template.Callback()
    def on_search_changed(self, entry: Gtk.SearchEntry):
        text = entry.get_text()
        print(text)

    @Gtk.Template.Callback()
    def on_create_clicked(self, button: Gtk.Button):
        print("clear")

    @Gtk.Template.Callback()
    def on_debug_clicked(self, button: Gtk.Button):
        print("debug")
