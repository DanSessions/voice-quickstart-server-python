import os
from flask import Flask, request
from twilio.jwt.access_token import AccessToken, VoiceGrant
from twilio.rest import Client
import twilio.twiml

ACCOUNT_SID = 'AC***'
API_KEY = 'SK***'
API_KEY_SECRET = '***'
ANDROID_PUSH_CREDENTIAL_SID = 'CR***'
IOS_PUSH_CREDENTIAL_SID = 'CR***'

app = Flask(__name__)

# Example: /token?user=39802&platform=android
# Example: /token?user=39802&platform=ios
@app.route('/token')
def token():
  user_id = request.args.get('user')
  
  if not user_id:
    return "Invalid user"

  platform = request.args.get('platform')

  if not platform:
    return "Invalid platform"

  account_sid = os.environ.get("ACCOUNT_SID", ACCOUNT_SID)
  api_key = os.environ.get("API_KEY", API_KEY)
  api_key_secret = os.environ.get("API_KEY_SECRET", API_KEY_SECRET)
  user_identity = 'agent_' + user_id
  
  if platform == 'android':
    push_credential = os.environ.get("ANDROID_PUSH_CREDENTIAL_SID", ANDROID_PUSH_CREDENTIAL_SID)
  else:
    push_credential = os.environ.get("IOS_PUSH_CREDENTIAL_SID", IOS_PUSH_CREDENTIAL_SID)

  grant = VoiceGrant(
    push_credential_sid=push_credential
  )

  token = AccessToken(account_sid, api_key, api_key_secret, user_identity)
  token.add_grant(grant)

  return str(token)

@app.route('/', methods=['GET', 'POST'])
def welcome():
  resp = twilio.twiml.Response()
  resp.say("Welcome to Twilio")
  return str(resp)

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
