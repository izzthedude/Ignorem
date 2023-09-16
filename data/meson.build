pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
gnome = import('gnome')
python = import('python')

# Install
conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)
configure_file(
  input: 'ignorem.py.in',
  output: 'ignorem',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr--r--'
)

# Compile gresource
gnome.compile_resources(
    'ignorem',
    'com.github.izzthedude.Ignorem.gresource.xml',
    gresource_bundle: true,
    install: true,
    install_dir: pkgdatadir,
)

# Validate desktop entry file
desktop_file = i18n.merge_file(
        input: 'com.github.izzthedude.Ignorem.desktop.in',
       output: 'com.github.izzthedude.Ignorem.desktop',
         type: 'desktop',
       po_dir: '../po',
      install: true,
  install_dir: join_paths(get_option('datadir'), 'applications')
)
desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
  test('Validate desktop file', desktop_utils, args: [desktop_file])
endif

# Validate appstream file
appstream_file = i18n.merge_file(
        input: 'com.github.izzthedude.Ignorem.appdata.xml.in',
       output: 'com.github.izzthedude.Ignorem.appdata.xml',
       po_dir: '../po',
      install: true,
  install_dir: join_paths(get_option('datadir'), 'appdata')
)
appstream_util = find_program('appstream-util', required: false)
if appstream_util.found()
  test('Validate appstream file', appstream_util, args: ['validate', appstream_file])
endif

# Validate schema file
install_data('com.github.izzthedude.Ignorem.gschema.xml',
  install_dir: join_paths(get_option('datadir'), 'glib-2.0/schemas')
)
compile_schemas = find_program('glib-compile-schemas', required: false)
if compile_schemas.found()
  test('Validate schema file',
       compile_schemas,
       args: ['--strict', '--dry-run', meson.current_source_dir()])
endif

subdir('icons')
