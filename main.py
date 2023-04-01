"""
Email Tracker API

By ~ Darkmash
"""

from flask import Flask, request , jsonify , send_file
from datetime import datetime, timedelta
import logging
import random
import string

def generate_random_string(length):
	letters = string.ascii_letters
	random_string = ''.join(random.choice(letters) for i in range(length))
	return random_string

def get_time():
  return str(datetime.utcnow())


app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

WORKERS = {}
TOKEN = {}


@app.route('/')
def main_func_():
  print("PING__UPTIME")
  return """
   <meta
      property="og:image"
      content="https://cdn.discordapp.com/attachments/1023460179087470663/1062001193733337158/image.png"
    />
    <meta
      name="description"
      content="An API for email tracking services."
    />
    <meta name="keywords" content="email, tracking ,dark.mail ,darkmash , tools , startup , coders" />
    <link
      rel="icon"
      type="image/png"
      href="https://cdn.discordapp.com/attachments/1023460179087470663/1062001193733337158/image.png"
    />
        <title> Dark.Mail. Email Tracker API ~ Darkmash</title>

  ######## DARKMASH ~ EMail Tracker API ~ V.1.0.0 ###################<br>
  To use the service [GET - method] ,<br>
      /service/get/ - > returns the data from tracking<br> 
            
      With headers ~ <br>
      &nbsp &nbsp token:token by us<br> 

      /service/generate/  - > returns the tracking code and token <br> 

      /service/track/[tracker-code]/ - > returns a one pixel image and logs user info from req <br>
  ##############################################################
  """




@app.route('/service/get/', methods=['GET'])
def get():
  global WORKERS
  try:
    token =  request.headers["token"] 
    return jsonify(WORKERS[token])
  except:
    return "Invalid Token"

@app.route('/service/generate/', methods=['GET'])
def generate():
  global TOKEN
  
  token = generate_random_string(14)
  
  TOKEN[f"{hash(token)}"] = token
  WORKERS[token] = []
  
  return token +"XXXX"+ f'<img src="https://emailtracker.darkmash.repl.co/service/track/{hash(token)}" width="0" height="0">'

@app.route('/service/track/<code>', methods=['GET'])
def track(code):
  global WORKERS, TOKEN
  ip =   request.headers["X-Forwarded-For"]
  user =    request.headers["user-agent"]
  token = TOKEN[code]

  WORKERS[token].append({"time":get_time(),"ip":ip,"user-agent":user})

  return send_file("a.png", mimetype='image/gif')


app.run(host="0.0.0.0", port=8080)
