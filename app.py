# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 16:46:23 2019

@author: user
"""
import base64
import json
import os
import google.auth
import tempfile
import io
import re
from flask import Flask, request, abort
from tempfile import NamedTemporaryFile

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError,LineBotApiError
)
from linebot.models import *
#from google.cloud import vision
from google.cloud import pubsub_v1
from google.cloud import storage
from google.cloud import translate
from google.cloud import vision

#import sys
#import gspread
#from oauth2client.service_account import ServiceAccountCredentials

#GDOCS_OAUTH_JSON = 'My First Project-4a3bbf5367dd.json' 
#GDOCS_SPREADSHEET_NAME = "LineBot"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "My First Project-4a3bbf5367dd.json"
vision_client = vision.ImageAnnotatorClient()
translate_client = translate.Client()
publisher = pubsub_v1.PublisherClient()
storage_client = storage.Client()

credentials, project_id = google.auth.default()

'''with open('config.json') as f:
    data = f.read()
config = json.loads(data)
'''
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
app = Flask(__name__)

# channel Access Token
line_bot_api = LineBotApi('KH38RTHaoQRq05iJ2t9aWN+M9pC26tC5SWEtmTREYWlEvTcQEb9eI/WUH/I+AUImrOdxtIyiEOW485A/8gr08gvAzvbE/qdFFaiWLW0ZGnHw61g51I98DyOHvVvDYiVMUuEEkrsFtbzA74OHZi4jwgdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('0991c34df72373c5171f4fc73b5a935a')



# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
   # message = TextSendMessage(text=event.message.text)
    #line_bot_api.reply_message(event.reply_token, message)
    print(event)
    text=event.message.text

    if (text=="Hi"):
        reply_text = "Hello"
        #Your user ID
    elif(text=="test"):
        reply_text=detect_text('ocr_test_x1','card.jpg')
    elif(text=="你好"):
        reply_text = "哈囉"
    elif(text=="哈哈"):
        reply_text = "數學"
    elif(text=="影片"):
        original_content_url='https://www.youtube.com/watch?v=apBd2IApksI&list=RDapBd2IApksI&start_radio=1'
        reply_text = original_content_url
    else:
        reply_text = text
#如果非以上的選項，就會學你說話
        

    message = TextSendMessage(reply_text)
    line_bot_api.reply_message(event.reply_token, message)
    #v_message = VideoSendMessage(
     #       original_content_url='https://www.youtube.com/watch?v=apBd2IApksI&list=RDapBd2IApksI&start_radio=1')
    #line_bot_api.reply_message(event.reply_token, message,v_message)
    
def detect_text(bucket, filename):
    print('Looking for text in image {}'.format(filename))

    futures = []

    text_detection_response = vision_client.text_detection({
        'source': {'image_uri': 'gs://{}/{}'.format(bucket, filename)}
    })
    annotations = text_detection_response.text_annotations
    if len(annotations) > 0:
        text = annotations[0].description
    else:
        text = ''
    text2 = text

    return text


def detect_text_local(path):
    """Detects text in the file."""
    #from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    
    image = vision.types.Image(content=content)
    
    response =client.text_detection(image=image)
    texts = response.text_annotations
    annotations = response.text_annotations
    if len(annotations) > 0:
        text = annotations[0].description
    else:
        text = ''
    return text
    
    #return text
@handler.add(MessageEvent, message=(ImageMessage))
def handle_content_message(event):
    
    ext = 'jpg'
    message_content = line_bot_api.get_message_content(event.message.id)

    #message = TextSendMessage(text="ok")
    #line_bot_api.reply_message(event.reply_token, message)    
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-',delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name
    #message = TextSendMessage(text="ok")
    #line_bot_api.reply_message(event.reply_token, message)  
    dist_path = tempfile_path + '.' + ext
    dist_name = os.path.basename(dist_path)
    os.rename(tempfile_path, dist_path)
    path = os.path.join('static', 'tmp', dist_name)
    #line_bot_api.reply_message(event.reply_token, message)
    
    message2 = detect_text_local(path)
    message = TextSendMessage(text=message2)
    line_bot_api.reply_message(event.reply_token, message)

def detect_write_local(path):
    client = vision.ImageAnnotatorClient()
    with io.open(path, 'rb') as image_file:
        content= image_file.read()
        
    image = vision.types.Image(content=content)
    
    response = client.document_text_detection(image=image)
    texts = response.document_text_annotations
    annotations = response.document_text_annotations
    if len(annotations) > 0:
        text = annotations[0].description
    else:
        text = ''
    return text

  
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)