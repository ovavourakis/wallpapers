#!/bin/sh
# Leave this running while Plash uses http://127.0.0.1:8766/index.html.
wallpaper_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec python3 "$wallpaper_dir/serve-wallpaper.py" "$@"
