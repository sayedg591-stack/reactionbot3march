"""
Telegram Channel Auto Reaction Bot
Bot will automatically add reactions to channels where it's admin
"""

import asyncio
import aiohttp
import json
import random
from datetime import datetime
import time

# ===================== BOT TOKEN LIST (Working Bots Only) =====================
BOT_TOKENS = [
    # Old bots
    "8524631629:AAFsNZpej0iiweOUCl5mvq8UoV0ryRcQcs0",  # jisanxreaction6bot
    "8543103576:AAFPzfvuO_hwMhoxPioPRLtyCASS5uJg2l8",  # jisanxreaction5bot
    "8558705643:AAH5w4kcQFWLyXVq_ywA5hV7R7Q3hY4pgZI",  # jisanxreaction9bot
    "8519115847:AAFxch3S1yIzvT4ASiR7pyh1rski9_pmTS0",  # jisanxreaction10bot
    "8221639563:AAFzUwIcW4cVChg2sFXhhEMQySD2Y3icl_s",  # jisanxreaction7bot
    "8498130158:AAFsoupI8Oz02AfBodr0LXATK4DNE4guFH8",  # jisanxreaction8bot
    "8424038815:AAHJNcKwoksKcqJ6MoimEBe8Jv7X1St2IL8",  # jisanxreaction15bot
    "8284921429:AAHBTmg326scQ6oHCQBUttelkTjniWRcYiQ",  # jisanxreaction14bot
    "7798491284:AAFsUASQm7sJgaklDDlQzaVEK_2bnNOMxQg",  # botmanebersinglealljisanx_bot
    "8096366191:AAEF2ZQYXtAJoHyDsuUvIIrI_UoF7EPpxb8",  # jgyjjygjyjybot
    "8395891439:AAF-9tLFBXo8S8qHb9AkhEobDm7W79a10zU",  # finorixprobot
    "8487045682:AAGGn5FD7owxGjwA9HYbCFSKMzhjpCYzOls",  # jisanxreaction3bot
    "8523873239:AAEZIj0B4kEpsqbizni0Gh8-QB5O_sU3rqg",  # jisanxreaction4bot
    "8293815029:AAGNe9Roq2aGKhyWVZgMvo6OwaZoWmYh3BA",  # Jisanxrection27bot
    "8271117844:AAHz454XKc870KhYeYA8seeDAzAnTICEOl0",  # Jisanxrection28bot
    "8222146140:AAGDLuXaiMSq-YUi46UUtiGNAwcJ0NmlPlY",  # Jisanxrection29bot
    "8287466194:AAHsE-DHL-YGzNl1uii_z-wUzxO095yAAlI",  # Jisanxrection30bot
    "8579880823:AAGq8PeRNqHKteYiOCDET-VWiTkwBAxiqNI",  # Jisanxrection31bot
    "8458237713:AAHWbRRQT6KYNpuHJVZLqiwTMZ7SaC82vZ8",  # Jisanxrection32bot
    "8492437873:AAFVkq7j1wVO_ON5b2yEdOSZHQCNYTcNisc",  # Jisanxrection33bot
    "8407419078:AAHx7oqWvodt2KT41aW39hMw0pRkZCYqVxM",  # Jisanxrection34bot
    "8203045836:AAH3MdXiNXuFB5s91evv0tzHT82YCJssSbQ",  # Jisanxrection35bot
    "7831068844:AAFpJxVbbZSyuRBHk-hoMLKpeSsfUcAG-4k",  # Jisanxrection36bot
    "8574147217:AAGGwFBh1fbMwElXiUaTdUQ6tSG2tw5c4R8",  # Jisanxrection37bot
    "7657638367:AAHJuZkpVXvDxZTcW2hYIluNtuohxeJtCGg",  # Jisanxrection38bot
    "8417068484:AAH-oPiLju_W-9sl_D-4RS-wj7KwcJ2_5f4",  # Jisanxrection39bot
    "7990868677:AAGE6W2Vc3G8ybnlPQ0j3go-MhIfmUVBe7I",  # Jisanxrection40bot
    "8530011880:AAHaitHiUGZX__LJ_ORdgcx1BfI_pZH27dM",  # Jisanxrection41bot
    "8387805490:AAFRWlTslLbqdIDDkbcNfQy6nxSpUgkLwwo",  # Jisanxrection42bot
    "8562483153:AAFd6yXgpiziDFuivxByHui1cNJAflYJsKc",  # Jisanxrection43bot
    "8450035810:AAHae8xAK_lJpqMZ7BI8h4yKLqcswE_L9tM",  # Jisanxrection44bot
    "8351315842:AAHY2-j58OeifYL6-oMkzAfbJxRXZD28MTk",  # Jisanxrection45bot
    "8501607135:AAE30LEZ7U4Mg_YRLizWtXgaFZ9nQBscomA",  # Jisanxrection46bot
    "8464589896:AAHHlF4SKMSpwUO2HFGRyfJPnFoGRCNV6Uo",  # Jisanxrection47bot
    "8507311777:AAE3FjXVVNaQyDEIu1F0nB9hpo_Me7_x91w",  # Jisanxrection48bot
    "8256276361:AAGx4go5WDTCg-4ldIH39oz20yrPjpsyQGs",  # Jisanxrection49bot
    "8591153215:AAGFQVDEo0yoXhX05H5eK-XTNVyE9GlbkYU",  # Jisanxrection50bot
    "8229218348:AAFxM_VyR1AUUVlgXrBoJ38pGo_Lm6bSSKA",  # Jisanxrection51bot
    "8253131272:AAHqU9eKjQNfeC96NvHqhV4EBHRlJ81hTzw",  # Jisanxrection52bot
    "8519157676:AAE99ktcjPV_xT8xHLQpoWFxpsxkwOGeWOs",  # Jisanxrection53bot
    "8306643283:AAHa7WW7fwsvHkz2imzOzZ-WY2l6khPbzyY",  # Jisanxrection54bot
    "8536259132:AAHoFdAG3yq82ag-x8REzP4PK99uCdmk9Gw",  # Jisanxrection55bot
    "8456731675:AAEKAgFpYn5TebwefpAzjVU74vpWGElrnaI",  # Jisanxrection56bot
    "8511464219:AAFwymstYrqNLiXHCCDd7Ll6EahHDUtILF4",  # Jisanxrection57bot
    "8590556272:AAEk7PMR1rRPSxVaa8lLmjBYmeFuEBw969M",  # Jisanxrection58bot
    "8546587618:AAEUFinj-6n3ngB9hCh9wQLZnZk3o1rmdWw",  # Jisanxrection59bot
    "8489846156:AAEwCXjBaonDY7OCKL5TEaST9WCYDjyRcVw",  # Jisanxrection60bot
    "8323862135:AAHVfDRdYdhX83lYgLcmsi59s_KsML4iPWU",  # Jisanxrection601bot
    "8506967189:AAHigacOo0xDFdSN6DMAbLaUCpA6WvKICD0",  # Jisanxrection62bot
    "8100231813:AAGuOIHoPyouaPzuWLhIDRzC-olU8mJqI5o",  # Jisanxrection63bot
    "8487982792:AAGh-J3Sy1RR-XIuNHaGbM7f0KOj8QaHa58",  # Jisanxrection64bot
    "8358101253:AAGZG35EvEUwt7P9XIlA-VkA7D8SY26WXbA",  # Jisanxrection65bot
    "8543218571:AAE6BFJK-WbIQr5BudY1RN6FNP_WFVHy_bI",  # Jisanxrection66bot
    "8564227784:AAEl3xzFiLKqcSSgO19SoO-p4tIkog0zOnA",  # Jisanxrection67bot
    "8574802650:AAHqIw1s12Eh_yP5DMpCsrUU4WLJ6HWMfys",  # Jisanxrection68bot
    "8038381121:AAE6fVN99Fs2cDTwRIGw0KA4iwlOz6DLfxo",  # Jisanxrection69bot
    "8259628212:AAHK8ohtZJ1fkyljcbhm7bFc-VWZC8UrJBQ",  # Jisanxrection70bot
    "8237930186:AAFzXO4_kKsawv3QuqIK2PqKSOQc_nCAG4c",  # Jisanxrection71bot
    "8517339103:AAHChHDe2eoyG2xhwewl-C2OjM89DQuHGcg",  # Jisanxrection72bot
    "7656375012:AAFW7KZscXDD0sOKztrvmD1yMNWALpki97I",  # Jisanxrection73bot
    "7680039867:AAEJtLCvtA6LKNOZgVHxmiH-5IOzG2LC5Jk",  # Autojoin5min_bot
]

