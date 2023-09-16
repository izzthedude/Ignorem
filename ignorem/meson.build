pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'ignorem')

ignorem_sources = [
  '__init__.py',
  'app.py',
]
install_subdir('ui', install_dir: moduledir)
install_data(ignorem_sources, install_dir: moduledir)
