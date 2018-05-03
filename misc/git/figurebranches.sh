#!/bin/bash

branches=()
branches_string="$(git ls-remote --heads origin | cut -f2 | sed -e "s/^refs\/heads\///")"
if [ -z "$branches_string" ]; then
    exit 2
fi
while read -r line; do branches+=("$line"); done <<<"$branches_string"

bucket_save=()
bucket_delete=()
bucket_ask=()

for branch in "${branches[@]}"; do
    while true; do
        printf "Where should the branch \"$branch\" be put?: "
        read input
        case "$input" in
            a)
                bucket_ask+=("$branch")
                break
                ;;
            s)
                bucket_save+=("$branch")
                break
                ;;
            d)
                bucket_delete+=("$branch")
                break
                ;;
            *) 
                echo "Invalid selection, try again!"
                ;;
        esac
    done
done

echo "All branches processed"
echo "\n\n\tSave:"
for branch in "${bucket_save[@]}"; do
    echo "$branch"
done

echo "\n\n\tDelete:"
for branch in "${bucket_delete[@]}"; do
    echo "$branch"
done

echo "\n\n\tAsk:"
for branch in "${bucket_ask[@]}"; do
    echo "$branch"
done