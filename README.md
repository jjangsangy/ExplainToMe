# ExplainToMe

[![travis](https://travis-ci.org/jjangsangy/ExplainToMe.svg?branch=master)](https://travis-ci.org/jjangsangy/ExplainToMe)
[![licence](https://img.shields.io/pypi/l/coverage.svg)](https://github.com/jjangsangy/ExplainToMe/blob/master/LICENSE)

## Text Summarization for Humans

![image](static/front.png)

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

# What is it?

`Explain To Me` is a automatic text summarizer, that utilizes
[TextRank](http://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf),
a graph based algorithm to scans through the contents of a website to
extract a concise machine generated summary. The methodology is similar
to the way search engines return the most relevant web pages from a
users search query.

# Quickstart

# Install

## Clone Repository

```bash
$ git clone https://github.com/jjangsangy/ExplainToMe.git
```

## Create a virtualenv

Currently we only support Python 2 due to the a dependency on [Python-Goose](https://github.com/grangier/python-goose)

```bash
$ virtualenv -p python2 venv
```

## Source Virtualenv

```bash
$ source venv/bin/activate
```

## Install Python Dependencies

```bash
$ pip install --upgrade pip setuptools wheel
$ pip install -r requirements.txt
```

## Run Server

```bash
$ python manage.py runserver
Running on http://127.0.0.1:8080/ (Press CTRL+C to quit)
```

# Things to look forward to:

-   Summaries of documents in other languages than English!
