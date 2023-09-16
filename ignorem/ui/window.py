# window.py
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

from gi.repository import Adw
from gi.repository import Gtk


@Gtk.Template(resource_path="/com/github/izzthedude/Ignorem/ui/window")
class MainWindow(Adw.ApplicationWindow):
    __gtype_name__ = "IgnoremWindow"

    label = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._setup_help_overlay()

    def _setup_help_overlay(self):
        builder = Gtk.Builder.new_from_resource(
            "/com/github/izzthedude/Ignorem/ui/help-overlay"
        )
        shortcuts_window = builder.get_object("help_overlay")
        self.set_help_overlay(shortcuts_window)