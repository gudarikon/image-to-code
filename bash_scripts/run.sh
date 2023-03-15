#!/bin/bash
tmux kill-session -t 0
tmux new -ds0 'source ~/projects/image-to-code-venv/bin/activate; PYTHONPATH=./ python3 ./src/telegram_handler/bot.py; exec $SHELL'
