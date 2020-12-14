#!/bin/bash

bash bash/start_sql.sh

python pipline.py

bash bash/end_sql.sh

