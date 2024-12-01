import time
import asyncio
from telethon import TelegramClient, events
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from collections import defaultdict

# Telegram API credentials
api_id = '27353904'  # Replace with your API ID
api_hash = '99b31ff29dc195f52e7bb6b526b2e4ca'  # Replace with your API Hash

# Source and destination chats
source_chats = [
    -1001859547091,  # Replace with your first source group ID
    -1002238563306   # Replace with your second source group ID
]

destination_chats = [
    "@JAATXONWER",
    "@bgmi_dva",
    "@RESELLER_COMMUNITY2",
    "@XeonChatGroup",
    "@dsstorechatgroup",
    "@ROLEXRESELLINGHUB",
    "@pubg_chat_group",
    "@SUFIYANxRESELLER",
    "@KRISHNAXRESELLING",
    "@rudraxchats",
    "@RARE_BGMI_STORE_CHAT",
    "@flexopresellinghub",
    "@ResellersChatBGMI",
    "@buying_and_selling_market",
    "@BGMI_Official_Chat_Group",
    "@CLASH_OF_CLANS60",
    "@bgmi_popularity_exchange23",
    "@RESELLER_COMMUNITY4",
    "@RITESHxRESELLING",
    "@ANTHONYBGMICHAT",
    "@RESELLERS_CHAT_GROUP",
    "@indianotphub",
    "@AIMGODRESELLINGHUB",
    "@OGxRESELLERSS",
    "@BGMIRESELLERSGROUP",
    "@VANSHIGCCCHAT",
    "@RAKURAICHATGROUP1",
    "@SANKYCHATGROUP",
    "@BGMlCHATGROUP",
    "@BGMIRESELLERSCOMMUNITY",
    "@CHAT_KING01",
    "@FRAGGER_RESELLING",
    "@MR_LUCKY_CTAT",
    "@KARMARESELLINGCOMMUNITY",
    "@Resellers_Group",
    "@KINGRESELLER",
    "@RESSELERGANG",
    "@ALPHASTORE20",
    "@WAR_RESELLER",
    "@MADARAxCHAT",
    "@QAZI_CHAT_GROUP",
    "@PUBGMANYA_CHAT",
    "@RDXBGMICHATGROUP",
    "@groupresell",
    "@yagami_chatzone",
    "@REALKRISHNAxESCROW",
    "@ScammerHellGroup",
    "@DIAMONDXSENORESEELER",
    "@BGMIRESELLING_GROUP",
    "@BEXXICHATS",
    "@Mr_C4RLO_GC",
    "@BEASTRESELLERGROUP",
    "@TITANIUM_BGMISTORE",
    "@NIHARCHATS",
    "@luciferytdiscussiongroup",
    "@TGEDITION",
    "@Crazy_reselleer",
    "@VIPRESELLERGROUP",
    "@LGDSxSTORExGROUP",
    "@Liger_Reseller",
    "@BGMIACCOUNTANDPOP",
    "@MARK_RESELLER_7",
    "@ARNAVOFFICIALGROUP",
    "@GAURAVSELLOP",
    "@BGMICHATHUB",
    "@bgmi_hacks_for_main_id",
    "@for_sell_hi",
    "@Bgmiresellercommunityop",
    "@Axeyys_chats",
    "@Devil_Gaming_Store",
    "@JayaResellingHub",
    "@micheal00790",
    "@BGMI_ResellerXCommunity1",
    "@BGMI_UCAccounts_STORE",
    "@CHATKROBSDK",
    "@DangerChatGroup",
    "@BgmiPopularityMarket3",
    "@bgmipopexchange01",
    "@resellerscommunityandbgmihub",
    "@RESSING",
    "@BGMIMANIA",
    # Add the rest of your destination chats
]

# Telegram Client
client = TelegramClient('session_name', api_id, api_hash)

# Album tracking
albums = defaultdict(list)

# Simple HTTP server for Render health check
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

def run_http_server():
    server = HTTPServer(('0.0.0.0', 8080), SimpleHandler)
    print("HTTP server running on port 8080...")
    server.serve_forever()

# Function to handle album forwarding
async def handle_album(event):
    grouped_id = event.message.grouped_id
    if grouped_id:
        # Collect all messages with the same grouped_id
        albums[grouped_id].append(event.message)

        # Wait briefly to ensure all parts of the album are collected
        await asyncio.sleep(2)  # Adjust delay if albums are incomplete

        # Check if the album is complete
        if len(albums[grouped_id]) > 1:  # Confirm it's an actual album
            messages = albums.pop(grouped_id)
            for chat in destination_chats:
                try:
                    for message in messages:
                        # Forward individual media messages to preserve attribution
                        await client.forward_messages(chat, message, from_peer=event.message.peer_id)
                    print(f"Album forwarded to {chat}")
                except Exception as e:
                    print(f"Failed to forward album to {chat}: {e}")
        else:
            # If album is incomplete, forward as individual messages
            for chat in destination_chats:
                for message in albums[grouped_id]:
                    try:
                        # Forward individual message with the "forwarded from" attribution
                        await client.forward_messages(chat, message, from_peer=event.message.peer_id)
                        print(f"Message forwarded to {chat}")
                    except Exception as e:
                        print(f"Failed to forward message to {chat}: {e}")
    else:
        # If not an album, forward normally
        for chat in destination_chats:
            try:
                # Forward individual message with the "forwarded from" attribution
                await client.forward_messages(chat, event.message, from_peer=event.message.peer_id)
                print(f"Message forwarded to {chat}")
            except Exception as e:
                print(f"Failed to forward message to {chat}: {e}")

# Forward messages from source chats to destination chats
@client.on(events.NewMessage(chats=source_chats))
async def forward_message(event):
    await handle_album(event)

# Run the Telegram client
def run_telethon():
    with client:
        print("Listening for new messages...")
        client.run_until_disconnected()

if __name__ == "__main__":
    # Start the HTTP server in a separate thread
    http_thread = Thread(target=run_http_server, daemon=True)
    http_thread.start()

    # Start the Telegram client
    run_telethon()
