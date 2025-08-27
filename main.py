from gmail_sender import send_html 
import configparser
config = configparser.ConfigParser()
config_file = 'config.ini'
config.read(config_file)
sa_key_file = config['gmail']['sa_key_file']
sender = config['gmail']['sender']

send_html(
    "minhlong2002@gmail.com", "Test", "<b>Hello from Gmail API</b>",
    sa_key_file, sender_email=sender
)

