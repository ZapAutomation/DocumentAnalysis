#! /bin/bash

curr_dir=$(pwd)

rm -r "$curr_dir/results" "$curr_dir/documents/txts" "$curr_dir/documents/pdfs" "$curr_dir/results.zip" "$curr_dir/questions.txt" 2> /dev/null
mkdir "$curr_dir/results" "$curr_dir/documents/txts" "$curr_dir/documents/pdfs" 2> /dev/null