# Telegram Supported Reaction Emojis (User selected)
REACTIONS = ["👍", "❤️", "😍", "❤️‍🔥", "🔥", "🥰", "😎"]

# Check Interval (seconds) - চেক করার সময়
CHECK_INTERVAL = 8  # প্রতি ৮ সেকেন্ডে চেক হবে

# Retry settings
MAX_RETRIES = 10  # আরও বেশি retry
BATCH_SIZE = 3  # ছোট batch - ৩টা বট একসাথে
DELAY_BETWEEN_BOTS = 0.8  # প্রতিটি বটের মধ্যে ০.৮ সেকেন্ড delay
DELAY_BETWEEN_BATCHES = 1.5  # ব্যাচের মধ্যে ১.৫ সেকেন্ড delay

# Tracking
reacted_messages = {}  # key: chat_id_msg_id, value: {'bots': set(), 'time': timestamp, 'retries': 0}


class ReactionBot:
    def __init__(self, token, index, emoji):
        self.token = token
        self.index = index
        self.emoji = emoji
        self.url = f"https://api.telegram.org/bot{token}"
        self.name = None
        self.last_update = 0
        self.channels = set()  # Channels where bot is admin
    
    async def init(self, session):
        """Initialize bot"""
        try:
            async with session.get(f"{self.url}/getMe") as r:
                data = await r.json()
                if data.get("ok"):
                    self.name = data["result"].get("username", f"Bot{self.index}")
                    return True
        except:
            pass
        return False
    
    async def react(self, session, chat_id, msg_id, retry_count=0):
        """Add reaction - Random emoji each time with retry logic"""
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                # Select a random emoji each time
                random_emoji = random.choice(REACTIONS)
                payload = {
                    "chat_id": chat_id,
                    "message_id": msg_id,
                    "reaction": json.dumps([{"type": "emoji", "emoji": random_emoji}]),
                    "is_big": False
                }
                async with session.post(f"{self.url}/setMessageReaction", data=payload) as r:
                    data = await r.json()
                    if data.get("ok"):
                        print(f"✅ Bot {self.index} (@{self.name}): {random_emoji} → msg {msg_id}")
                        return True
                    else:
                        error_code = data.get("error_code", "?")
                        error_desc = data.get("description", "Unknown error")
                        
                        # Rate limit - wait and retry
                        if error_code == 429:
                            retry_after = data.get("parameters", {}).get("retry_after", 5)
                            print(f"⏳ Bot {self.index}: Rate limited, waiting {retry_after}s...")
                            await asyncio.sleep(retry_after)
                            continue
                        
                        # Other retryable errors
                        if attempt < max_retries - 1:
                            await asyncio.sleep(1)
                            continue
                        
                        print(f"❌ Bot {self.index}: API Error [{error_code}] {error_desc}")
                        return False
                        
            except asyncio.TimeoutError:
                if attempt < max_retries - 1:
                    await asyncio.sleep(1)
                    continue
                print(f"❌ Bot {self.index}: Timeout")
                return False
            except Exception as e:
                if attempt < max_retries - 1:
                    await asyncio.sleep(1)
                    continue
                print(f"❌ Bot {self.index}: Error - {e}")
                return False
        
        return False
    
    async def get_updates(self, session):
        """Get updates"""
        try:
            params = {
                "offset": self.last_update + 1,
                "timeout": 30,
                "allowed_updates": json.dumps(["channel_post", "my_chat_member"])
            }
            async with session.get(f"{self.url}/getUpdates", params=params, timeout=aiohttp.ClientTimeout(total=35)) as r:
                data = await r.json()
                if data.get("ok"):
                    return data.get("result", [])
        except:
            pass
        return []


