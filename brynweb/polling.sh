#!/usr/bin/env bash

dir=$1
cd $dir

source ../venv/bin/activate
python manage.py runscript hypervisor_stats
