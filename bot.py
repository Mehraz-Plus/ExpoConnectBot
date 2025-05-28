from telethon import TelegramClient, events
from telethon.tl.types import PeerUser
from telethon import Button
from env import env
from mongo import Mongo
import lang
import datetime

# Environment detection
if env == 'live':
    import config_live
    config = config_live
elif env == 'dev':
    import config_dev
    config = config_dev
else:
    import config_test
    config = config_test

# Connect to database
db = Mongo(config.db_host, config.db_port, config.db_name)

# Initialize Telegram client
if config.proxy:
    bot = TelegramClient(session=config.session_name, api_id=config.api_id, api_hash=config.api_hash,
                         proxy=(config.proxy_protocol, config.proxy_host, config.proxy_port))
else:
    bot = TelegramClient(session=config.session_name, api_id=config.api_id, api_hash=config.api_hash)


@bot.on(events.NewMessage(pattern='/start', incoming=True))
async def start(event):
    welcome_msg = f"{lang.get('welcome', 'en')}\n\n{lang.get('welcome', 'fa')}\n\n{lang.get('welcome', 'cn')}\n\n{lang.get('welcome', 'ar')}"
    welcome_btns = []
    welcome_btns.append([Button.inline(lang.get('english', 'en'), b'select_english')])
    welcome_btns.append([Button.inline(lang.get('persian', 'fa'), b'select_persian')])
    welcome_btns.append([Button.inline(lang.get('chinese', 'cn'), b'select_chinese')])
    welcome_btns.append([Button.inline(lang.get('arabic', 'ar'), b'select_arabic')])
    await event.respond(welcome_msg, buttons=welcome_btns)
    raise events.StopPropagation


@bot.on(events.CallbackQuery(pattern=b'select_english'))
async def select_english(event):
    db.insert('language', {'user_id': event.sender_id, 'language': 'en', 'start_time': datetime.datetime.now()})
    await main_conv(event, 'en')
    raise events.StopPropagation

@bot.on(events.CallbackQuery(pattern=b'select_persian'))
async def select_persian(event):
    db.insert('language', {'user_id': event.sender_id, 'language': 'fa', 'start_time': datetime.datetime.now()})
    await main_conv(event, 'fa')
    raise events.StopPropagation

@bot.on(events.CallbackQuery(pattern=b'select_chinese'))
async def select_chinese(event):
    db.insert('language', {'user_id': event.sender_id, 'language': 'cn', 'start_time': datetime.datetime.now()})
    await main_conv(event, 'cn')
    raise events.StopPropagation

@bot.on(events.CallbackQuery(pattern=b'select_arabic'))
async def select_arabic(event):
    db.insert('language', {'user_id': event.sender_id, 'language': 'ar', 'start_time': datetime.datetime.now()})
    await main_conv(event, 'ar')
    raise events.StopPropagation

async def main_conv(event, user_lang):
    async with bot.conversation(event.sender_id) as conv:
            await conv.send_message(lang.get('enter_company_name', user_lang))
            response = await conv.get_response()
            company_name = response.text
            await conv.send_message(lang.get('enter_company_country', user_lang))
            response = await conv.get_response()
            company_country = response.text
            await conv.send_message(lang.get('enter_company_industry', user_lang))
            response = await conv.get_response()
            company_industry = response.text
            await conv.send_message(lang.get('enter_company_contact', user_lang))
            response = await conv.get_response()
            company_contact = response.text
            db.insert('company', 
                      {'name': company_name,
                       'country': company_country,
                       'industry': company_industry,
                       'contact': company_contact,
                       'user_id': event.sender_id})
            for admin in config.admin_list:
                await bot.send_message(admin, f'{company_name}\n\n{company_country}\n\n{company_industry}\n\n{company_contact}')
            await conv.send_message(lang.get('info_sent_successfully', user_lang))


# Connect to Telegram and run in a loop
try:
    print('bot starting...')
    bot.start(bot_token=config.bot_token)
    print('bot started')
    bot.run_until_disconnected()
finally:
    print('never runs in async mode!')