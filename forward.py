from telethon import TelegramClient, events, Button
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser, PeerChannel, InputPeerChat, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
import os
import sys
import csv
import traceback
import time
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Telegram API credentials
api_id = '27353904'
api_hash = '99b31ff29dc195f52e7bb6b526b2e4ca'
phone = '+919103804557'

# Source chat ID
source_chat_id = -1002210572103

# List of target channel usernames (you can add more usernames)
target_channel_usernames = ['gyyfj7'] 

# Create a Telegram client
client = TelegramClient('anon', api_id, api_hash)

# Global variable to store the last message ID
last_message_id = 0

# Backoff strategy parameters
backoff_delay = 2  # Initial backoff delay in seconds
max_backoff_delay = 30  # Maximum backoff delay in seconds

# Create an input peer for the source chat
source_chat_peer = InputPeerChannel(source_chat_id, 0) 

@client.on(events.NewMessage)
async def handler(event):
    global last_message_id
    try:
        if event.message.id > last_message_id and event.chat_id == source_chat_peer.channel_id: 
            try:
                # Get the source chat entity
                source_chat = await client.get_entity(event.message.peer_id)
            
                # Forward to each target channel
                for target_username in target_channel_usernames:
                    try:
                        # Get the target channel entity
                        target_channel = await client.get_input_entity(target_username)

                        # Forward the message
                        await client.forward_messages(
                            entity=target_channel,
                            messages=event.message,
                            from_peer=source_chat
                        )
                        logger.info(f"Message forwarded to {target_username}")
                        last_message_id = event.message.id  # Update last_message_id AFTER success
                        backoff_delay = 2  # Reset backoff delay on success
                    except PeerFloodError:
                        logger.warning(f"Getting Flood Error from {target_username}. \nWaiting {backoff_delay} seconds.")
                        time.sleep(backoff_delay)
                        backoff_delay *= 2  # Increase backoff delay
                        if backoff_delay > max_backoff_delay:
                            backoff_delay = max_backoff_delay
                    except UserPrivacyRestrictedError:
                        logger.info(f"The user's privacy settings do not allow you to do this. Skipping.")
                    except Exception as e:
                        logger.error(f'Error forwarding message to {target_username}: {e}')
                        traceback.print_exc()
            except Exception as e:
                logger.error(f'Error getting source chat entity or forwarding message: {e}')
                traceback.print_exc()

    except AttributeError:
        # Suppress the error (Don't print it to the terminal)
        logger.debug("Encountered AttributeError: 'UpdateNewChannelMessage' object has no attribute 'chat_id'")
        pass  # Skip to the next message

    # Add a delay to prevent rate limiting
    time.sleep(1)

async def main():
    # Connect to the Telegram client
    await client.connect()
    if not await client.is_user_authorized():  # Await the result of is_user_authorized
        await client.send_code_request(phone)
        await client.sign_in(phone, input('Enter the code: ')) # Await the result of sign_in

    # Start the handler to listen for new messages
    client.add_event_handler(handler)
    logger.info('Listening for new messages in the source chat.')

    # Define a port and start the server
    port = int(os.environ.get("PORT", 5000))  # Get port from environment (default: 5000)
    logger.info(f"Server started on port {port}")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
