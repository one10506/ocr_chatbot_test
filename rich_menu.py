# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 14:18:05 2019

@author: user
"""

import requests
import json

headers = {"Authorization":"Bearer KH38RTHaoQRq05iJ2t9aWN+M9pC26tC5SWEtmTREYWlEvTcQEb9eI/WUH/I+AUImrOdxtIyiEOW485A/8gr08gvAzvbE/qdFFaiWLW0ZGnHw61g51I98DyOHvVvDYiVMUuEEkrsFtbzA74OHZi4jwgdB04t89/1O/w1cDnyilFU=","Content-Type":"application/json"}

body = {
    "size": {"width": 2500, "height": 1686},
    "selected": "true",
    "name": "Controller",
    "chatBarText": "Controller",
    "areas":[
        {
          "bounds": {"x": 551, "y": 325, "width": 321, "height": 321},
          "action": {"type": "message", "text": "up"}
        },
        {
          "bounds": {"x": 876, "y": 651, "width": 321, "height": 321},
          "action": {"type": "message", "text": "right"}
        },
        {
          "bounds": {"x": 551, "y": 972, "width": 321, "height": 321},
          "action": {"type": "message", "text": "down"}
        },
        {
          "bounds": {"x": 225, "y": 651, "width": 321, "height": 321},
          "action": {"type": "message", "text": "left"}
        },
        {
          "bounds": {"x": 1433, "y": 657, "width": 367, "height": 367},
          "action": {"type": "message", "text": "btn b"}
        },
        {
          "bounds": {"x": 1907, "y": 657, "width": 367, "height": 367},
          "action": {"type": "message", "text": "btn a"}
        }
    ]
  }

req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu', 
                       headers=headers,data=json.dumps(body).encode('utf-8'))

print(req.text)