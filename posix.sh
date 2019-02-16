#!/bin/sh

debug() { ! "${log_debug-false}" || log "DEBUG: $*" >&2; }
log() { printf '%s\n' "$*"; }
warn() { log "WARNING: $*" >&2; }
error() { log "ERROR: $*" >&2; }
fatal() { error "$*"; exit 1; }
try() { "$@" || fatal "'$@' failed"; }

mydir=$(cd "$(dirname "$0")" && pwd -L) || fatal "Unable to determine script directory"

cleanup() {
    debug "In cleanup"
}
trap 'cleanup' INT TERM EXIT

var=${1:-default}

# check for ${word} in ${string}
test "${string#*$word}" != "$string" && echo "$word found in $string"

# parse arguments
while [ $# -gt 0 ]; do
    case $1 in
        --help|-h)
            log "Help here"
            ;;
        --arg)
            if [ -z "$2" ]; then
                fatal "--arg is missing argument"
            fi
            param=$2
            shift
            ;;
    esac
    shift
done
