from telethon import TelegramClient, events
from http.server import BaseHTTPRequestHandler, HTTPServer

# Telegram API credentials
api_id = '27353904'  # Replace with your API ID
api_hash = '99b31ff29dc195f52e7bb6b526b2e4ca'  # Replace with your API Hash

# Source channel/group IDs
source_chats = [-1001859547091, -1002238563306]  # Add the new source chat ID here

# New list of destination groups/chats
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
    "@BGMIMANIA"
]

# Create the Telegram client
client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage(chats=source_chats))
async def forward_message(event):
    for chat in destination_chats:
        try:
            # Forward the message with "forwarded from" attribution
            await client.forward_messages(chat, event.message)
            print(f"Message forwarded to {chat}")
        except Exception as e:
            print(f"Failed to forward message to {chat}: {e}")

# HTTP server to keep the bot alive on Render
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

def run_http_server():
    server = HTTPServer(('0.0.0.0', 8080), SimpleHandler)
    print("HTTP server running on port 8080...")
    server.serve_forever()

# Run the HTTP server in a separate thread
import threading
http_thread = threading.Thread(target=run_http_server)
http_thread.daemon = True
http_thread.start()

# Start the Telegram client
with client:
    print("Listening for new messages...")
    client.run_until_disconnected()
