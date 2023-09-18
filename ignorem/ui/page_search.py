from gi.repository import Adw, GObject, Gtk

from ignorem import utils
from ignorem.controller import AppController


@Gtk.Template(resource_path="/com/github/izzthedude/Ignorem/ui/page-search")
class SearchPage(Adw.NavigationPage):
    __gtype_name__ = "SearchPage"

    search_stack: Adw.ViewStack = Gtk.Template.Child()
    search_page: Adw.ViewStackPage = Gtk.Template.Child()
    loading_page: Adw.ViewStackPage = Gtk.Template.Child()
    # TODO: Figure out how to give search suggestions

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._controller = AppController.instance()
        self._is_loading: bool = False
        self.bind_property(
            "is-loading",
            self.search_stack,
            "visible-child-name",
            GObject.BindingFlags.DEFAULT | GObject.BindingFlags.SYNC_CREATE,
            lambda *_: self.loading_page.get_name()
            if self.is_loading
            else self.search_page.get_name(),
        )

        # Fetch list on page init
        utils.ui.run_async(self, self._controller.fetch_list, self.on_refresh_finished)
        self.is_loading = True

    @Gtk.Template.Callback()
    def on_refresh(self, button: Gtk.Button):
        if not self.is_loading:
            utils.ui.run_async(
                self,
                self._controller.fetch_list,
                self.on_refresh_finished,
                func_args=(True,),
            )
            self.is_loading = True

    def on_refresh_finished(self):
        self.is_loading = False

    @GObject.Property(type=bool, default=False, nick="is-loading")
    def is_loading(self) -> bool:
        return self._is_loading

    @is_loading.setter
    def is_loading(self, value: bool):
        self._is_loading = value

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
