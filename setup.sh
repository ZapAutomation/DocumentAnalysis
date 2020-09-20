#! /bin/bash

python3 -m pip install -q -r requirements.txt

wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.6.2-linux-x86_64.tar.gz -q
tar -xzf elasticsearch-7.6.2-linux-x86_64.tar.gz
chown -R daemon:daemon elasticsearch-7.6.2

main_dir=$(pwd)

mkdir documents
mkdir results
cd documents
mkdir pdfs
mkdir txts
