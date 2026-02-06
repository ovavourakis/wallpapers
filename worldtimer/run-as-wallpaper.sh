#!/bin/bash
# Open World Timer in default browser (use as wallpaper with a browser-in-kiosk tool, or fullscreen)
DIR="$(cd "$(dirname "$0")" && pwd)"
open "$DIR/index.html"
