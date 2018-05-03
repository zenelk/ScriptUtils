#!/bin/bash

input_lines="$(cat $1)"
result=""

for line in $input_lines; do
	echo "git branch -D $line"
	git branch -D $line
	echo "git push origin :$line"
	git push origin :$line
done

echo "$result"