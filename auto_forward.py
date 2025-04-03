from telethon import TelegramClient, events

# Your Telegram API credentials
api_id = 26842829
api_hash = "6325758f0b207d005e09dddf2483a6b5"

# Friend’s username (bot you want to forward to)
friend_username = "@ExtraPeBot"  # Use this instead of user ID

# List of source channels (Use usernames or numeric IDs)
source_channels = [
    -1001158070897,
    -1001651396342,
    -1001856519972,
    -1001307859655,
    -1001670336143,
    -1002514331220
]

# Initialize the client
client = TelegramClient('session_name', api_id, api_hash)

async def get_friend_entity():
    """ Fetch friend entity once before starting the bot. """
    try:
        return await client.get_entity(friend_username)  # Using username method
    except Exception as e:
        print(f"❌ Error fetching friend's entity: {e}")
        return None

@client.on(events.NewMessage(chats=source_channels))
async def forward_message(event):
    if not friend_entity:
        print("❌ Friend entity missing, skipping message forwarding.")
        return

    try:
        await client.forward_messages(friend_entity, event.message)
        print(f"✅ Message forwarded from {event.chat_id} to {friend_entity.id}")
    except Exception as e:
        print(f"❌ Error forwarding message: {e}")

async def main():
    await client.start()
    print("🚀 Bot is running... Fetching friend entity...")
    
    global friend_entity  # Store friend entity globally
    friend_entity = await get_friend_entity()

    if friend_entity:
        print(f"✅ Friend entity found: {friend_entity.id}. Listening for messages...")
        await client.run_until_disconnected()
    else:
        print("❌ Failed to fetch friend entity. Exiting...")

client.loop.run_until_complete(main())