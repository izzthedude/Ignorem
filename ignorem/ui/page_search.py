from gi.repository import Adw, GObject, Gdk, Gtk

from ignorem import utils
from ignorem.controller import AppController
from ignorem.ui.widgets import SearchSuggestionsBox, TemplatePill


@Gtk.Template(resource_path="/com/github/izzthedude/Ignorem/ui/page-search")
class SearchPage(Adw.NavigationPage):
    __gtype_name__ = "SearchPage"

    search_stack: Adw.ViewStack = Gtk.Template.Child()

    search_page: Adw.ViewStackPage = Gtk.Template.Child()
    overlay: Gtk.Overlay = Gtk.Template.Child()
    search_entry: Gtk.SearchEntry = Gtk.Template.Child()
    suggestions_box: SearchSuggestionsBox = Gtk.Template.Child()

    loading_page: Adw.ViewStackPage = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._controller = AppController.instance()
        self._is_loading: bool = False
        self._current_filter: str = ""
        self._init()

        # Fetch list on page init
        utils.ui.run_async(self, self.populate_templates, self.on_refresh_finished)
        self.is_loading = True

    def populate_templates(self, fetch: bool = False):
        templates = self._controller.fetch_list(fetch)

        # Populate suggestions box
        pill_box = self.suggestions_box.templatepill_box
        for template in templates:
            pill = TemplatePill(template)
            pill_box.append(pill)

    @Gtk.Template.Callback()
    def on_refresh(self, button: Gtk.Button):
        if not self.is_loading:
            utils.ui.run_async(
                self,
                self.populate_templates,
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
        self._current_filter = entry.get_text()

        self.suggestions_box.templatepill_box.invalidate_sort()
        self.suggestions_box.templatepill_box.invalidate_filter()

        # Only doing this for
        results = [
            template
            for template in self._controller.templates()
            if self._current_filter.lower() in template.name.lower()
        ]
        self.suggestions_box.set_results_found(bool(results))
        self.suggestions_box.set_visible(bool(self._current_filter))

    @Gtk.Template.Callback()
    def on_create_clicked(self, button: Gtk.Button):
        print("clear")

    @Gtk.Template.Callback()
    def on_debug_clicked(self, button: Gtk.Button):
        print("debug")

    def on_suggestions_visible(self, _, __, allocation: Gdk.Rectangle):
        entry_allocation = self.search_entry.get_allocation()
        self.suggestions_box.set_size_request(entry_allocation.width, -1)
        self.suggestions_box.set_margin_top(180)

    def _init(self):
        pill_box = self.suggestions_box.templatepill_box
        pill_box.set_filter_func(self._pillbox_filter_func)
        pill_box.set_sort_func(self._pillbox_sort_func)

        # Have to bind here cause it wouldn't work in the ui file for some reason
        self.bind_property(
            "is-loading",
            self.search_stack,
            "visible-child-name",
            GObject.BindingFlags.DEFAULT | GObject.BindingFlags.SYNC_CREATE,
            lambda *_: self.loading_page.get_name()
            if self.is_loading
            else self.search_page.get_name(),
        )

        self.overlay.connect("get-child-position", self.on_suggestions_visible)

    def _pillbox_filter_func(self, child: Gtk.FlowBoxChild):
        pill: TemplatePill = child.get_child()
        return self._current_filter.lower() in pill.template.name.lower()

    def _pillbox_sort_func(self, child1: Gtk.FlowBoxChild, child2: Gtk.FlowBoxChild):
        pill1: TemplatePill = child1.get_child()
        pill2: TemplatePill = child2.get_child()
        return pill1.template.name.lower() > pill2.template.name.lower()
