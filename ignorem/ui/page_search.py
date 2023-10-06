from gi.repository import Adw, GObject, Gdk, Gtk

from ignorem.controller import AppController
from ignorem.ui.widgets import AddablePill, DeletablePill, TemplatePill, TemplatePillBox
from ignorem.utils import ui


@Gtk.Template(resource_path="/com/github/izzthedude/Ignorem/ui/page-search")
class SearchPage(Adw.NavigationPage):
    __gtype_name__ = "SearchPage"

    search_stack: Adw.ViewStack = Gtk.Template.Child()

    search_page: Adw.ViewStackPage = Gtk.Template.Child()
    overlay: Gtk.Overlay = Gtk.Template.Child()
    search_entry: Gtk.SearchEntry = Gtk.Template.Child()
    suggestions_box: Gtk.ScrolledWindow = Gtk.Template.Child()
    suggestions_pillbox: TemplatePillBox = Gtk.Template.Child()
    selected_pillbox: TemplatePillBox = Gtk.Template.Child()
    no_results_label: Gtk.Label = Gtk.Template.Child()

    loading_page: Adw.ViewStackPage = Gtk.Template.Child()

    search_actionbar: Gtk.ActionBar = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._controller = AppController.instance()
        self._is_loading: bool = False
        self._init()

        # Fetch list on page init
        ui.run_async(self, self.populate_templates, self.on_refresh_finished)
        self.is_loading = True

    def populate_templates(self, fetch: bool = False):
        templates = self._controller.fetch_list(fetch)

        # Populate suggestions box
        pill_box = self.suggestions_pillbox
        for template in templates:
            pill = AddablePill(template)
            pill.action_button.connect("clicked", self.on_suggestion_clicked, pill)
            pill_box.append(pill)

    def on_suggestion_clicked(self, _, pill: AddablePill):
        selected_pill = DeletablePill(pill.template)
        selected_pill.action_button.connect("clicked", self.on_selected_deleted, pill)
        self.selected_pillbox.append(selected_pill)

        pill.set_sensitive(False)
        self._update_actionbar_visibility()

    def on_selected_deleted(self, _, pill: AddablePill):
        pill.set_sensitive(True)
        self._update_actionbar_visibility()

    def on_refresh(self):
        if not self.is_loading:
            ui.run_async(
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
        text = entry.get_text()

        self.suggestions_pillbox.invalidate_sort()
        self.suggestions_pillbox.invalidate_filter()

        # Determine if app should display pills or no results
        results = [
            template
            for template in self._controller.templates()
            if text.lower() in template.name.lower()
        ]
        self.no_results_label.set_visible(not bool(results))
        self.suggestions_box.set_visible(bool(text))

    @Gtk.Template.Callback()
    def on_create_clicked(self, button: Gtk.Button):
        for pill in self.selected_pillbox.pills():
            self._controller.add_selected_template(pill.template)
        self.search_entry.set_text("")

    @Gtk.Template.Callback()
    def on_debug_clicked(self, button: Gtk.Button):
        print("debug")

    def on_suggestions_visible(self, _, __, allocation: Gdk.Rectangle):
        entry_allocation = self.search_entry.get_allocation()
        self.suggestions_box.set_size_request(entry_allocation.width, -1)

    def _update_actionbar_visibility(self):
        self.search_actionbar.set_revealed(bool(self.selected_pillbox.pills()))

    def _init(self):
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

        self.suggestions_pillbox.set_filter_func(self._pillbox_filter_func)
        self.suggestions_pillbox.set_sort_func(self._pillbox_sort_func)

        # Escape/click outside the suggestion box to hide it
        key_controller = Gtk.EventControllerKey()
        key_controller.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
        key_controller.connect("key-pressed", self._on_key_pressed)
        self.overlay.add_controller(key_controller)

        gesture = Gtk.GestureClick()
        gesture.connect("pressed", self._on_mouse_clicked)
        self.overlay.add_controller(gesture)

        self.overlay.connect("get-child-position", self.on_suggestions_visible)

    def _pillbox_filter_func(self, child: Gtk.FlowBoxChild):
        pill: TemplatePill = child.get_child()
        text = self.search_entry.get_text()
        return text.lower() in pill.template.name.lower()

    def _pillbox_sort_func(self, child1: Gtk.FlowBoxChild, child2: Gtk.FlowBoxChild):
        pill1: TemplatePill = child1.get_child()
        pill2: TemplatePill = child2.get_child()
        return pill1.template.name.lower() > pill2.template.name.lower()

    def _on_key_pressed(
        self,
        controller: Gtk.EventControllerKey,
        key_value: int,
        key_code: int,
        state: Gdk.ModifierType,
    ):
        if key_value == 65307:  # Escape
            self.suggestions_box.set_visible(False)

    def _on_mouse_clicked(self, gesture: Gtk.Gesture, n_press: int, x: float, y: float):
        allocation = self.suggestions_box.get_allocation()
        if not allocation.contains_point(int(x), int(y)):
            self.suggestions_box.set_visible(False)


GObject.type_register(SearchPage)
