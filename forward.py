from telethon import TelegramClient, events, Button
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser, PeerChannel, InputPeerChat
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
import traceback
import time
from flask import Flask
import threading

# Telegram API credentials
api_id = 27353904
api_hash = '99b31ff29dc195f52e7bb6b526b2e4ca'
phone = '+919103804557'

# Source chat ID and target channels
source_chat_id = -1002210572103
target_channel_usernames = ['gyyfj7']  # Add more usernames as needed

# Logging file
log_file = "logs.txt"

# Create a Telegram client
client = TelegramClient('anon', api_id, api_hash)

# Global variable to store the last message ID
last_message_id = 0

# Backoff strategy parameters
backoff_delay = 2  # Initial backoff delay in seconds
max_backoff_delay = 30  # Maximum backoff delay in seconds

# Flask app for Render to keep the bot alive
app = Flask(__name__)

@app.route('/')
def index():
    return "Telegram Bot is Running"

def run_flask():
    app.run(host="0.0.0.0", port=5000)

@client.on(events.NewMessage)
async def handler(event):
    global last_message_id
    if event.message.id > last_message_id and event.chat_id == source_chat_id: 
        try:
            # Get the source chat entity
            source_chat = await client.get_entity(event.message.peer_id)
            
            # Forward to each target channel
            for target_username in target_channel_usernames:
                try:
                    # Get the target channel entity
                    target_channel = await client.get_input_entity(target_username.strip())

                    # Forward the message
                    await client.forward_messages(
                        entity=target_channel,
                        messages=event.message,
                        from_peer=source_chat
                    )
                    print(f"Message forwarded to {target_username}")
                    last_message_id = event.message.id  # Update last_message_id AFTER success
                    backoff_delay = 2  # Reset backoff delay on success
                except PeerFloodError:
                    print(f"Getting Flood Error from {target_username}. \nWaiting {backoff_delay} seconds.")
                    time.sleep(backoff_delay)
                    backoff_delay = min(backoff_delay * 2, max_backoff_delay)
                except UserPrivacyRestrictedError:
                    print(f"The user's privacy settings do not allow you to do this. Skipping.")
                except Exception as e:
                    traceback.print_exc()
                    print(f'Error forwarding message to {target_username}: {e}')
        except Exception as e:
            traceback.print_exc()
            print(f'Error getting source chat entity or forwarding message: {e}')

    # Add a delay to prevent rate limiting
    time.sleep(1)

async def main():
    # Connect to the Telegram client
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        await client.sign_in(phone, input('Enter the code: '))

    # Start the handler to listen for new messages
    client.add_event_handler(handler)
    print('Listening for new messages in the source chat.')

    # Run the client until the user stops it
    await client.run_until_disconnected()

# Start the Telegram bot and Flask server
if __name__ == '__main__':
    try:
        threading.Thread(target=run_flask).start()  # Start Flask server in a separate thread
        client.loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Exiting.")
