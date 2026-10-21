#!/bin/sh
# Builds the whole site. Needs Python 3 with `pip install markdown pyyaml`.
#   ./build.sh          build pages + explorer + legal landscape into _site/ and check links
#   ./build.sh pdf      also regenerate the Toolkit PDFs (needs Node + Playwright: npm i playwright)
set -e
cd "$(dirname "$0")"
python3 src/landscape/findings.py
python3 src/explorer/gen.py
python3 src/build.py --check
if [ "$1" = "pdf" ]; then
  python3 src/explorer/make_pdfs.py
  node src/explorer/topdf.js _build/pdf toolkit/pdf
  node src/explorer/tierfig.js _build/pdf toolkit/pdf
  cp -r toolkit/pdf _site/toolkit/
fi
echo "Preview: python3 -m http.server 8000 -d _site   →  http://localhost:8000/"
