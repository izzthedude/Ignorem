# Define values in settings.py from the top-most meson.build variables
conf = configuration_data()
conf.set('APP_ID', APP_ID)
conf.set('APP_NAME', APP_NAME)
conf.set('APP_VERSION', APP_VERSION)
conf.set('APP_AUTHOR', APP_AUTHOR)
conf.set('APP_LICENSE', APP_LICENSE)
conf.set('APP_WEBSITE', APP_WEBSITE)
conf.set('APP_ISSUE_URL', APP_ISSUE_URL)
configure_file(
  input: 'settings.py',
  output: 'settings.py',
  configuration: conf,
  install: true,
  install_dir: moduledir,
  install_mode: 'r-xr--r--'
)

ignorem_sources = [
  '__init__.py',
  'constants.py',
  'controller.py',
  # settings.py no need, it's handled above.
]
install_subdir('base', install_dir: moduledir)
install_subdir('gitignoreio', install_dir: moduledir)
install_subdir('ui', install_dir: moduledir)
install_subdir('utils', install_dir: moduledir)
install_data(ignorem_sources, install_dir: moduledir)
