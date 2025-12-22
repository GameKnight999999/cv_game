#! /bin/sh
ln -sf ../poses pages/poses
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt