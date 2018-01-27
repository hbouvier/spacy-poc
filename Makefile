all: .env activate install MobyDick.txt run

.env:
	virtualenv .env

activate: .env
	@pip -V | grep '/.env/' >/dev/null 2>&1 || (printf "You must setup your python virtual environment before running make by copy/pasting the following command:\n\n\tsource .env/bin/activate\n\n" ; echo 'source .env/bin/activate' | pbcopy ; exit 1)
	
install: activate language
	pip install -r requirements.txt
	pip install --ignore-installed six

MobyDick.txt:
	wget https://www.gutenberg.org/files/2701/2701-0.txt -O MobyDick.txt

language: english

english: .env/lib/python2.7/site-packages/en_core_web_sm/__init__.py
	
.env/lib/python2.7/site-packages/en_core_web_sm/__init__.py:
	python -m spacy download en

run: activate MobyDick.txt
	python analyze.py