#!/usr/bin/bash
set -euxo pipefail

pandoc -s \
    --metadata "title=Ad-hoc lab solutions" \
    -i adhoc-lab-solutions.md \
    -o adhoc-lab-solutions.html
reveal-md ansible-fundamentals.md \
    --title "Ansible Fundamentals" \
    --theme league \
    --css css/theme.css \
    --static html
reveal-md ansible-fundamentals.md \
    --title "Ansible Fundamentals" \
    --theme league \
    --css css/theme.css \
    --print AnsibleFundamentals.pdf \
    --puppeteer-chromium-executable=`which chromium-browser`
