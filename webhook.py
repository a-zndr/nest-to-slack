import hashlib
import json
import os
import requests
import time

#declare variables
#set slack webhook endpoint
webhook_url = 'https://hooks.slack.com/services/0000000000' #replace with your webhook url
#set door variables based on email parse, add as many doors here as needed, may need to be updated to handle more than two doors
if input_data.get('body') and 'FRONT LOBBY' in input_data['body']:
    #lobby nest
    door_uid, door_name = '00000000', 'Lobby Door'
else:
    #server room nest
    door_uid, door_name = '000000000', 'Server Room'
print(door_uid, door_name) #for logs

#set nest api endpoint for the right camera
url = "https://developer-api.nest.com/devices/cameras/{}/last_event/animated_image_url".format(door_uid)
print(url) #for logs
#set nest developer authorization token for HackerOne
token = "000000000000" # Update with your token

#delay 30 seconds cause nest is slow
#time.sleep(30)

# set get request to nest API
headers = {'Authorization': 'Bearer {0}'.format(token), 'Content-Type': 'application/json'} # Update with your token

initial_response = requests.get(url, headers=headers, allow_redirects=False)
if initial_response.status_code == 307:
    initial_response = requests.get(initial_response.headers['Location'], headers=headers, allow_redirects=False)
print(initial_response.text[1:-1])

gif_url= initial_response.text[1:-1] #set url for animated image response from nest

#build slack webhook


slack_data = {
    "attachments": [
        {
            "fallback": "Required plain-text summary of the attachment.",
            "color": "#EC1075",
            "title": "SFO3 {}".format(door_name),
            "title_link": "",
            "text": "{} Who Done It?".format(input_data['subject']),
            "image_url":"{}".format(gif_url),

        }
    ]
}
print(slack_data)
response = requests.post(
    webhook_url, data=json.dumps(slack_data),
    headers={'Content-Type': 'application/json'}
)
if response.status_code != 200:
    raise ValueError(
        'Request to slack returned an error %s, the response is:\n%s'
        % (response.status_code, response.text)
    )
