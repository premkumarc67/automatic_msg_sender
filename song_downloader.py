from telethon import TelegramClient
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

api_id = int(os.getenv("api_id"))
api_hash = os.getenv("api_hash")
phone_number = os.getenv("phone_number")
target_bot = '@songdl_bot'

# The list of songs you want to process
song_list = [
    'Vaadi pulla vaadi',  # Including your original one
    'Vaarayo Vaarayo',
    'Paththavaikkum',
    'Kannadi Poove',
    'Enadhuyire',
    'Yaaro Manathile'
]
# ---------------------

async def interact_with_bot():
    # Create the client
    async with TelegramClient('anon', api_id, api_hash) as client:
        
        # 1. Login if not already authorized
        if not await client.is_user_authorized():
            await client.send_code_request(phone_number)
            try:
                await client.sign_in(phone_number, input('Enter the code: '))
            except Exception:
                # Handle 2FA if enabled
                password = input('Two-step verification password: ')
                await client.sign_in(password=password)

        print(f"Logged in. Starting batch process for {len(song_list)} songs.\n")

        # 2. Iterate through the list of songs
        for index, song in enumerate(song_list, 1):
            print(f"[{index}/{len(song_list)}] Searching for: {song}")

            try:
                # Open a conversation for this specific song
                # Exclusive=True helps prevent message mixing if multiple run
                async with client.conversation(target_bot, timeout=30, exclusive=True) as conv:
                    
                    # Send the song name
                    await conv.send_message(song)

            except asyncio.TimeoutError:
                print(f"  > ERROR: Bot took too long to respond to '{song}'. Skipping.")
            except Exception as e:
                print(f"  > ERROR processing '{song}': {e}")

            # 3. SAFETY DELAY
            # Sleep for 5-10 seconds between songs to avoid "FloodWait" errors
            print("  > Waiting 5 seconds before next song...\n")
            await asyncio.sleep(5)

        print("All songs processed.")

if __name__ == '__main__':
    asyncio.run(interact_with_bot())