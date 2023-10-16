from typing import Any

from gi.repository import Adw, GObject, Gdk, Gtk
from requests.exceptions import ConnectionError, ReadTimeout

from ignorem.controller import AppController
from ignorem.gitignoreio.models import TemplateModel
from ignorem.ui.widgets import AddablePill, DeletablePill, TemplatePill, TemplatePillBox
from ignorem.utils import ui, worker


@Gtk.Template(resource_path="/com/github/izzthedude/Ignorem/ui/page-search")
class SearchPage(Adw.NavigationPage):  # type: ignore
    __gtype_name__: str = "SearchPage"

    ERROR_OCCURRED = "error-occurred"

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
    create_button: Gtk.Button = Gtk.Template.Child()

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._controller = AppController.instance()
        self._is_loading: bool = False
        self._init()

        # Fetch list on page init
        self.request_list()
        self.is_loading = True

    @GObject.Property(type=bool, default=False, nick="is-loading")
    def is_loading(self) -> bool:
        return self._is_loading

    @is_loading.setter  # type: ignore
    def is_loading(self, value: bool) -> None:
        self._is_loading = value

    def request_list(self, fetch: bool = False) -> None:
        self.is_loading = True
        worker.run(
            self,
            self._controller.request_list,
            (fetch,),
            callback=self.on_request_list_finished,
            error_callback=self.on_request_error,
        )

    def on_request_list_finished(self, result: None) -> None:
        self.populate_suggestions(self._controller.templates())
        self.is_loading = False

    def on_request_error(self, error: BaseException) -> None:
        icon_name = "dialog-error-symbolic"
        title = "Unexpected Error"
        description = "An unexpected error occurred. Please check the logs."

        if isinstance(error, ConnectionError):
            icon_name = "network-error-symbolic"
            title = "Network Error"
            description = (
                "A network error has occurred. This may be caused by a "
                "DNS failure, refused connection, or no internet connection."
            )

        elif isinstance(error, ReadTimeout):
            icon_name = "network-no-route-symbolic"
            title = "Connection Timed Out"
            description = (
                "Request took too long to respond. Check your internet connection."
            )

        self.emit(self.ERROR_OCCURRED, icon_name, title, description)
        self.is_loading = False

    @worker.run_decorator()
    def populate_suggestions(self, templates: list[TemplateModel]) -> None:
        self.suggestions_pillbox.clear()
        for template in templates:
            pill = AddablePill(template)
            pill.set_sensitive(not self._controller.is_selected(template))
            pill.action_button.connect("clicked", self.on_suggestion_clicked, pill)
            self.suggestions_pillbox.add_pill(pill)

    def on_suggestion_clicked(self, button: Gtk.Button, pill: AddablePill) -> None:
        self._controller.add_selected(pill.template)

        selected_pill = DeletablePill(pill.template)
        selected_pill.action_button.connect(
            "clicked", self.on_selected_clicked, selected_pill
        )
        self.selected_pillbox.add_pill(selected_pill)

        pill.set_sensitive(False)
        self._update_actionbar_visibility()

    def on_selected_clicked(self, button: Gtk.Button, pill: DeletablePill) -> None:
        self._controller.remove_selected(pill.template)
        self.selected_pillbox.remove_pill(pill)

        suggestion_pill = self.suggestions_pillbox.get_pill_by_template(pill.template)
        suggestion_pill.set_sensitive(True)  # type: ignore

        self._update_actionbar_visibility()

    def on_refresh(self) -> None:
        if not self.is_loading:
            self.is_loading = True
            worker.run(
                self,
                self._controller.request_list,
                (True,),
                callback=self.on_request_list_finished,
                error_callback=self.on_request_error,
            )

    @Gtk.Template.Callback()
    def on_search_changed(self, entry: Gtk.SearchEntry) -> None:
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

    def on_suggestions_visible(
        self, _: Any, __: Any, allocation: Gdk.Rectangle
    ) -> None:
        entry_allocation = self.search_entry.get_allocation()
        self.suggestions_box.set_size_request(entry_allocation.width, -1)

    @Gtk.Template.Callback()
    def on_create_clicked(self, button: Gtk.Button) -> None:
        self.is_loading = True
        worker.run(
            self,
            self._controller.request_template,
            callback=self.on_request_template_finished,
            error_callback=self.on_request_error,
        )

    def on_request_template_finished(self, result: None) -> None:
        self.create_button.activate_action("app.create-template")
        self.is_loading = False

    @Gtk.Template.Callback()
    def on_debug_clicked(self, button: Gtk.Button) -> None:
        print("debug")

    def _init(self) -> None:
        self.bind_property(
            "is-loading",
            self.search_stack,
            "visible-child-name",
            GObject.BindingFlags.DEFAULT | GObject.BindingFlags.SYNC_CREATE,
            lambda *_: self.loading_page.get_name()
            if self.is_loading
            else self.search_page.get_name(),
        )

        self.bind_property(
            "is-loading",
            self.search_actionbar,
            "revealed",
            GObject.BindingFlags.DEFAULT | GObject.BindingFlags.SYNC_CREATE,
            lambda *_: not self.is_loading and bool(self._controller.selected()),
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

    def _pillbox_filter_func(self, child: Gtk.FlowBoxChild) -> bool:
        pill: TemplatePill = child.get_child()
        text = self.search_entry.get_text()
        return text.lower() in pill.template.name.lower()

    def _pillbox_sort_func(
        self, child1: Gtk.FlowBoxChild, child2: Gtk.FlowBoxChild
    ) -> bool:
        pill1: TemplatePill = child1.get_child()
        pill2: TemplatePill = child2.get_child()
        return pill1.template.name.lower() > pill2.template.name.lower()

    def _on_key_pressed(
        self,
        controller: Gtk.EventControllerKey,
        key_value: int,
        key_code: int,
        state: Gdk.ModifierType,
    ) -> None:
        if key_value == 65307:  # Escape
            self.suggestions_box.set_visible(False)

    def _on_mouse_clicked(
        self, gesture: Gtk.Gesture, n_press: int, x: float, y: float
    ) -> None:
        allocation = self.suggestions_box.get_allocation()
        if not allocation.contains_point(int(x), int(y)):
            self.suggestions_box.set_visible(False)

    def _update_actionbar_visibility(self) -> None:
        self.search_actionbar.set_revealed(bool(self.selected_pillbox.pills()))


ui.register_type(SearchPage)
ui.register_signal(
    SearchPage.ERROR_OCCURRED,
    SearchPage,
    GObject.SignalFlags.RUN_FIRST,
    GObject.TYPE_NONE,
    (
        str,  # icon_name
        str,  # title
        str,  # description
    ),
)
