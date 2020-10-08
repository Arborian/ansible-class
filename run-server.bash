#!/usr/bin/bash
set -euxo pipefail

reveal-md ansible-fundamentals.md \
    --title "Ansible Fundamentals" \
    --theme league \
    --css css/theme.css \
    -w
