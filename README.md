# cantera-chatbot

> Facebook chatbot on Heroku server using Miniconda3 and Cantera-2.5

[m.me/cantera.chatbot](m.me/cantera.chatbot)

Send a message to calculate adiabatic flame temperature.
"/aft 300 101.325 10 0.5"
will calculate flame temperature at 300K temperature, 101.325kPa pressure, with 10kg/s of air and 0.5kg/s of fuel (Jet-A, kerosene).

![sample](https://github.com/shaunkim/cantera-chatbot/blob/master/webapp/img/aft_sample.jpg "sample")

## Available functions
- **/jeta** : Jet A (A2, POSF10325)
- **/jp8** : JP-8 (A1, POSF10264)
- **/jp10** : JP-10 
- **/methane** : CH4 (using GRI-Mech 3.0)
- **/ethylene** : C2H4
- **/hydrogen** : H2
- **/syngas** : Choose up to 3 species with mole fraction
- **/yplus** : Y+ wall distance calculator like [https://www.cfd-online.com/Tools/yplus.php](https://www.cfd-online.com/Tools/yplus.php)

## Build your own chatbot
- Requirement
  - Heroku CLI tool: https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli
  - Docker account
  - Heroku server
  - ~~Facebook~~ Meta Developer tools: https://developers.facebook.com/tools/

- Clone this repository
```
$ git clone https://github.com/shaunkim/cantera-chatbot.git
```
- Update webapp/main.py with your credentials
- After logging into Heroku and Docker, run the following to push and release the app.
```
$ heroku container:push web
$ heroku container:release web
```
- Check if your heroku server is alive. Should display "hello from cantera-chatbot feat. NumPy1.18.5 and Cantera 2.5.1" like [cantera-chatbot-01.herokuapp.com](cantera-chatbot-01.herokuapp.com)
- Submit an app review on Meta Developer Tools to allow chatbot to message other people

## Reference
- Miniconda3 Dockerfile
  - https://hub.docker.com/r/frolvlad/alpine-miniconda3/
- Building a chatbot
  - https://korchris.github.io/2017/06/29/FB_chatbot/
- Jet-A (kerosene), JP-10 chemical mechanism
  - https://web.stanford.edu/group/haiwanglab/HyChem/pages/download.html
