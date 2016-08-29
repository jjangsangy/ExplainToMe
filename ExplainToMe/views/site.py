from __future__ import print_function

import json
import logging
import logging.config
import os
import sys

import requests
from flask import (Blueprint, flash, jsonify, make_response, redirect,
                   render_template, request, session, url_for)
from sumy.nlp.tokenizers import Tokenizer
from wtforms.validators import URL

from ..forms import LinkForm
from ..textrank import get_parser, run_summarizer

logger = logging.getLogger(__name__)

site = Blueprint('site', __name__)

VERSION = '1.0'


def respond(recipient_id, message_text):
    logger.info(message_text)
    data = {
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    }
    resp = requests.post(
        "https://graph.facebook.com/v2.6/me/messages",
        params={"access_token": os.getenv("PAGE_ACCESS_TOKEN")},
        headers={"Content-Type": 'application/json'},
        data=json.dumps(data),
    )
    return resp


def valid_url(raw_url):
    validator = URL()
    match = validator.regex.match(raw_url)
    if not match:
        return False
    return validator.validate_hostname(match.group('host'))


def get_summary(url, max_sent, language='english'):
    tokenizer = Tokenizer(language)
    parser, meta = get_parser(url, tokenizer)
    summary = run_summarizer(parser, max_sent, language)
    return dict(
        summary=summary,
        url=url,
        meta=meta,
        max_sent=max_sent
    )


def recieve():
    data = json.loads(request.data)
    logger.info(data)
    for entry in data["entry"]:
        for message in entry['messaging']:
            if 'message' in message:
                respond(message["sender"]["id"], "thanks")
    return 'ok', 200


@site.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method.upper() == 'POST':
        return recieve()
    if request.method.upper() == 'GET':
        if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
            if request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
                return request.args['hub.challenge'], 200
            else:
                return "Verification token mismatch", 403

        return redirect(url_for('site.index'))


@site.route('/api/v{VERSION}/summary'.format(VERSION=VERSION), methods=['POST'])
def api():
    language = 'english'
    url = request.json.get('url')
    max_sent = request.json.get('max_sent', 10)
    session_data = get_summary(url, max_sent, language)
    return jsonify(**session_data)


@site.route('/summary', methods=['POST'])
def summary():
    language = 'english'
    url = request.form.get('url', '')
    max_sent = int(request.form.get('max_sent', 10))
    session.update(get_summary(url, max_sent, language))
    return redirect(url_for('site.index', _anchor='summary'))


@site.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html',
                           url=session.get('url'),
                           meta=session.get('meta'),
                           summary=session.get('summary'),
                           max_sent=session.get('max_sent'),
                           form=LinkForm())
