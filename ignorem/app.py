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

from gi.repository import Adw, GObject, Gio, Gtk

from ignorem import utils
from ignorem.controller import AppController
from ignorem.enums import Ignorem
from ignorem.ui import MainWindow, PreviewPage, SearchPage
from ignorem.ui.widgets import SearchSuggestionsBox, TemplatePill, TemplatePillBox


class IgnoremApp(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id=Ignorem.ID,
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )
        utils.ui.create_action(self, "preferences", self.on_preferences_action)
        utils.ui.create_action(self, "about", self.on_about_action)
        utils.ui.create_action(self, "quit", lambda *_: self.quit(), ["<primary>q"])
        self.set_accels_for_action("win.show-help-overlay", ["<primary>question"])

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = MainWindow(application=self)
        win.present()

    def on_about_action(self, widget, _):
        about = Adw.AboutWindow(
            transient_for=self.props.active_window,
            application_name=Ignorem.NAME,
            application_icon=Ignorem.ID,
            version=Ignorem.VERSION,
            developer_name=Ignorem.AUTHOR,
            developers=[Ignorem.AUTHOR],
            copyright="© 2023 Izzat Z.",
            license_type=Gtk.License.GPL_3_0,
            website=Ignorem.WEBSITE,
            issue_url=Ignorem.ISSUE_URL,
        )
        about.present()

    def on_preferences_action(self, widget, _):
        print("app.preferences action activated")


def _register_types():
    GObject.type_register(MainWindow)
    GObject.type_register(SearchPage)
    GObject.type_register(PreviewPage)
    GObject.type_register(TemplatePillBox)
    GObject.type_register(TemplatePill)
    GObject.type_register(SearchSuggestionsBox)


def main(version):
    _register_types()
    AppController.instance()  # Initialise controller
    app = IgnoremApp()
    return app.run(sys.argv)
