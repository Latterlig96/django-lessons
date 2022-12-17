#!/bin/bash


# Section 1- Bash options
set -o errexit  
set -o nounset

daphne -b 0.0.0.0 -p 9010 ${DJANGO_ASGI_GATEWAY}