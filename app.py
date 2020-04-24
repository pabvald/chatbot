import os
import telegram
import spacy 
import flask_monitoringdashboard as monitoring

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

global bot
global URL
global TOKEN 
global db
global nlp


app = Flask(__name__)
load_dotenv()
app.config.from_object(os.getenv('APP_SETTINGS'))
TOKEN = os.getenv('BOT_TOKEN')
URL = os.getenv('URL')
bot = telegram.Bot(token=TOKEN)
db = SQLAlchemy(app)
nlp = {
    'en': spacy.load("spacy_models/en", disable=["ner", "parser"]),
    'es': spacy.load("spacy_models/es", disable=["ner", "parser"])
}

from logs.functions import init_log
from brain.mastermind import MasterMind


init_log(app)
if app.config['MONITORING']:
    monitoring.config.init_from(file=os.getenv("MONITORING_SETTINGS"))
    monitoring.bind(app)


@app.route('/')
def index():
    """ Does nothing """
    return ""


@app.route('/webhooktelegram', methods=['GET', 'POST'])
def set_webhook_telegram():
    """ Sets up the bot's webhook """
    success = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if success:
        response = "webhook setup ok \n"
    else:
        response = "webhook setup failed \n"
    return jsonify({"message": response})


@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond_telegram():
    """ Handles the incoming messages and provides a response """
    
    try:
        # Get the msg in JSON and convert it into a Telegram obj.
        update = telegram.Update.de_json(request.get_json(force=True), bot)

        # Extract message's fields: user, chat_id, msg_id, text, entities
        chat_id = update.effective_message.chat_id
        msg_id = update.effective_message.message_id
        text = update.effective_message.text
        entities = update.effective_message.parse_entities()
        user = update.effective_message.from_user

        # Telegram entities (including commands) are ignored 
        for ent in entities.values():
            text = text.replace(str(ent), '')

        # Process only text messages
        if user and text:
            text = text.encode('utf-8').decode()
            # Create an MasterMind instance
            mastermind = MasterMind.from_telegram_msg(user, text)

            # Send 'TYPING' action
            bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)

            # Process the msg, get the corresponding response(s)
            telegram_responses = mastermind.get_response_for_telegram()

            # Send the response(s)
            for r in telegram_responses:
                bot.sendMessage(chat_id=chat_id, **r)
        else:
            app.logger.warning("Unsupported Telegram message type")

    except Exception as e:       
        app.logger.error(str(e))
        response = "There was an internal error. Please, try again later"
        bot.sendMessage(chat_id=chat_id, text=response)

    finally:
        return jsonify({"message": "updated"})


if __name__ == '__main__':
    # Run app allowing more than one thread
    app.run(threaded=True)