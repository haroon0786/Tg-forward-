import time
import asyncio
import logging
from telethon import TelegramClient, events
from flask import Flask
from threading import Thread

# Telegram API credentials
api_id = '27353904'  # Replace with your API ID
api_hash = '99b31ff29dc195f52e7bb6b526b2e4ca'  # Replace with your API Hash

# Source channel/group ID
source_chat = -1001859547091  # Replace with your source group ID

# List of destination groups/chats - Ensure these usernames are valid
destination_chats = [
    "@JAATXONWER", "@bgmi_dva", "@RESELLER_COMMUNITY2", "@XeonChatGroup",
    "@dsstorechatgroup", "@ROLEXRESELLINGHUB", "@pubg_chat_group",
    "@SUFIYANxRESELLER", "@KRISHNAXRESELLING", "@rudraxchats",
    "@RARE_BGMI_STORE_CHAT", "@flexopresellinghub", "@ResellersChatBGMI",
    "@buying_and_selling_market", "@BGMI_Official_Chat_Group", "@CLASH_OF_CLANS60",
    "@bgmi_popularity_exchange23", "@RESELLER_COMMUNITY4", "@RITESHxRESELLING",
    "@ANTHONYBGMICHAT", "@RESELLERS_CHAT_GROUP", "@indianotphub",
    "@AIMGODRESELLINGHUB", "@OGxRESELLERSS", "@BGMIRESELLERSGROUP",
    "@VANSHIGCCCHAT", "@RAKURAICHATGROUP1", "@SANKYCHATGROUP", "@BGMlCHATGROUP",
    "@BGMIRESELLERSCOMMUNITY", "@CHAT_KING01", "@FRAGGER_RESELLING",
    "@MR_LUCKY_CTAT", "@KARMARESELLINGCOMMUNITY", "@Resellers_Group",
    "@KINGRESELLER", "@RESSELERGANG", "@ALPHASTORE20", "@WAR_RESELLER",
    "@MADARAxCHAT", "@QAZI_CHAT_GROUP", "@PUBGMANYA_CHAT", "@RDXBGMICHATGROUP",
    "@groupresell", "@yagami_chatzone", "@REALKRISHNAxESCROW",
    "@ScammerHellGroup", "@DIAMONDXSENORESEELER", "@BGMIRESELLING_GROUP",
    "@BEXXICHATS", "@Mr_C4RLO_GC", "@BEASTRESELLERGROUP", "@TITANIUM_BGMISTORE",
    "@NIHARCHATS", "@luciferytdiscussiongroup", "@TGEDITION", "@Crazy_reselleer",
    "@VIPRESELLERGROUP", "@LGDSxSTORExGROUP", "@Liger_Reseller",
    "@BGMIACCOUNTANDPOP", "@MARK_RESELLER_7", "@ARNAVOFFICIALGROUP",
    "@GAURAVSELLOP", "@BGMICHATHUB", "@bgmi_hacks_for_main_id", "@for_sell_hi",
    "@Bgmiresellercommunityop", "@Axeyys_chats", "@Devil_Gaming_Store",
    "@JayaResellingHub", "@micheal00790", "@BGMI_ResellerXCommunity1",
    "@BGMI_UCAccounts_STORE", "@CHATKROBSDK", "@DangerChatGroup",
    "@BgmiPopularityMarket3", "@bgmipopexchange01", "@resellerscommunityandbgmihub",
    "@RESSING", "@BGMIMANIA"
]

# Create the Telegram client
client = TelegramClient('session_name', api_id, api_hash)

# Flask web server to keep Render happy
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# List to track problematic chats
banned_chats = set()

# Message forwarding logic
@client.on(events.NewMessage(chats=source_chat))
async def forward_message(event):
    for chat in destination_chats:
        if chat in banned_chats:
            logger.info(f"Skipping banned chat: {chat}")
            continue  # Skip banned chats
        try:
            await client.forward_messages(chat, event.message)
            logger.info(f"Message forwarded to {chat}")
        except Exception as e:
            logger.error(f"Failed to forward message to {chat}: {e}")
            if "banned" in str(e).lower() or "wait" in str(e).lower():
                banned_chats.add(chat)  # Add to banned list if rate-limited or banned
        await asyncio.sleep(2)  # Add delay to prevent rate-limiting

# Ensure the client runs continuously
def run_telethon():
    while True:
        try:
            with client:
                logger.info("Listening for new messages...")
                client.run_until_disconnected()
        except Exception as e:
            logger.error(f"Error: {e}")
            time.sleep(10)  # Wait before trying again

if __name__ == "__main__":
    # Run Flask web server in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Run Telethon client
    run_telethon()
