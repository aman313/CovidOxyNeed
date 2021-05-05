#!/usr/bin/env bash
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo apt-get install mongodb-org-shell

#python -m spacy download en_core_web_sm
# nltk.download('averaged_perceptron_tagger')
#nltk.download('maxent_ne_chunker')
# nltk.download('words')