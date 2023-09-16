project(
    'Ignorem',
    version: '0.1.0-wip',
    license: 'GPL-3.0-or-later',
    default_options: [ 'warning_level=2', 'werror=false', ],
    meson_version: '>= 0.62.0',
)

APP_ID = 'com.github.izzthedude.Ignorem'
APP_NAME = meson.project_name()
APP_VERSION = meson.project_version()
APP_MODULE = 'ignorem'
APP_LICENSE = meson.project_license()
APP_LICENSE_FILES = ['COPYING']
APP_AUTHOR = 'Izzat Z.'
APP_WEBSITE = 'https://www.github.com/izzthedude/Ignorem'
APP_ISSUE_URL = 'https://github.com/izzthedude/Ignorem/issues'

gnome = import('gnome')

pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), APP_NAME)
moduledir = join_paths(pkgdatadir, APP_MODULE)

subdir('data')
subdir('po')
subdir(APP_MODULE)

gnome.post_install(
     glib_compile_schemas: true,
    gtk_update_icon_cache: true,
  update_desktop_database: true,
)
