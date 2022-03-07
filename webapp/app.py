from flask import Flask, request, jsonify
import requests
import numpy as np

import cantera as ct #cantera.chatbot🔥🤳

ct.suppress_thermo_warnings()
import matplotlib.pyplot as plt


def convert(value):
    try:
        return float(value)
    except ValueError:
        return value

app = Flask(__name__)
FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages'
VERIFY_TOKEN='your password'
PAGE_ACCESS_TOKEN='your page access token'

# Available functions 2020.11.24
avail_fs = 'Available functions : ' + '\n' \
'/jeta : Adiabatic flame temperature (Jet-A)' + '\n' \
'/jp8 : Adiabatic flame temperature (JP-8)' + '\n' \
'/jp10 : Adiabatic flame temperature (JP-10)' + '\n' \
'/methane : Adiabatic flame temperature (CH4)' + '\n' \
'/ethylene : Adiabatic flame temperature (C2H4)' + '\n' \
'/hydrogen : Adiabatic flame temperature (H2)' + '\n' \
'/syngas : Adiabatic flame temperature (3 fuels)' + '\n' \
'/yplus : Y+ wall distance estimation'

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
    if ('/tpaf' in message.lower()):
        return "TPAF [K], [kPa], [kg/s], [kg/s]"

    # Adiabatic flame temperature
    # /aft Temperature Pressure  W_air W_fuel [K, kPa, kg/s, kg/s]
    elif ('/aft' in message.lower()):
        try:
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
        except:
            err_message = 'Something is wrong. Type "/help" for help.'
            return err_message

    # Adiabatic flame temperature (Jet-A)
    elif ('/jeta' in message.lower()):
        try:
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
                T4_message = 'Jet-A flame temperature: ' + str.format('{0:.4f}',T4) + ' [K]' \
                            +'\n'+ '\n'+ \
                            'T[K], P[kPa], Wa[kg/s], Wf[kg/s]' +'\n'+ \
                            str(tpaf[:4])
                return T4_message

            else:
                help_message = 'Type "/jeta T P W_air W_fuel" in [K, kPa, kg/s, kg/s] to calculate adiabatic flame temperature.' +'\n'+'\n'+ \
                               'For example, "/jeta 300 101.325 14.7 1"'
                return help_message
        except:
            err_message = 'Something is wrong. Type "/jeta" for help.'
            return err_message

    # Adiabatic flame temperature (JP-8)
    elif ('/jp8' in message.lower()):
        try:
            data= message.split()
            # Default Jet-A
            if (len(data)==5 and type(convert(data[1]))==float \
                             and type(convert(data[2]))==float \
                             and type(convert(data[3]))==float \
                             and type(convert(data[4]))==float):

                tpaf = list(map(float, data[1:]))

                #Mech

                gas = ct.Solution('mech/A1highT.cti')
                Yo2 = 0.233*tpaf[2]
                Yn2 = 0.767*tpaf[2]
                Yfuel= tpaf[3]
                Ystring="POSF10264:" + str(Yfuel) +', O2:'+ str(Yo2) +', N2:'+ str(Yn2) +""

                gas.TPY = tpaf[0], tpaf[1]*1000, Ystring
                gas.equilibrate("HP")

                T4 = gas.T
                T4_message = 'JP8 flame temperature: ' + str.format('{0:.4f}',T4) + ' [K]' \
                            +'\n'+ '\n'+ \
                            'T[K], P[kPa], Wa[kg/s], Wf[kg/s]' +'\n'+ \
                            str(tpaf[:4])
                return T4_message

            else:
                help_message = 'Type "/jp8 T P W_air W_fuel" in [K, kPa, kg/s, kg/s] to calculate adiabatic flame temperature.' +'\n'+'\n'+ \
                               'For example, "/jp8 300 101.325 14.7 1"'
                return help_message
        except:
            err_message = 'Something is wrong. Type "/jp8" for help.'
            return err_message


    # Adiabatic flame temperature (JP-8)
    elif ('/jp10' in message.lower()):
        try:
            data= message.split()
            # Default Jet-A
            if (len(data)==5 and type(convert(data[1]))==float \
                             and type(convert(data[2]))==float \
                             and type(convert(data[3]))==float \
                             and type(convert(data[4]))==float):

                tpaf = list(map(float, data[1:]))

                #Mech

                gas = ct.Solution('mech/JP10highT.cti')
                Yo2 = 0.233*tpaf[2]
                Yn2 = 0.767*tpaf[2]
                Yfuel= tpaf[3]
                Ystring="C10H16:" + str(Yfuel) +', O2:'+ str(Yo2) +', N2:'+ str(Yn2) +""

                gas.TPY = tpaf[0], tpaf[1]*1000, Ystring
                gas.equilibrate("HP")

                T4 = gas.T
                T4_message = 'JP10 flame temperature: ' + str.format('{0:.4f}',T4) + ' [K]' \
                            +'\n'+ '\n'+ \
                            'T[K], P[kPa], Wa[kg/s], Wf[kg/s]' +'\n'+ \
                            str(tpaf[:4])
                return T4_message

            else:
                help_message = 'Type "/jp8 T P W_air W_fuel" in [K, kPa, kg/s, kg/s] to calculate adiabatic flame temperature.' +'\n'+'\n'+ \
                               'For example, "/jp10 300 101.325 14.7 1"'
                return help_message
        except:
            err_message = 'Something is wrong. Type "/jp8" for help.'
            return err_message


    # Adiabatic flame temperature using GRI 3.0
    # CH4 as fuel, for now.
    elif ('/methane' in message.lower()):
        try:
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
                T4_message = 'CH4 flame temperature: ' + str.format('{0:.4f}',T4) + ' [K]' \
                            +'\n'+ '\n'+ \
                            'T[K], P[kPa], Wa[kg/s], Wf[kg/s]' +'\n'+ \
                            str(tpaf[:4])
                return T4_message

            else:
                help_message = 'Type "/methane T P W_air W_fuel" in [K, kPa, kg/s, kg/s] to calculate adiabatic flame temperature.' +'\n'+'\n'+ \
                               'For example, "/methane 300 101.325 17.2 1"' +'\n' \
                               'Based on GRI3.0 and CH4 as fuel'
                return help_message
        except:
            err_message = 'Something is wrong. Type "/methane" for help.'
            return err_message


    elif ('/ethylene' in message.lower()):
        try:
            data= message.split()
            # Default C2H4
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
                Ystring="C2H4:" + str(Yfuel) +', O2:'+ str(Yo2) +', N2:'+ str(Yn2) +""

                gas.TPY = tpaf[0], tpaf[1]*1000, Ystring
                gas.equilibrate("HP")

                T4 = gas.T
                T4_message = 'C2H4 flame temperature: ' + str.format('{0:.4f}',T4) + ' [K]' \
                            +'\n'+ '\n'+ \
                            'T[K], P[kPa], Wa[kg/s], Wf[kg/s]' +'\n'+ \
                            str(tpaf[:4])
                return T4_message

            else:
                help_message = 'Type "/ethylene T P W_air W_fuel" in [K, kPa, kg/s, kg/s] to calculate adiabatic flame temperature.' +'\n'+'\n'+ \
                               'For example, "/ethylene 300 101.325 14.8 1"' +'\n' \
                               'Based on GRI3.0 and C2H4 as fuel'
                return help_message

        except:
            err_message = 'Something is wrong. Type "/ethylene" for help.'
            return err_message

    elif ('/hydrogen' in message):
        try:
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
                Ystring="H2:" + str(Yfuel) +', O2:'+ str(Yo2) +', N2:'+ str(Yn2) +""

                gas.TPY = tpaf[0], tpaf[1]*1000, Ystring
                gas.equilibrate("HP")

                T4 = gas.T
                T4_message = 'H2 flame temperature: ' + str.format('{0:.4f}',T4) + ' [K]' \
                            +'\n'+ '\n'+ \
                            'T[K], P[kPa], Wa[kg/s], Wf[kg/s]' +'\n'+ \
                            str(tpaf[:4])
                return T4_message


            else:
                help_message = 'Type "/hydrogen T P W_air W_fuel" in [K, kPa, kg/s, kg/s] to calculate adiabatic flame temperature.' +'\n'+'\n'+ \
                               'For example, "/hydrogen 300 101.325 34.3 1"' +'\n' \
                               'Based on GRI3.0 and H2 as fuel'
                return help_message
        except:
            err_message = 'Something is wrong. Type "/hydrogen" for help.'
            return err_message

    # Adiabatic flame temperature using GRI 3.0
    # Fuel string as input
    # /syngas h2 co ch4 0.5 0.10 0.85 300.0 101.325 14.7 1
    # data[i] 1  2  3   4    5   6    7     8       9    10
    elif ('/syngas' in message):
        try:
            data= message.split()
            # Default C
            if (len(data)==11 and type(data[1])==str \
                             and type(data[2])==str \
                             and type(data[3])==str \
                             and type(convert(data[4]))==float \
                             and type(convert(data[5]))==float \
                             and type(convert(data[6]))==float \
                             and type(convert(data[7]))==float \
                             and type(convert(data[8]))==float \
                             and type(convert(data[9]))==float \
                             and type(convert(data[10]))==float):

                tpaf = list(map(float, data[7:]))



                #GRI-3.0 Mech
                gas = ct.Solution('gri30.cti')
                Xo2 = 0.21*tpaf[2]
                Xn2 = 0.79*tpaf[2]

                fuel_string = data[1].upper()+":" + str(convert(data[4])*tpaf[3])+", " + data[2].upper()+":"  + str(convert(data[5])*tpaf[3])+ ", "+ data[3].upper()+ " :" + str(convert(data[6])*tpaf[3])
                Xstring="O2:"+ str(Xo2) +", N2:"+ str(Xn2) + ", "+ fuel_string

                gas.TPX = tpaf[0], tpaf[1]*1000., Xstring
                gas.equilibrate("HP")
                Eqv = gas.equivalence_ratio()

                T4 = gas.T
                T4_message = 'Syngas flame temperature: ' + str.format('{0:.4f}',T4) + ' [K]' \
                            +'\n'+ '\n'+ \
                            'T[K], P[kPa], Wa[kg/s], Wf[kg/s]' +'\n'+ \
                            str(tpaf[:4])+'\n' + \
                            'Fuel composition :' + '\n' +\
                            fuel_string + '\n' + \
                            'Eqv Ratio: {0:1.4f}'.format(Eqv)
                return T4_message

            else:
                help_message = 'Type "/syngas h2 co ch4 Xh2 Xco Xch4 T P W_air W_fuel" in [K, kPa, kg/s, kg/s] to calculate adiabatic flame temperature.' +'\n'+'\n'+ \
                               'For example, "/syngas h2 co ch4 0.05 0.1 0.85  300 101.325 17.2 1"' +'\n' \
                               'Based on GRI3.0'
                return help_message
        except:
            err_message = 'Something is wrong. Type "/syngas" for help.'
            return err_message





    #y plus estimation
    #https://www.cfd-online.com/Wiki/Y_plus_wall_distance_estimation
    elif ('/yplus' in message):
        data= message.split()
        # Default CH4
        if (len(data)==5 and type(convert(data[1]))==float \
                         and type(convert(data[2]))==float \
                         and type(convert(data[3]))==float \
                         and type(convert(data[4]))==float):

            uRhoMuL = list(map(float, data[1:]))
            U =   uRhoMuL[0]   # velocity m/s
            rho = uRhoMuL[1]   # density  kg/m3
            mu =  uRhoMuL[2]   # dynamic viscosity kg/ms
            L  =  uRhoMuL[3]   # boundary layer length m

            Re = rho*U*L/mu
            if Re>1e9:
                yplus_message= 'Re= '+ str.format('{0:.5E}',Re) +'\n' \
                'y+ calculation is valid for Re<1e9'
                return yplus_message

            else:
                Cf= (2.0*np.log10(Re)-0.65)**(-2.3)
                tw= Cf*0.5*rho*U**2.0
                ustar= (tw/rho)**0.5
                yplus = mu/(rho*ustar)
                yplus_message= 'Re = '+ str.format('{0:.5e}',Re) +'\n' \
                'y+ = ' + str.format('{0:.5e}',yplus) + '[m]'
                return yplus_message
        else:
            help_message = 'Type "/yplus u rho mu L" in [m/s, kg/m3, kg/ms, m] to calculate y+ distance' +'\n'+'\n'+ \
                           'For example, "/yplus 1.0 1.205 1.82e-5 1.0"'
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
        help_message = avail_fs

        return help_message
    # Greeting
    elif ('hi' in message.lower() or 'hello' in message.lower() or
    'hi' in message.lower() or
    'holla' in message.lower() or
    '안녕' in message.lower() or
    'hey' in message.lower()):
        help_message = 'Hi, this is Cantera Chatbot.'+ '\n'+ '\n' \
                       + avail_fs
        return help_message


    else:
        """This is just a dummy function, returning a variation of what
        the user said. Replace this function with one connected to chatbot."""

        return "This is a dummy response to '{}'. Try '/help'".format(message)


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
    +'\n'+ 'NumPy'+ np.__version__ + ' and  Cantera '+ct.__version__
    return hello_message
if __name__ == '__main__':
    app.run(threaded=True, port=5000)
