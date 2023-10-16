# window_main.py
#
# Copyright 2023 Izzat Z.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later
from typing import Any

from gi.repository import Adw, Gio, Gtk

from ignorem import settings
from ignorem.ui.page_preview import PreviewPage
from ignorem.ui.page_search import SearchPage
from ignorem.utils import ui


@Gtk.Template(resource_path="/com/github/izzthedude/Ignorem/ui/window-main")
class MainWindow(Adw.ApplicationWindow):
    __gtype_name__: str = "MainWindow"

    toast_overlay: Adw.ToastOverlay = Gtk.Template.Child()

    navigation_view: Adw.NavigationView = Gtk.Template.Child()  # type: ignore
    search_page: SearchPage = Gtk.Template.Child()
    preview_page: PreviewPage = Gtk.Template.Child()

    error_page: Adw.NavigationPage = Gtk.Template.Child()  # type: ignore
    status_page: Adw.StatusPage = Gtk.Template.Child()
    home_button: Gtk.Button = Gtk.Template.Child()
    logs_button: Gtk.Button = Gtk.Template.Child()

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._setup_help_overlay()
        self._bind_settings()

        self.search_page.connect(SearchPage.ERROR_OCCURRED, self.on_error_occurred)

    def toast_message(self, message: str) -> None:
        toast = Adw.Toast(title=message, timeout=5)
        self.toast_overlay.add_toast(toast)

    def on_error_occurred(
        self, page: SearchPage, icon_name: str, title: str, description: str
    ) -> None:
        self.status_page.set_icon_name(icon_name)
        self.status_page.set_title(title)
        self.status_page.set_description(description)
        self.navigation_view.push_by_tag(self.error_page.get_tag())

    @Gtk.Template.Callback()
    def on_home_clicked(self, button: Gtk.Button) -> None:
        self.navigation_view.pop_to_tag(self.search_page.get_tag())

    @Gtk.Template.Callback()
    def on_logs_clicked(self, button: Gtk.Button) -> None:
        print("logs")  # TODO

    def _setup_help_overlay(self) -> None:
        builder = Gtk.Builder.new_from_resource(
            "/com/github/izzthedude/Ignorem/ui/help-overlay"
        )
        shortcuts_window = builder.get_object("help_overlay")
        self.set_help_overlay(shortcuts_window)  # type: ignore

    def _bind_settings(self) -> None:
        settings_ = Gio.Settings(schema_id=settings.APP_ID)
        settings_.bind(
            "window-width", self, "default-width", Gio.SettingsBindFlags.DEFAULT
        )
        settings_.bind(
            "window-height", self, "default-height", Gio.SettingsBindFlags.DEFAULT
        )
        settings_.bind(
            "window-maximized", self, "maximized", Gio.SettingsBindFlags.DEFAULT
        )


ui.register_type(MainWindow)
