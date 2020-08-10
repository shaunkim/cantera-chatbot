from flask import Flask, request, jsonify
import requests

import numpy as np
import cantera as ct
ct.suppress_thermo_warnings()

import matplotlib.pyplot as plt

def convert(value):
    try:
        return float(value)
    except ValueError:
        return value

app = Flask(__name__)
FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages'
VERIFY_TOKEN='tlsgus'
PAGE_ACCESS_TOKEN='EAAIWnkVn7twBAJX26aKy9oWYZBK9kIfPDWuOYPs7H1ptlgkXzLEo4mfZB7lgkCyQuaZB7JqujynFUqDfGofqFAnSYHvkXVQOpc5FvZAal5cbpyQjowPN8v7MuaKpq5NZBXcHZAfyZChn8lh4lgicq9vWs7EWzVFSZCkVdeKOtEW0sgZDZD'

def send_message(recipient_id, text):
    """Send a response to Facebook"""
    payload = {
        'message': {
            'text': text
        },
        'recipient': {
            'id': recipient_id
        },
        'notification_type': 'regular'
    }

    auth = {
        'access_token': PAGE_ACCESS_TOKEN
    }

    response = requests.post(
        FB_API_URL,
        params=auth,
        json=payload
    )

    return response.json()

def get_bot_response(message):
    if ('/tpaf' in message):
        return "TPAF [K], [kPa], [kg/s], [kg/s]"

    # Adiabatic flame temperature using GRI 3.0
    # CH4 as fuel, for now.
    elif ('/gri30' in message):
        data= message.split()
        # Default CH4
        if (len(data)==5 and type(convert(data[1]))==float \
                         and type(convert(data[2]))==float \
                         and type(convert(data[3]))==float \
                         and type(convert(data[4]))==float):

            tpaf = list(map(float, data[1:]))

            #GRI-3.0 Mech
            gas = ct.Solution('gri30.cti')
            Yo2 = 0.233*tpaf[2]
            Yn2 = 0.767*tpaf[2]
            Yfuel= tpaf[3]
            Ystring="CH4:" + str(Yfuel) +', O2:'+ str(Yo2) +', N2:'+ str(Yn2) +""

            gas.TPY = tpaf[0], tpaf[1]*1000, Ystring
            gas.equilibrate("HP")

            T4 = gas.T
            T4_message = 'CH4 Adiabatic flame temperature: ' + str.format('{0:.4f}',T4) + ' [K]' \
                        +'\n'+ '\n'+ \
                        'T[K], P[kPa], Wa[kg/s], Wf[kg/s]' +'\n'+ \
                        str(tpaf[:4])
            return T4_message

        else:
            help_message = 'Type "/gri30 T P W_air W_fuel" in [K, kPa, kg/s, kg/s] to calculate adiabatic flame temperature.' +'\n'+'\n'+ \
                           'For example, "/gri30 300 101.325 10 0.5"' +'\n' \
                           'Based on GRI3.0 and CH4 as a fuel'
            return help_message

    # Adiabatic flame temperature
    # /aft Temperature Pressure  W_air W_fuel [K, kPa, kg/s, kg/s]
    elif ('/aft' in message):
        data= message.split()
        # Default Jet-A
        if (len(data)==5 and type(convert(data[1]))==float \
                         and type(convert(data[2]))==float \
                         and type(convert(data[3]))==float \
                         and type(convert(data[4]))==float):

            tpaf = list(map(float, data[1:]))

            #Mech

            gas = ct.Solution('mech/A2highT.cti')
            Yo2 = 0.233*tpaf[2]
            Yn2 = 0.767*tpaf[2]
            Yfuel= tpaf[3]
            Ystring="POSF10325:" + str(Yfuel) +', O2:'+ str(Yo2) +', N2:'+ str(Yn2) +""

            gas.TPY = tpaf[0], tpaf[1]*1000, Ystring
            gas.equilibrate("HP")

            T4 = gas.T
            T4_message = 'Adiabatic flame temperature: ' + str.format('{0:.4f}',T4) + ' [K]' \
                        +'\n'+ '\n'+ \
                        'T[K], P[kPa], Wa[kg/s], Wf[kg/s]' +'\n'+ \
                        str(tpaf[:4])
            return T4_message

        else:
            help_message = 'Type "/aft T P W_air W_fuel" in [K, kPa, kg/s, kg/s] to calculate adiabatic flame temperature.' +'\n'+'\n'+ \
                           'For example, "/aft 300 101.325 10 0.5"'
            return help_message



    # Sample image url
    elif ('/sample' in message.lower()):
        help_message ='https://i.imgur.com/GefZBx3.jpg'  #/sample_aft
        return help_message

    # send plot
    elif ('/test_plot' in message.lower()):
        x = [1,2,3.2]
        y = [1, 1.2, 1.3]
        fig = plt.plot(x,y)
        help_message ='will it plot?'  #/sample_aft
        return help_message



    # Help message
    elif ('help' in message.lower() or 'info' in message.lower() or 'test' in message.lower()):
        help_message = 'Available functions : ' + '\n' \
        '/aft : adiabatic flame temperature (Jet-A)'+ '\n' \
        '/gri30 : adiabatic flame temperature (CH4)'+ '\n' \

        return help_message
    # Greeting
    elif ('hi' in message.lower() or 'hello' in message.lower() or
    'hi' in message.lower() or
    'holla' in message.lower() or
    '안녕' in message.lower() or
    'hey' in message.lower()):
        help_message = 'Hi, this is Cantera Chatbot.'+ '\n' \
                       'Available functions : ' + '\n' \
                       '/aft : Adiabatic flame temperature'
        return help_message


    else:
        """This is just a dummy function, returning a variation of what
        the user said. Replace this function with one connected to chatbot."""

        return "This is a dummy response to '{}'. Try '/aft'".format(message)


def verify_webhook(req):
    if req.args.get("hub.verify_token") == VERIFY_TOKEN:
        return req.args.get("hub.challenge")
    else:
        return "incorrect"

def respond(sender, message):
    """Formulate a response to the user and
    pass it on to a function that sends it."""
    response = get_bot_response(message)
    send_message(sender, response)


def is_user_message(message):
    """Check if the message is a message from the user"""
    return (message.get('message') and
            message['message'].get('text') and
            not message['message'].get("is_echo"))


@app.route("/webhook", methods=['GET'])
def listen():
    """This is the main function flask uses to
    listen at the `/webhook` endpoint"""
    if request.method == 'GET':
        return verify_webhook(request)

@app.route("/webhook", methods=['POST'])
def talk():
    payload = request.get_json()
    event = payload['entry'][0]['messaging']
    for x in event:
        if is_user_message(x):
            text = x['message']['text']
            sender_id = x['sender']['id']
            respond(sender_id, text)

    return "ok"

@app.route('/')
def hello():
    hello_message = 'hello from cantera-chatbot  feat. ' \
    +'\n'+ 'NumPy'+ np.__version__ + 'and  Cantera '+ct.__version__
    return hello_message
if __name__ == '__main__':
    app.run(threaded=True, port=5000)