async def react_all(session, bots, chat_id, msg_id):
    """React from all bots - Sequential processing with proper delays"""
    global reacted_messages
    
    key = f"{chat_id}_{msg_id}"
    if key in reacted_messages:
        # Already processing this message
        return
    
    print(f"\n📬 New post: {msg_id} in {chat_id}")
    reacted_messages[key] = {
        'bots': set(),
        'time': time.time(),
        'retries': 0,
        'total_bots': len(bots),
        'chat_id': chat_id,
        'msg_id': msg_id
    }
    
    # Process bots in small batches to avoid rate limiting
    for i in range(0, len(bots), BATCH_SIZE):
        batch = bots[i:i + BATCH_SIZE]
        batch_num = (i // BATCH_SIZE) + 1
        total_batches = (len(bots) + BATCH_SIZE - 1) // BATCH_SIZE
        
        # Process each bot in the batch sequentially
        for bot in batch:
            try:
                if await bot.react(session, chat_id, msg_id):
                    reacted_messages[key]['bots'].add(bot.index)
            except Exception as e:
                print(f"❌ Bot {bot.index} error in react_all: {e}")
            
            # Delay between bots
            await asyncio.sleep(DELAY_BETWEEN_BOTS)
        
        # Longer delay between batches
        if i + BATCH_SIZE < len(bots):
            await asyncio.sleep(DELAY_BETWEEN_BATCHES)
    
    done = len(reacted_messages[key]['bots'])
    total = len(bots)
    print(f"✨ Initial: {done}/{total} reactions added")
    
    if done < total:
        print(f"⏳ {total - done} missing - will retry automatically")


async def check_missing(session, bots):
    """Check and fix missing reactions - Aggressive retry"""
    global reacted_messages
    
    current_time = time.time()
    messages_to_check = []
    
    # Get all messages that need checking (within last 3 minutes)
    for key, data in list(reacted_messages.items()):
        age = current_time - data['time']
        done = len(data['bots'])
        total = data['total_bots']
        retries = data['retries']
        
        # Check if incomplete and within retry window
        if done < total and retries < MAX_RETRIES and age < 180:
            messages_to_check.append((key, total - done))  # Store missing count
    
    if not messages_to_check:
        return
    
    # Sort by missing count (prioritize messages with fewer missing)
    messages_to_check.sort(key=lambda x: x[1])
    
    total_missing = sum(m[1] for m in messages_to_check)
    print(f"\n🔍 Checking {len(messages_to_check)} messages ({total_missing} total missing reactions)...")
    
    for key, _ in messages_to_check:
        data = reacted_messages[key]
        chat_id = data.get('chat_id')
        msg_id = data.get('msg_id')
        
        # Fallback for old format
        if chat_id is None:
            parts = key.rsplit("_", 1)
            chat_id = int(parts[0])
            msg_id = int(parts[1])
        
        done_bots = data['bots']
        missing_bots = [bot for bot in bots if bot.index not in done_bots]
        
        if not missing_bots:
            continue
        
        data['retries'] += 1
        retry_num = data['retries']
        print(f"\n🔧 Retry #{retry_num}/{MAX_RETRIES} for msg {msg_id}: {len(missing_bots)} missing")
        
        fixed_count = 0
        
        # Process missing bots in small batches
        for i in range(0, len(missing_bots), BATCH_SIZE):
            batch = missing_bots[i:i + BATCH_SIZE]
            
            for bot in batch:
                try:
                    if await bot.react(session, chat_id, msg_id):
                        data['bots'].add(bot.index)
                        fixed_count += 1
                except Exception as e:
                    print(f"  ❌ Bot {bot.index}: {e}")
                
                await asyncio.sleep(DELAY_BETWEEN_BOTS)
            
            # Delay between batches
            if i + BATCH_SIZE < len(missing_bots):
                await asyncio.sleep(DELAY_BETWEEN_BATCHES)
        
        done = len(data['bots'])
        total = data['total_bots']
        
        if fixed_count > 0:
            print(f"  ✅ Fixed {fixed_count} reactions | Status: {done}/{total}")
        
        if done == total:
            print(f"  🎉 All reactions complete for msg {msg_id}!")
        elif retry_num >= MAX_RETRIES:
            print(f"  ⚠️ Max retries reached for msg {msg_id} ({done}/{total})")
    
    # Clean up old entries (older than 5 minutes)
    for key in list(reacted_messages.keys()):
        if current_time - reacted_messages[key]['time'] > 300:
            del reacted_messages[key]


async def run_bot(bot, all_bots, session):
    """Run a single bot"""
    while True:
        try:
            updates = await bot.get_updates(session)
            
            for update in updates:
                bot.last_update = update["update_id"]
                
                # Channel post
                post = update.get("channel_post")
                if post:
                    chat_id = post["chat"]["id"]
                    msg_id = post["message_id"]
                    bot.channels.add(chat_id)
                    await react_all(session, all_bots, chat_id, msg_id)
                
                # Bot added/removed from channel
                member = update.get("my_chat_member")
                if member:
                    chat = member.get("chat", {})
                    if chat.get("type") == "channel":
                        new_status = member.get("new_chat_member", {}).get("status")
                        if new_status == "administrator":
                            bot.channels.add(chat["id"])
                            print(f"📢 Bot {bot.index} added as admin to: {chat.get('title', chat['id'])}")
                        elif new_status in ["left", "kicked"]:
                            bot.channels.discard(chat["id"])
            
            await asyncio.sleep(1)
        except Exception as e:
            print(f"❌ Bot {bot.index} error: {e}")
            await asyncio.sleep(5)


async def main():
    print("=" * 60)
    print("🤖 Telegram Auto Reaction Bot - Enhanced Version")
    print("=" * 60)
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔢 Bots: {len(BOT_TOKENS)}")
    print(f"🎭 Emojis: {len(REACTIONS)} types available")
    print(f"⏱️ Check Interval: {CHECK_INTERVAL}s (Max retries: {MAX_RETRIES})")
    print(f"📦 Batch Size: {BATCH_SIZE} bots at a time")
    print("=" * 60)
    
    # Create bots
    bots = []
    for i, token in enumerate(BOT_TOKENS):
        emoji = REACTIONS[i % len(REACTIONS)]
        bots.append(ReactionBot(token, i + 1, emoji))
    
    # Initialize
    print("\n🔧 Initializing bots...")
    async with aiohttp.ClientSession() as session:
        tasks = [bot.init(session) for bot in bots]
        results = await asyncio.gather(*tasks)
        
        active = [b for b, ok in zip(bots, results) if ok]
        for bot in active:
            print(f"  ✅ Bot {bot.index}: @{bot.name}")
        
        failed = len(bots) - len(active)
        if failed:
            print(f"  ❌ {failed} bots failed")
        
        if not active:
            print("\n❌ No bots available!")
            return
        
        print(f"\n✅ {len(active)} bots ready!")
        print("\n" + "=" * 60)
        print("📢 Add bots as admin to your channel")
        print("   Auto reactions will be added where bot is admin")
        print("=" * 60)
        print("\n👂 Listening for channel posts...\n")
        
        # Run all bots
        bot_tasks = [run_bot(bot, active, session) for bot in active]
        
        # Missing check task - runs frequently
        async def check_loop():
            while True:
                await asyncio.sleep(CHECK_INTERVAL)
                await check_missing(session, active)
        
        bot_tasks.append(check_loop())
        await asyncio.gather(*bot_tasks)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Bot stopped.")
