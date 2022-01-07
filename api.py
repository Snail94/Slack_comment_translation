# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import slack
from flask import Flask, request, Response
import os
import json
from pathlib import Path
from dotenv import load_dotenv
from slackeventsapi import SlackEventAdapter
import translation
import database as db

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)


slack_events_adapter = SlackEventAdapter(
    os.environ['Signing_Secret'], '/slack/events', app)

slack_client = slack.WebClient(token=os.environ['Slack_Token'])


@app.route('/target/<targetid>/comments', methods=['get', 'post'])
def get_comments(targetid):
    target_comment = db.select_query({"publishedAt": targetid})
    target_replies = db.select_query({"targetId": targetid})
    response = target_comment + target_replies
    return json.dumps(response, default=str)


# connecter au db voir si le target est présent sinon retourner une erreur

@app.route("/components/schemas/NewComment", methods=['post'])
def add_comment():
    request_data = request.json
    print(json.dumps(request_data))
    print(request_data['targetId'])
    print("qsd", request_data['targetId'] != 'None')
    if request_data['targetId'] != 'None' and db.get_id({
                "targetId": request_data['targetId']}) != []:
        x = db.insert_comment(request_data)
        return {"x": x}
    else:
        return Response("Error", status=400,)


@slack_events_adapter.on("message")
def handle_message(event_data):
    print("received : ", event_data)
    if 'bot_id' not in event_data.get("event"):
        message = event_data.get("event")
        resp = message.get("text")
        ts = message.get('ts')
        tra = translation.handle_traduction(resp)
        db.insert_message(event_data)
        return send_reply(ts, tra)
    elif 'bot_id' in event_data.get("event_data"):
        db.insert_message(event_data)


@slack_events_adapter.on("error")
def error_handler(err):
    print('Error:' + str(err))


def send_reply(target: str, comment: str, broadcast=None):
    result = slack_client.chat_postMessage(
        channel=os.environ["channel"],
        thread_ts=target,
        text=comment,
        reply_broadcast=broadcast
        )
    return result


if __name__ == "__main__":
    app.run(debug=True)
