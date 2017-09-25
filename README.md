# nest-to-slack
A python script for taking data from nest API and pushing a webhook to slack using zapier

This project was to help associate the emails we were getting through our service providor from our Brivo card system with attribution for peace of mind. We were channeling the emails into slack already, but it was hard not to panic when we saw them. Also giving zapier full slack access or full gmail access was a bit nuts so we stepped back and built some basic webhooks to utilize the Nest API, the slack webhook API, sadly it's been 4 months and Brivo hasn't approved developer access so we can't use that API.

The Zapier workflow consists of

1. New Inbound Email creating an `@zapier` mailbox to send to from our brivo system
2. Filter: Only continue if: only proceeding if 
  `Body Plain, (Text) Contains, door name 1` 
  Or 
  `Body Plain, (Text) Contains, door name 2`
3. two instances of a python code module containing the following code
```
  import time
  time.sleep(9)
```
> Simply put this is to deal with several issues. 1) nest runs about 15-20 seconds behind so calling for the last "incident" actually calls for something far before your incident. Simple problem: delay the zapier call 2) Zapier doesn't have a delay feature that's less than 1 minute AND the delay can get caught up and last longer than 1 minute (in testing had 1, 3, 5, and 4 minute delays from a 1 minute delay module). No problem I'll just add `time.sleep(20)` to the code itself. 3) Zapier times out code after 10.01 seconds which includes the time it takes to load the script, and parse it (which also means `time.sleep(10)` doesn't work. The resulting solution of two added delays works well, leaving the ability to add another delay to fine-tune in the primary payload.

4. The primary python payload should be added, updated with your device ID's, authentication token, and Slack webhook address etc. Examples of the nest codes can be found here: developers.nest.com/documentation/cloud/how-to-read-data
