#!/bin/bash

apt-get update
apt-get install -y graphviz
python -m spacy download en_core_web_sm