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
from pathlib import Path
from typing import Optional

from gi.repository import Adw, GLib, Gdk, Gio, Gtk

from ignorem import settings
from ignorem.controller import AppController
from ignorem.ui.window_main import MainWindow
from ignorem.utils import ui, worker


class IgnoremApp(Adw.Application):
    def __init__(self) -> None:
        super().__init__(
            application_id=settings.APP_ID, flags=Gio.ApplicationFlags.DEFAULT_FLAGS
        )
        self._controller = AppController.instance()
        ui.create_action(self, "refresh-list", self.on_refresh_action)
        ui.create_action(self, "create-template", self.on_create_template_action)
        ui.create_action(self, "copy-template", self.on_copy_template_action)
        ui.create_action(self, "save-template", self.on_save_template_action)
        ui.create_action(self, "about", self.on_about_action)
        ui.create_action(self, "quit", lambda *_: self.quit(), ["<primary>q"])
        self.set_accels_for_action("win.show-help-overlay", ["<primary>question"])

    def do_activate(self) -> None:
        if not self.props.active_window:
            self.main_window = MainWindow(application=self)
        self.main_window.show()

    def on_create_template_action(
        self, action: Gio.SimpleAction, param: Optional[GLib.Variant]
    ) -> None:
        self.main_window.navigation_view.push_by_tag("page-preview")

    def on_copy_template_action(
        self, action: Gio.SimpleAction, param: Optional[GLib.Variant]
    ) -> None:
        template = self._controller.template_text
        clipboard = Gdk.Display.get_clipboard(Gdk.Display.get_default())  # type: ignore
        clipboard.set(template)
        self.main_window.toast_message("Successfully copied template to clipboard")

    def on_save_template_action(
        self, action: Gio.SimpleAction, param: Optional[GLib.Variant]
    ) -> None:
        dialog = Gtk.FileChooserNative(
            transient_for=self.main_window,
            action=Gtk.FileChooserAction.SAVE,
            title="Save template",
            accept_label="Save",
            cancel_label="Cancel",
        )
        dialog.set_current_name(".gitignore")
        dialog.connect("response", self.on_save_response)
        dialog.show()

    def on_save_response(self, dialog: Gtk.FileChooserNative, response: int) -> None:
        if response == Gtk.ResponseType.ACCEPT:
            file: Gio.File = dialog.get_file()  # type: ignore
            worker.run(
                self,
                self.save_template,
                (file.get_path(),),
                callback=self.on_save_template_finished,
                error_callback=self.on_save_template_error,
            )
            self.save_template(file.get_path())  # type: ignore

    def save_template(self, path: str) -> None:
        text = self._controller.template_text
        file_path = Path(path)
        file_path.write_text(text)

    def on_save_template_finished(self, result: None) -> None:
        self.main_window.toast_message("Successfully saved template to file.")

    def on_save_template_error(self, error: BaseException) -> None:
        self.main_window.toast_message(f"Failed to save template to file: {error}")

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
