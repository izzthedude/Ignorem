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

import logging
import sys
from typing import Optional

from gi.repository import Adw, GLib, Gio, Gtk

from ignorem import settings
from ignorem.controller import AppController
from ignorem.gui.utils import functions as gui
from ignorem.gui.utils import worker
from ignorem.gui.window import IgnoremWindow

logger = logging.getLogger(__name__)


class IgnoremApp(Adw.Application):
    def __init__(self) -> None:
        super().__init__(
            application_id=settings.APP_ID, flags=Gio.ApplicationFlags.DEFAULT_FLAGS
        )
        self._controller = AppController.instance()
        gui.create_action(self, "refresh-list", self.on_refresh_action)
        gui.create_action(self, "create-template", self.on_create_template_action)
        gui.create_action(self, "copy-template", self.on_copy_template_action)
        gui.create_action(self, "save-template", self.on_save_template_action)
        gui.create_action(self, "open-logs", gui.open_logs)
        gui.create_action(self, "about", self.on_about_action)
        gui.create_action(self, "quit", lambda *_: self.quit(), ["<primary>q"])
        self.set_accels_for_action("win.show-help-overlay", ["<primary>question"])

    def do_activate(self) -> None:
        logger.info("Starting application")
        if not self.props.active_window:
            self.main_window = IgnoremWindow(application=self)
        self.main_window.show()

    def do_shutdown(self) -> None:
        # FIXME: This causes an Adw critical error but idk how to fix it
        logger.info("Shutting down application")

    def on_refresh_action(
        self,
        action: Gio.SimpleAction,
        param: Optional[GLib.Variant],
    ) -> None:
        self.main_window.search_page.on_refresh()

    def on_create_template_action(
        self,
        action: Gio.SimpleAction,
        param: Optional[GLib.Variant],
    ) -> None:
        self.main_window.navigation_view.push_by_tag("page-preview")

    def on_copy_template_action(
        self,
        action: Gio.SimpleAction,
        param: Optional[GLib.Variant],
    ) -> None:
        gui.copy_to_clipboard(self._controller.template_text)
        message = "Successfully copied template to clipboard"
        logger.info(message)
        self.main_window.toast_message(message)

    def on_save_template_action(
        self,
        action: Gio.SimpleAction,
        param: Optional[GLib.Variant],
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
                gui.save_template,
                (
                    self._controller.template_text,
                    file.get_path(),
                ),
                callback=self.on_save_template_finished,
                error_callback=self.on_save_template_error,
            )

    def on_save_template_finished(self, result: None) -> None:
        message = "Successfully saved template to file"
        logger.info(message)
        self.main_window.toast_message(message)

    def on_save_template_error(self, error: BaseException) -> None:
        logger.warning(f"Failed to save template due to error: {error}", exc_info=error)
        self.main_window.toast_action(
            "app.open-logs",
            "Check logs",
            "Failed to save template to file. Check logs for more info.",
        )

    def on_about_action(
        self,
        action: Gio.SimpleAction,
        param: Optional[GLib.Variant],
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
