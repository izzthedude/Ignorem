# app.py
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

import sys
from typing import Optional

from gi.repository import Adw, GLib, Gio, Gtk

from ignorem import settings
from ignorem.ui.window_main import MainWindow
from ignorem.utils import ui


class IgnoremApp(Adw.Application):
    def __init__(self) -> None:
        super().__init__(
            application_id=settings.APP_ID, flags=Gio.ApplicationFlags.DEFAULT_FLAGS
        )
        ui.create_action(self, "refresh", self.on_refresh_action)
        ui.create_action(self, "about", self.on_about_action)
        ui.create_action(self, "quit", lambda *_: self.quit(), ["<primary>q"])
        self.set_accels_for_action("win.show-help-overlay", ["<primary>question"])

    def do_activate(self) -> None:
        if not self.props.active_window:
            self.main_window = MainWindow(application=self)
        self.main_window.show()

    def on_refresh_action(
        self, action: Gio.SimpleAction, param: Optional[GLib.Variant]
    ) -> None:
        self.main_window.search_page.on_refresh()

    def on_about_action(
        self, action: Gio.SimpleAction, param: Optional[GLib.Variant]
    ) -> None:
        about = Adw.AboutWindow(
            transient_for=self.props.active_window,
            application_name=settings.APP_NAME,
            application_icon=settings.APP_ID,
            version=settings.APP_VERSION,
            developer_name=settings.APP_AUTHOR,
            developers=[settings.APP_AUTHOR],
            copyright="© 2023 Izzat Z.",
            license_type=Gtk.License.GPL_3_0,
            website=settings.APP_WEBSITE,
            issue_url=settings.APP_ISSUE_URL,
        )
        about.present()


def main(version: str) -> int:
    app = IgnoremApp()
    return app.run(sys.argv)
