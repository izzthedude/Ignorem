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

from gi.repository import Adw, GObject, Gio, Gtk

from ignorem import settings
from ignorem.ui.page_preview import PreviewPage
from ignorem.ui.page_search import SearchPage


@Gtk.Template(resource_path="/com/github/izzthedude/Ignorem/ui/window-main")
class MainWindow(Adw.ApplicationWindow):
    __gtype_name__: str = "MainWindow"

    search_page: SearchPage = Gtk.Template.Child()
    preview_page: PreviewPage = Gtk.Template.Child()

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._setup_help_overlay()

        # Bind setting
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

    def _setup_help_overlay(self) -> None:
        builder = Gtk.Builder.new_from_resource(
            "/com/github/izzthedude/Ignorem/ui/help-overlay"
        )
        shortcuts_window = builder.get_object("help_overlay")
        self.set_help_overlay(shortcuts_window)


GObject.type_register(MainWindow)
