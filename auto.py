from pyrogram import Client, filters
from pyrogram.types import Message
import openai

# Konfigurasi API
api_id = "24773720"        # Ganti dengan API ID kamu
api_hash = "b8158aa3d0e6deabfb14c92ccf95ff8d"
openai.api_key = "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"

# Inisialisasi session userbot
app = Client("userbot", api_id=api_id, api_hash=api_hash)

# Status fitur per grup
auto_reply_status = {}

# Fungsi AI dari OpenAI
async def get_ai_response(text):
    try:
        result = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": text}]
        )
        return result.choices[0].message.content.strip()
    except Exception as e:
        return f"[AI Error] {e}"

# Perintah /autoreply on|off
@app.on_message(filters.command("autoreply", prefixes="/") & filters.group)
async def toggle_autoreply(client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Hanya admin boleh mengubah
    member = await client.get_chat_member(chat_id, user_id)
    if member.status not in ("administrator", "creator"):
        return await message.reply("Hanya admin yang bisa mengatur fitur ini.")

    args = message.text.lower().split()
    if len(args) != 2 or args[1] not in ("on", "off"):
        return await message.reply("Gunakan: /autoreply on atau /autoreply off")

    auto_reply_status[chat_id] = args[1] == "on"
    status = "AKTIF" if auto_reply_status[chat_id] else "NONAKTIF"
    await message.reply(f"Auto-reply sekarang *{status}*.")

 
@app.on_message(filters.group & filters.text & ~filters.me & ~filters.bot)
async def ai_autoreply(client, message: Message):
    chat_id = message.chat.id
    if auto_reply_status.get(chat_id, False):
        response = await get_ai_response(message.text)
        await message.reply(response)

app.run()
