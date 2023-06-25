#!/bin/bash

python3 -m FidoSelf
gunicorn myapp.wsgi --log-file -
