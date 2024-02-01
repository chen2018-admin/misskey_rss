"""
-*- coding: utf-8 -*-

@Author : geteshi
@Time : 2024/1/31 17:55
@File : create.py
"""
from datetime import datetime
import sqlite3
import time
import os
from misskey import Misskey
from misskey.exceptions import MisskeyAPIException
from dotenv import load_dotenv
from jobs.sentiment import get_sentiment

load_dotenv()
env = {
    'local_only': os.getenv('LOCAL', 'False').lower() \
        in ('true', '1', 't', 'on', 'ok'),
    'visibility': os.getenv('VISIBILITY', 'public').lower(),
    'frequency': int(os.getenv('EVERY_MINUTES', '60')),
    'quantity': int(os.getenv('HOW_MANY', '1'))
}

def publish_note():
    """ Takes the latest published news and posts a note """
    import requests
    from urllib.parse import urlparse
    if env['quantity'] >= env['frequency']//2:
        env['quantity'] = env['frequency']//2-1

    db = sqlite3.connect('feed-bot.sqlite')
    c = db.cursor()
    # mk = Misskey(os.getenv('HOST'), i=os.getenv('APIKEY'))

    c.execute('''
        SELECT * FROM news 
        WHERE notedAt IS NULL OR notedAt = ''
        ORDER BY publishedAt DESC LIMIT ?
    ''', str(env['quantity']))
    data = c.fetchall()
    address = os.getenv('HOST')
    parse_res = urlparse(address)
    if parse_res.scheme == '':
        parse_res = urlparse(f'https://{address}')
    mkurl = f'{str(parse_res.scheme)}://{str(parse_res.netloc)}/api'

    if data is not None:
        for d in data:
            note_params = {
                'sentiment': get_sentiment(d[4] + d[5]),
                'text': "\n<b>" + d[4] + "</b>\n" + d[5] + " <i>(" +d[1] + ")</i>\n\n" + d[3],
                'cw': None
            }
            if note_params['sentiment'] < 0:
                note_params['cw'] = ":nsfw: News article flagged CW"
            time.sleep(2)
            try:
                msg = {
                    'text': note_params['text'],
                    "localOnly": env['local_only'],
                    "visibility": env['visibility'],
                    "viaMobile": False,
                    "i": os.getenv('APIKEY'),
                    # "visibleUserIds": [mskid],
                    "channelId": d[9] if len(d) >= 10 else None,
                    "cw": note_params['cw'],
                }
                api = requests.post(url=f"{mkurl}/notes/create", json=msg).json()
                # api = mk.notes_create(
                #     text=note_params['text'],
                #     visibility=env['visibility'],
                #     local_only=env['local_only'],
                #     cw=note_params['cw']
                # )
                n_id = api['createdNote']['id']
                n_at = int(datetime.strptime(
                    api['createdNote']['createdAt'], '%Y-%m-%dT%H:%M:%S.%fZ'
                ).timestamp())

                c.execute('''
                    UPDATE news SET sentiment = ?, noteId = ?, notedAt = ? WHERE id = ?
                ''', (note_params['sentiment'], n_id, n_at, d[0]))
                db.commit()
            except MisskeyAPIException as e:
                print(f"MK API error: {e}")
    db.close()
