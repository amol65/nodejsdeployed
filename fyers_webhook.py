from flask import *
import requests
app = Flask(__name__)

import requests
def telegram_bot_sendtext(bot_message):
    
    bot_token = '5700167747:AAEcLoVrOhpN0lrBwv-3Yo2ylglNGcbCWOY'
    bot_chatID = '694240190'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + \
                '&parse_mode=HTML&text=' + bot_message

    return requests.get(send_text)


@app.route('/fyers',methods=['GET', 'POST'])
def fyers():
    if request.content_type == 'application/json' :
        json_data = request.json
        message = json.dumps(json_data) 
        if message is not None : 
            telegram_bot_sendtext(message)
            return 'Done'
   
    return "Unable to read Message"

@app.route('/',methods=['GET', 'POST'])
def home():
    return 'All is well'



if __name__ == "__main__":
    app.run(debug=True)