#!/bin/sh
grep -r -h -o -E '([a-z2-7]{16})' list | grep -E '([2-7].*[a-z]|[a-z].*[2-7])' | sort | uniq > list.txt

