#!/bin/bash
set -e

IMAGE=rick446/ansible
COMMAND=$(basename $0)

exec docker run \
  --interactive --tty --rm \
  --volume "$PWD":/wd \
  --workdir /wd \
  "$IMAGE" "$COMMAND" $@
