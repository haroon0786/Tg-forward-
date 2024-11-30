from telethon import TelegramClient, events

# Telegram API credentials
api_id = '27353904'  # Replace with your API ID
api_hash = '99b31ff29dc195f52e7bb6b526b2e4ca'  # Replace with your API Hash

# Source channel/group ID
source_chat = -1001859547091  # Replace with your source group ID

# List of destination groups/chats - Duplicates removed
destination_chats = set([
    'gyyfj7',
    'destination_group_2',
    '@CHAT_KING01',
    '@RESELLER_COMMUNITY2',
    '@dsstorechatgroup',
    '@bgmi_dva',
    '@flexopresellinghub',
    '@BGMIRESELLERSCOMMUNITY',
    '@rudraxchats',
    '@BGMI_Official_Chat_Group',
    '@BGMIRESELLERSGROUP',
    '@FRAGGER_RESELLING',
    '@ANTHONYBGMICHAT',
    '@JAATXONWER',
    '@ROLEXRESELLINGHUB',
    '@bgmipop023',
    '@SANKYCHATGROUP',
    '@Resellers_Group',
    '@RITESHxRESELLING',
    '@CLASH_OF_CLANS60',
    '@BGMlCHATGROUP',
    '@PUBGMANYA_CHAT',
    '@SUFIYANxRESELLER',
    '@QAZI_CHAT_GROUP',
    '@RESSELERGANG',
    '@RARE_BGMI_STORE_CHAT',
    '@KARMARESELLINGCOMMUNITY',
    '@OGxRESELLERSS',
    '@MADARAxCHAT',
    '@KINGRESELLER',
    '@VICTOR_CHATS10',
    '@SNAX_ESCROW',
    '@RESELLER_COMMUNITY4',
    '@RESELLERS_CHAT_GROUP',
    '@WAR_RESELLER',
    '@ScammerHellGroup',
    '@XeonChatGroup'
])
destination_chats = list(destination_chats)  # Convert back to list

# Create the Telegram client
client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage(chats=source_chat))
async def forward_message(event):
    for chat in destination_chats:
        try:
            # Forward the message with "forwarded from" attribution
            await client.forward_messages(chat, event.message)
            print(f"Message forwarded to {chat}")
        except Exception as e:
            print(f"Failed to forward message to {chat}: {e}")

# Start the client
with client:
    print("Listening for new messages...")
    client.run_until_disconnected()
