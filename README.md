# cantera-chatbot

> Facebook chatbot on Heroku server using Miniconda3 and Cantera-2.4

[m.me/cantera.chatbot](m.me/cantera.chatbot)

Send a message to calculate adiabatic flame temperature.
"/aft 300 101.325 10 0.5"
will calculate flame temperature at 300K temperature, 101.325kPa pressure, with 10kg/s of air and 0.5kg/s of fuel (Jet-A, kerosene).

![sample](https://github.com/shaunkim/cantera-chatbot/blob/master/webapp/img/aft_sample.jpg "sample")

## Reference
- Miniconda3 Dockerfile
  - https://hub.docker.com/r/frolvlad/alpine-miniconda3/
- Building a chatbot
  - https://korchris.github.io/2017/06/29/FB_chatbot/
- Jet-A (kerosene) chemical mechanism
  - https://web.stanford.edu/group/haiwanglab/HyChem/pages/download.html
