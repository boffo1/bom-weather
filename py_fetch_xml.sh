#!/usr/bin/env bash
## py_fetch_xml.sh

set -e

# Keep all project files together under ~/bin/bom/bom-weather-py
PROJECT_DIR="$HOME/bin/bom/bom-weather-py"
CACHE_DIR="$PROJECT_DIR"
PRODUCT="IDV60920"

# ensure project cache directory exists
mkdir -p "$CACHE_DIR"

local_xml="$CACHE_DIR/${PRODUCT}.xml"
ftp_url="ftp://ftp.bom.gov.au/anon/gen/fwo/${PRODUCT}.xml"
tmp="${local_xml}.tmp"

curl -# -f -z "$local_xml" "$ftp_url" -o "$tmp"
sleep 1
mv "$tmp" "$local_xml"
