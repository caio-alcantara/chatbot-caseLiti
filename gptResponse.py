from twilio.rest import Client
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI

# credenciais Twilio 
account_sid = 'ACCOUNT_SID'
auth_token = 'AUTH_TOKEN'
whatsapp_number = 'whatsapp:+14155238886'  # Número do WhatsApp Twilio

# chave de API OpenAI
api_key = 'sk'

twilio_client = Client(account_sid, auth_token)
openai_client = OpenAI(api_key=api_key)

app = Flask(__name__)

# Endpoint para receber mensagens
@app.route('/webhook', methods=['POST'])
def webhook():
    # Recebe a mensagem do usuário no whatsapp
    incoming_msg = request.form.get('Body')
    from_number = request.form.get('From')

    # manda a mensagem do usuário como pergunta para o chat gpt 
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            # Esta primeira linha define a "personalidade" do chat gpt
            {"role": "system", "content": "Você é um assistente que responde perguntas sobre saúde de maneira simplificada e didática para aqueles que estão buscando uma vida mais saudável."},
            {"role": "user", "content": incoming_msg},
        ]
    )
    # Trata a mensagem do chat gpt
    chatgpt_response = response.choices[0].message.content
    # Envia a resposta do chat gpt para o usuário no whatsapp
    reply = MessagingResponse()
    reply.message(chatgpt_response)

    return str(reply)

if __name__ == '__main__':
    app.run()
