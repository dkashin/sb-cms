#!/bin/bash

# Check repo catalog
curl -s -u developer:sta123 https://reg.tebox.eu/v2/_catalog | jq .

# Check repo tags
curl -s -u developer:sta123 https://reg.tebox.eu/v2/stabox/router/tags/list | jq .
