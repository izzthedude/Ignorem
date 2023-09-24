scalable_dir = join_paths('hicolor', 'scalable', 'apps')
symbolic_dir = join_paths('hicolor', 'symbolic', 'apps')

scalable_icons = [
    '@0@.svg'.format(APP_ID),
]
symbolic_icons = [
    '@0@-symbolic.svg'.format(APP_ID),
    'git-symbolic.svg'.format(APP_ID),
]

install_data(
  scalable_icons,
  install_dir: join_paths(get_option('datadir'), 'icons', scalable_dir),
)
install_data(
  symbolic_icons,
  install_dir: join_paths(get_option('datadir'), 'icons', symbolic_dir)
)
