import socket
socket.setdefaulttimeout(30)

# Force IPv4
import requests
requests.packages.urllib3.util.connection.HAS_IPV6 = False

import os
import json
import re
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ============================================
# CONFIGURATION
# ============================================
BOT_TOKEN = "8978819633:AAF9si6gH_sqvxC4uExZdwIK0gSkx8ToLq8"
ADMIN_ID = 6012442109
ACCOUNTANT_ID = 6012442109  # Can be same as ADMIN_ID, change if needed
AGENT_USERNAME = "@Saudi_1xbet_agent"
CASHBACK_PERCENT = 0.25  # 25% cashback

# ============================================
# DATA DIRECTORY - Persistent storage on Railway
# ============================================
if os.path.exists("/app/data"):
    DATA_DIR = "/app/data"
else:
    DATA_DIR = "."

ACCOUNTS_FILE = os.path.join(DATA_DIR, "accounts.json")
USED_FILE = os.path.join(DATA_DIR, "used_accounts.json")
DEPOSIT_FILE = os.path.join(DATA_DIR, "deposits.json")
WITHDRAW_FILE = os.path.join(DATA_DIR, "withdrawals.json")
PAYMENT_METHODS_FILE = os.path.join(DATA_DIR, "payment_methods.json")
VIDEOS_FILE = os.path.join(DATA_DIR, "videos.json")
SHARES_FILE = os.path.join(DATA_DIR, "shares.json")

# ============================================
# FILE HANDLING
# ============================================
def load_accounts():
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_accounts(accounts):
    with open(ACCOUNTS_FILE, 'w') as f:
        json.dump(accounts, f, indent=2)

def load_used():
    if os.path.exists(USED_FILE):
        with open(USED_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_used(used):
    with open(USED_FILE, 'w') as f:
        json.dump(used, f, indent=2)

def load_deposits():
    if os.path.exists(DEPOSIT_FILE):
        with open(DEPOSIT_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_deposits(deposits):
    with open(DEPOSIT_FILE, 'w') as f:
        json.dump(deposits, f, indent=2)

def load_withdrawals():
    if os.path.exists(WITHDRAW_FILE):
        with open(WITHDRAW_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_withdrawals(withdrawals):
    with open(WITHDRAW_FILE, 'w') as f:
        json.dump(withdrawals, f, indent=2)

def load_payment_methods():
    """Load payment methods from file. Returns empty dict if file doesn't exist."""
    if os.path.exists(PAYMENT_METHODS_FILE):
        try:
            with open(PAYMENT_METHODS_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Payment methods file corrupted, starting fresh.")
            return {}
    return {}

def save_payment_methods(methods):
    with open(PAYMENT_METHODS_FILE, 'w') as f:
        json.dump(methods, f, indent=2)

def load_videos():
    if os.path.exists(VIDEOS_FILE):
        try:
            with open(VIDEOS_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Videos file corrupted, starting fresh.")
            return {}
    return {}

def save_videos(videos):
    with open(VIDEOS_FILE, 'w') as f:
        json.dump(videos, f, indent=2)

def load_shares():
    if os.path.exists(SHARES_FILE):
        with open(SHARES_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_shares(shares):
    with open(SHARES_FILE, 'w') as f:
        json.dump(shares, f, indent=2)

# ============================================
# USER STATE STORAGE
# ============================================
user_states = {}
admin_states = {}

# ============================================
# HELPER FUNCTIONS - Handle both old and new data formats
# ============================================

def get_user_today_count(user_id, used_data):
    if user_id not in used_data:
        return 0
    entry = used_data[user_id]
    if isinstance(entry, list):
        accounts = entry
    else:
        accounts = entry.get("accounts", [])
    today = datetime.now().strftime("%Y-%m-%d")
    return sum(1 for a in accounts if a.get("date") == today)

def get_user_accounts(user_id, used_data):
    if user_id not in used_data:
        return []
    entry = used_data[user_id]
    if isinstance(entry, list):
        return [a.get("account") for a in entry]
    else:
        return [a.get("account") for a in entry.get("accounts", [])]

def update_user_data(user_id, username, account=None):
    """Save user data in new format, converting old format if needed."""
    used = load_used()
    if user_id in used and isinstance(used[user_id], list):
        old_accounts = used[user_id]
        used[user_id] = {"username": username, "accounts": old_accounts}
    elif user_id not in used:
        used[user_id] = {"username": username, "accounts": []}
    else:
        if "username" not in used[user_id] or not used[user_id]["username"]:
            used[user_id]["username"] = username
        if "accounts" not in used[user_id]:
            used[user_id]["accounts"] = []
    if account:
        used[user_id]["accounts"].append(account)
    save_used(used)

# ============================================
# KEYBOARD FUNCTIONS
# ============================================
def get_main_menu_keyboard():
    return ReplyKeyboardMarkup([
        ["🎰 Get Account", "💬 Talk to Agent"],
        ["📋 My Accounts", "💳 Deposit & Withdraw"],
        ["📹 Video Tutorials"],
        ["📢 Share Bot"],
        ["🔙 Back to Menu"]
    ], resize_keyboard=True)

def get_admin_menu_keyboard():
    return ReplyKeyboardMarkup([
        ["🎰 Get Account", "💬 Talk to Agent"],
        ["📋 My Accounts", "💳 Deposit & Withdraw"],
        ["📹 Video Tutorials"],
        ["📢 Share Bot"],
        ["📊 /stats", "📋 /listaccounts"],
        ["➕ /ass", "💳 /pm"],
        ["🔙 Back to Menu"]
    ], resize_keyboard=True)

def get_back_to_menu_keyboard():
    return ReplyKeyboardMarkup([["🔙 Back to Menu"]], resize_keyboard=True)

def get_get_another_keyboard():
    return ReplyKeyboardMarkup([
        ["🎰 Get Another Account"],
        ["📋 My Accounts"],
        ["📢 Share Bot"],
        ["🔙 Back to Menu"]
    ], resize_keyboard=True)

def get_pm_menu_keyboard():
    return ReplyKeyboardMarkup([
        ["📋 List Methods", "➕ Add Method"],
        ["✏️ Edit Method", "🗑️ Delete Method"],
        ["🔙 Back to Menu"]
    ], resize_keyboard=True)

def get_admin_video_keyboard():
    return ReplyKeyboardMarkup([
        ["📹 Add Video", "🗑️ Delete Video"],
        ["📋 List Videos"],
        ["🔙 Back to Menu"]
    ], resize_keyboard=True)

def get_video_menu_keyboard(videos):
    keyboard = []
    for video_id, video_data in videos.items():
        keyboard.append([KeyboardButton(f"🎬 {video_data['title']}")])
    keyboard.append(["🔙 Back to Menu"])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_stats_menu_keyboard():
    return ReplyKeyboardMarkup([
        ["📊 Overall Stats"],
        ["👤 User Stats"],
        ["💰 Player ID Cashback"],
        ["🔙 Back to Menu"]
    ], resize_keyboard=True)

# ============================================
# MAIN BOT COMMANDS
# ============================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    is_member = await is_user_member(user_id, "saudi_1xbet_accounts", context)
    if not is_member:
        keyboard = [
            [InlineKeyboardButton("📢 Join Our Channel", url="https://t.me/saudi_1xbet_accounts")],
            [InlineKeyboardButton("✅ I've Joined! Check Subscription", callback_data="check_subscription")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "👋 *Welcome!*\n\nTo use this bot, you must first join our channel:\n"
            "➡️ [1xbet Saudi Arabia](https://t.me/saudi_1xbet_accounts)\n\n"
            "After joining, click the button below to continue.",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
        return
    await show_main_menu(update, context)

async def is_user_member(user_id, channel_username, context):
    try:
        bot = context.bot
        chat_member = await bot.get_chat_member(chat_id=f"@{channel_username}", user_id=user_id)
        return chat_member.status in ["member", "administrator", "creator"]
    except Exception as e:
        print(f"Error checking membership: {e}")
        return False

async def show_main_menu(update, context):
    user_id = update.effective_user.id
    username = update.effective_user.username or "NoUsername"
    update_user_data(str(user_id), username)
    if user_id == ADMIN_ID:
        keyboard = get_admin_menu_keyboard()
        menu_text = (
            "🎰 *Welcome Admin!*\n\n"
            "👑 *Admin Panel*\n➕ `/ass` - Add accounts\n"
            "📊 `/stats` - View statistics\n"
            "📋 `/listaccounts` - View all accounts\n"
            "💳 `/pm` - Payment Methods\n\n"
            "📌 *User Features:*\n"
            "💰 *Get 30% CASHBACK on all losses!*\n"
            "📌 You can get up to *2 accounts per day*\n"
            "💳 *Deposit & Withdraw easily!*\n\n"
            "👆 Click the buttons below:"
        )
    else:
        keyboard = get_main_menu_keyboard()
        menu_text = (
            "🎰 *Welcome to Saudi 1xBet Bot!*\n\n"
            "💰 *Get 30% CASHBACK on all losses!*\n"
            "📌 You can get up to *2 accounts per day*\n"
            "💳 *Deposit & Withdraw easily!*\n\n"
            "👆 Click the buttons below:"
        )
    await update.message.reply_text(menu_text, parse_mode="Markdown", reply_markup=keyboard)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data.startswith(("deposit_accept_", "deposit_reject_", "withdraw_accept_", "withdraw_reject_")):
        await handle_accountant_action(update, context)
        return
    if query.data == "check_subscription":
        user_id = query.from_user.id
        is_member = await is_user_member(user_id, "saudi_1xbet_accounts", context)
        if is_member:
            await query.message.reply_text("✅ Subscription verified! Welcome!", reply_markup=get_main_menu_keyboard())
        else:
            keyboard = [
                [InlineKeyboardButton("📢 Join Our Channel", url="https://t.me/saudi_1xbet_accounts")],
                [InlineKeyboardButton("✅ I've Joined! Check Subscription", callback_data="check_subscription")]
            ]
            await query.message.reply_text(
                "❌ *Not a member yet!*\n\n"
                "Please join [our channel](https://t.me/saudi_1xbet_accounts) first, then click 'Check Subscription' again.",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        return

# ============================================
# MESSAGE HANDLER - COMPLETE FIX
# ============================================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    used_data = load_used()
    await update.message.chat.send_action(action="typing")

    if await process_rejection_reason(update, context):
        return

    # Video state check
    if user_id in admin_states and admin_states[user_id].get("action") == "add_video":
        print(f"📹 User {user_id} in add_video state")
        if update.message.video or (update.message.document and update.message.document.mime_type and update.message.document.mime_type.startswith('video/')):
            await handle_video_buttons(update, context)
            return
        elif update.message.text:
            if update.message.text.lower() == "/cancel":
                admin_states.pop(user_id, None)
                await update.message.reply_text("❌ *Cancelled!*", parse_mode="Markdown", reply_markup=get_admin_video_keyboard())
                return
            else:
                await handle_video_buttons(update, context)
                return
        else:
            await update.message.reply_text("📹 *Please send a video file!*\n\nType /cancel to cancel.", parse_mode="Markdown")
            return

    if update.message.photo:
        await handle_receipt(update, context)
        return

    message_text = update.message.text if update.message.text else ""
    print(f"🔍 DEBUG: handle_message received: '{message_text}' from user {user_id}")

    if message_text == "🔙 Back to Menu":
        admin_states.pop(user_id, None)
        await show_main_menu(update, context)
        return

    # Admin: Stats Menu
    if update.effective_user.id == ADMIN_ID:
        if message_text in ["📊 Overall Stats", "👤 User Stats", "💰 Player ID Cashback"]:
            await handle_stats_buttons(update, context)
            return

    # Admin: Payment Methods Management
    if update.effective_user.id == ADMIN_ID:
        if user_id in admin_states:
            await handle_pm_state(update, context)
            return
        if message_text in ["📋 List Methods", "➕ Add Method", "✏️ Edit Method", "🗑️ Delete Method"]:
            await handle_pm_buttons(update, context)
            return

    # Admin Commands from buttons
    if message_text == "➕ /ass":
        if update.effective_user.id != ADMIN_ID:
            await update.message.reply_text("⛔ *Unauthorized!*", parse_mode="Markdown")
            return
        await update.message.reply_text(
            "📝 *How to add an account:*\n\n"
            "`/ass Username: 123456789 Password: abcd1234`\n\n"
            "**Example:**\n"
            "`/ass Username: Ahmed_123 Password: SecurePass456`\n\n"
            "You can also add multiple:\n"
            "`/ass Username: user1 Password: pass1, Username: user2 Password: pass2`",
            parse_mode="Markdown"
        )
        return

    if message_text == "📊 /stats":
        if update.effective_user.id != ADMIN_ID:
            await update.message.reply_text("⛔ *Unauthorized!*", parse_mode="Markdown")
            return
        await show_stats_menu(update, context)
        return

    if message_text == "📋 /listaccounts":
        if update.effective_user.id != ADMIN_ID:
            await update.message.reply_text("⛔ *Unauthorized!*", parse_mode="Markdown")
            return
        await list_accounts(update, context)
        return

    if message_text == "💳 /pm":
        if update.effective_user.id != ADMIN_ID:
            await update.message.reply_text("⛔ *Unauthorized!*", parse_mode="Markdown")
            return
        await manage_payment_methods(update, context)
        return

    # Video Tutorials
    if message_text == "📹 Video Tutorials":
        await show_video_tutorials(update, context)
        return
    if message_text in ["📹 Add Video", "🗑️ Delete Video", "📋 List Videos"] or message_text.startswith(("🎬 ", "🗑️ ")):
        await handle_video_buttons(update, context)
        return

    # Share Bot
    if message_text == "📢 Share Bot":
        await handle_share_bot(update, context)
        return

    # User Features
    if message_text in ["🎰 Get Account", "🎰 Get Another Account"]:
        await handle_get_account(update, user_id, used_data)
        return

    if message_text == "💬 Talk to Agent":
        await update.message.reply_text(
            f"💬 *Contact Our Agent*\n\n📞 Reach out to *{AGENT_USERNAME}* for:\n"
            "• Account issues\n• Technical support\n• Questions about 1xBet\n"
            "• Cashback inquiries\n\n👉 Click here: *{AGENT_USERNAME}*",
            parse_mode="Markdown",
            reply_markup=get_back_to_menu_keyboard()
        )
        return

    if message_text == "📋 My Accounts":
        await handle_my_accounts(update, user_id, used_data)
        return

    if message_text == "💳 Deposit & Withdraw":
        await show_deposit_withdraw_menu(update, context)
        return

    if message_text == "💰 Deposit":
        await start_deposit(update, context)
        return

    if message_text == "💸 Withdraw":
        await start_withdraw(update, context)
        return

    # Handle user states (deposit/withdraw flows)
    if user_id in user_states:
        state = user_states[user_id]
        action = state.get("action")
        step = state.get("step")
        if action == "deposit":
            if step == "player_id":
                await process_deposit_player_id(update, context)
                return
            elif step == "method":
                await process_deposit_method(update, context)
                return
            elif step == "amount":
                await process_deposit_amount(update, context)
                return
        elif action == "withdraw":
            if step == "method":
                await process_withdraw_method(update, context)
                return
            elif step == "player_id":
                await process_withdraw_player_id(update, context)
                return
            elif step == "details":
                await process_withdraw_field(update, context)
                return
            elif step == "code":
                await process_withdraw_code(update, context)
                return

    # ✅ ADMIN STATES CHECK - MUST BE OUTSIDE AND AT THE BOTTOM
    print(f"🔍 DEBUG: admin_states before check: {admin_states}")  # This line should appear
    if user_id in admin_states:
        state = admin_states[user_id]
        action = state.get("action")
        print(f"🔍 DEBUG: Found admin state action={action} for user {user_id}")
        if action == "user_stats":
            await process_user_stats(update, context)
            return
        elif action == "cashback":
            step = state.get("step")
            if step == "waiting_for_player_id":
                await process_cashback_player_id(update, context)
                return
            elif step == "waiting_for_start_date":
                await process_cashback_start_date(update, context)
                return
            elif step == "waiting_for_end_date":
                await process_cashback_end_date(update, context)
                return
        elif action == "withdraw_amount":
            print(f"🔍 DEBUG: Calling process_withdraw_amount for withdraw_id={state.get('withdraw_id')}")
            await process_withdraw_amount(update, context)
            return

    # Default reply
    await update.message.reply_text(
        "❌ *I don't understand that command.*\n\nPlease use the buttons below:",
        parse_mode="Markdown",
        reply_markup=get_main_menu_keyboard()
    )

# ============================================
# SHARE BOT
# ============================================

async def handle_share_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    shares = load_shares()
    share_count = shares.get(user_id, 0)
    shares[user_id] = share_count + 1
    save_shares(shares)
    bot_username = (await context.bot.get_me()).username
    share_text = (
        f"📢 *Share Bot & Earn Rewards!*\n\n"
        f"🤖 *Bot:* @{bot_username}\n\n"
        f"📊 *You have shared:* {share_count + 1} times\n"
        f"🎁 *Rewards:* Ask our agent for special bonuses!\n\n"
        f"📤 *Share link:* `https://t.me/{bot_username}`\n"
        f"💬 Contact agent: {AGENT_USERNAME}"
    )
    await update.message.reply_text(share_text, parse_mode="Markdown", reply_markup=get_back_to_menu_keyboard())

# ============================================
# STATS SYSTEM
# ============================================

async def show_stats_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ *Unauthorized!*", parse_mode="Markdown")
        return
    await show_overall_stats(update, context)

async def handle_stats_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text
    if message_text == "📊 Overall Stats":
        await show_overall_stats(update, context)
    elif message_text == "👤 User Stats":
        await show_user_stats(update, context)
    elif message_text == "💰 Player ID Cashback":
        await show_cashback_calculator(update, context)

async def show_overall_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    accounts = load_accounts()
    used_data = load_used()
    deposits = load_deposits()
    withdrawals = load_withdrawals()

    total_users = len(used_data)
    total_accounts_given = 0
    today = datetime.now().strftime("%Y-%m-%d")
    today_given = 0
    for entry in used_data.values():
        if isinstance(entry, list):
            user_accounts = entry
        else:
            user_accounts = entry.get("accounts", [])
        total_accounts_given += len(user_accounts)
        today_given += sum(1 for a in user_accounts if a.get("date") == today)

    deposits_accepted = sum(1 for d in deposits.values() if d.get("status") == "completed")
    deposits_rejected = sum(1 for d in deposits.values() if d.get("status") == "rejected")
    total_deposit_amount = sum(d.get("amount", 0) for d in deposits.values() if d.get("status") == "completed")

    withdrawals_accepted = sum(1 for w in withdrawals.values() if w.get("status") == "completed")
    withdrawals_rejected = sum(1 for w in withdrawals.values() if w.get("status") == "rejected")
    total_withdraw_amount = sum(w.get("amount", 0) for w in withdrawals.values() if w.get("status") == "completed")

    keyboard = get_stats_menu_keyboard()
    await update.message.reply_text(
        f"📊 *Bot Statistics*\n\n"
        f"📦 *Available Accounts:* {len(accounts)}\n"
        f"👤 *Total Users used bot:* {total_users}\n"
        f"📤 *Total Accounts Given:* {total_accounts_given}\n"
        f"📅 *Given Today:* {today_given}\n"
        f"💰 *Cashback:* 30% on all losses\n\n"
        f"💳 *Deposit Stats:*\n   ✅ Accepted: {deposits_accepted}\n"
        f"   ❌ Rejected: {deposits_rejected}\n"
        f"   💵 Total Accepted Amount: {total_deposit_amount:,.0f} SAR\n\n"
        f"💸 *Withdraw Stats:*\n   ✅ Accepted: {withdrawals_accepted}\n"
        f"   ❌ Rejected: {withdrawals_rejected}\n"
        f"   💵 Total Accepted Amount: {total_withdraw_amount:,.0f} SAR",
        parse_mode="Markdown",
        reply_markup=keyboard
    )

async def show_user_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    admin_states[user_id] = {"action": "user_stats", "step": "waiting_for_username"}
    await update.message.reply_text(
        "👤 *User Stats*\n\nPlease enter the Telegram username to check stats:\n\n"
        "📝 *Example:* `@username` or `username`\n\nType /cancel to cancel.",
        parse_mode="Markdown",
        reply_markup=get_back_to_menu_keyboard()
    )

async def process_user_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    username_input = update.message.text.strip()
    if username_input.startswith("@"):
        username_input = username_input[1:]

    used_data = load_used()
    deposits = load_deposits()
    withdrawals = load_withdrawals()
    shares = load_shares()

    found_user_id = None
    found_username = username_input
    for uid, entry in used_data.items():
        if isinstance(entry, dict) and entry.get("username", "").lower() == username_input.lower():
            found_user_id = uid
            break
    if not found_user_id:
        for did, deposit in deposits.items():
            if deposit.get("username", "").lower() == username_input.lower():
                found_user_id = deposit.get("user_id")
                break
        if not found_user_id:
            for wid, withdrawal in withdrawals.items():
                if withdrawal.get("username", "").lower() == username_input.lower():
                    found_user_id = withdrawal.get("user_id")
                    break
    if not found_user_id and username_input.isdigit():
        found_user_id = username_input
        found_username = "User " + username_input

    if not found_user_id:
        await update.message.reply_text(f"❌ *User not found!*\n\nNo user found with username `{username_input}`.", parse_mode="Markdown", reply_markup=get_stats_menu_keyboard())
        admin_states.pop(user_id, None)
        return

    user_accounts = get_user_accounts(found_user_id, used_data)
    user_deposits = [d for d in deposits.values() if d.get("user_id") == found_user_id]
    user_withdrawals = [w for w in withdrawals.values() if w.get("user_id") == found_user_id]

    total_accounts = len(user_accounts)
    given_today = get_user_today_count(found_user_id, used_data)

    deposits_accepted = sum(1 for d in user_deposits if d.get("status") == "completed")
    deposits_rejected = sum(1 for d in user_deposits if d.get("status") == "rejected")
    total_deposit_amount = sum(d.get("amount", 0) for d in user_deposits if d.get("status") == "completed")

    withdrawals_accepted = sum(1 for w in user_withdrawals if w.get("status") == "completed")
    withdrawals_rejected = sum(1 for w in user_withdrawals if w.get("status") == "rejected")
    total_withdraw_amount = sum(w.get("amount", 0) for w in user_withdrawals if w.get("status") == "completed")

    share_count = shares.get(found_user_id, 0)
    admin_states.pop(user_id, None)

    await update.message.reply_text(
        f"👤 *User Stats for @{found_username}*\n\n"
        f"📤 *Total Accounts Given:* {total_accounts}\n"
        f"📅 *Given Today:* {given_today}\n\n"
        f"💳 *Deposit Stats:*\n   ✅ Accepted: {deposits_accepted}\n"
        f"   ❌ Rejected: {deposits_rejected}\n"
        f"   💵 Total Accepted Amount: {total_deposit_amount:,.0f} SAR\n\n"
        f"💸 *Withdraw Stats:*\n   ✅ Accepted: {withdrawals_accepted}\n"
        f"   ❌ Rejected: {withdrawals_rejected}\n"
        f"   💵 Total Accepted Amount: {total_withdraw_amount:,.0f} SAR\n\n"
        f"📢 *Times shared bot:* {share_count}",
        parse_mode="Markdown",
        reply_markup=get_stats_menu_keyboard()
    )

# ============================================
# CASHBACK CALCULATOR
# ============================================

async def show_cashback_calculator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    admin_states[user_id] = {"action": "cashback", "step": "waiting_for_player_id"}
    await update.message.reply_text(
        "💰 *Player ID Cashback Calculator*\n\nStep 1/3: Enter the Player ID\n\n"
        "📝 *Example:* `123456789`\n\nType /cancel to cancel.",
        parse_mode="Markdown",
        reply_markup=get_back_to_menu_keyboard()
    )

async def process_cashback_player_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    player_id = update.message.text.strip()
    if not player_id.isdigit():
        await update.message.reply_text("❌ *Invalid Player ID!*\n\nPlease enter a numeric Player ID.", parse_mode="Markdown")
        return
    admin_states[user_id]["player_id"] = player_id
    admin_states[user_id]["step"] = "waiting_for_start_date"
    await update.message.reply_text(
        f"✅ Player ID: `{player_id}`\n\nStep 2/3: Enter the start date\n\n"
        "📝 *Format:* `YYYY-MM-DD`\n📌 *Example:* `2026-07-01`\n\nType /cancel to cancel.",
        parse_mode="Markdown",
        reply_markup=get_back_to_menu_keyboard()
    )

async def process_cashback_start_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    start_date = update.message.text.strip()
    try:
        datetime.strptime(start_date, "%Y-%m-%d")
    except ValueError:
        await update.message.reply_text("❌ *Invalid date format!*\n\nPlease use the format: `YYYY-MM-DD`", parse_mode="Markdown")
        return
    admin_states[user_id]["start_date"] = start_date
    admin_states[user_id]["step"] = "waiting_for_end_date"
    await update.message.reply_text(
        f"✅ Start Date: `{start_date}`\n\nStep 3/3: Enter the end date\n\n"
        "📝 *Format:* `YYYY-MM-DD`\n📌 *Example:* `2026-07-14`\n\nType /cancel to cancel.",
        parse_mode="Markdown",
        reply_markup=get_back_to_menu_keyboard()
    )

async def process_cashback_end_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    end_date = update.message.text.strip()
    try:
        datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        await update.message.reply_text("❌ *Invalid date format!*\n\nPlease use the format: `YYYY-MM-DD`", parse_mode="Markdown")
        return

    state = admin_states[user_id]
    player_id = state.get("player_id")
    start_date = state.get("start_date")
    deposits = load_deposits()
    withdrawals = load_withdrawals()

    total_deposits = 0
    deposits_count = 0
    for d in deposits.values():
        if d.get("player_id") == player_id and d.get("status") == "completed":
            created_at = d.get("created_at", "")
            if created_at:
                try:
                    created_date = created_at.split("T")[0] if "T" in created_at else created_at[:10]
                    if start_date <= created_date <= end_date:
                        total_deposits += d.get("amount", 0)
                        deposits_count += 1
                except:
                    pass

    total_withdrawals = 0
    withdrawals_count = 0
    for w in withdrawals.values():
        if w.get("player_id") == player_id and w.get("status") == "completed":
            created_at = w.get("created_at", "")
            if created_at:
                try:
                    created_date = created_at.split("T")[0] if "T" in created_at else created_at[:10]
                    if start_date <= created_date <= end_date:
                        total_withdrawals += w.get("amount", 0)
                        withdrawals_count += 1
                except:
                    pass

    net_amount = total_deposits - total_withdrawals
    cashback = net_amount * CASHBACK_PERCENT
    admin_states.pop(user_id, None)

    await update.message.reply_text(
        f"💰 *Cashback Calculation*\n\n🆔 Player ID: `{player_id}`\n"
        f"📅 Period: {start_date} to {end_date}\n\n"
        f"📊 *Summary:*\n   💳 Deposits Accepted: {deposits_count} ({total_deposits:,.0f} SAR)\n"
        f"   💸 Withdrawals Accepted: {withdrawals_count} ({total_withdrawals:,.0f} SAR)\n"
        f"   📊 Net Amount: {net_amount:,.0f} SAR\n\n"
        f"🎯 *Cashback ({int(CASHBACK_PERCENT*100)}%):* `{cashback:,.2f} SAR`\n\n"
        f"📌 *Formula:* {int(CASHBACK_PERCENT*100)}% × (Deposits - Withdrawals)",
        parse_mode="Markdown",
        reply_markup=get_stats_menu_keyboard()
    )

# ============================================
# ACCOUNT HANDLING
# ============================================

async def handle_get_account(update, user_id, used_data):
    today_count = get_user_today_count(user_id, used_data)
    if today_count >= 2:
        await update.message.reply_text(
            "❌ *Daily Limit Reached!*\n\n"
            f"You've already received *{today_count}* accounts today.\n"
            "Maximum is *2 accounts per day*.\n\n"
            "⏳ Please try again tomorrow.\n"
            "📋 Use 'My Accounts' to see your accounts.",
            parse_mode="Markdown",
            reply_markup=get_back_to_menu_keyboard()
        )
        return
    accounts = load_accounts()
    if not accounts:
        await update.message.reply_text(
            "❌ *No Accounts Available!*\n\nAll accounts have been distributed.\nPlease check back later or contact our agent.",
            parse_mode="Markdown",
            reply_markup=get_back_to_menu_keyboard()
        )
        return
    account = accounts.pop(0)
    save_accounts(accounts)
    today = datetime.now().strftime("%Y-%m-%d")
    username = update.effective_user.username or "NoUsername"
    update_user_data(user_id, username, {"account": account, "date": today, "timestamp": datetime.now().isoformat()})
    remaining = len(accounts)
    parts = account.split(":", 1)
    account_display = f"*Username:* `{parts[0]}`\n*Password:* `{parts[1]}`" if len(parts) == 2 else f"`{account}`"
    await update.message.reply_text(
        f"✅ *Account Assigned!*\n\n{account_display}\n\n💰 *30% CASHBACK on all losses!*\n\n"
        f"📊 *Today's Usage:* {get_user_today_count(user_id, used_data)}/2\n"
        f"📦 *Accounts Remaining:* {remaining}\n\n💡 *Tap to copy!*\n🔒 Save it securely.",
        parse_mode="Markdown",
        reply_markup=get_get_another_keyboard()
    )

async def handle_my_accounts(update, user_id, used_data):
    accounts = get_user_accounts(user_id, used_data)
    if not accounts:
        await update.message.reply_text("📋 *No Accounts Found*\n\nUse 'Get Account' to get your first one!", parse_mode="Markdown", reply_markup=get_back_to_menu_keyboard())
        return
    formatted = []
    for acc in accounts:
        parts = acc.split(":", 1)
        formatted.append(f"• *Username:* `{parts[0]}`\n  *Password:* `{parts[1]}`" if len(parts) == 2 else f"• `{acc}`")
    await update.message.reply_text(
        f"📋 *Your Accounts*\n\n{'\n\n'.join(formatted)}\n\n"
        f"📊 *Today's Usage:* {get_user_today_count(user_id, used_data)}/2\n"
        f"📦 *Total Accounts:* {len(accounts)}\n\n💰 *30% Cashback on all losses!*\n💡 *Tap any to copy*",
        parse_mode="Markdown",
        reply_markup=get_get_another_keyboard()
    )

# ============================================
# VIDEO TUTORIALS
# ============================================

async def show_video_tutorials(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    videos = load_videos()
    if user_id == ADMIN_ID:
        keyboard = get_admin_video_keyboard()
        await update.message.reply_text(
            f"📹 *Video Tutorials - Admin Panel*\n\n📊 Total Videos: {len(videos)}\n\n"
            "📹 *Add Video* - Add a new video tutorial\n"
            "🗑️ *Delete Video* - Remove a video\n"
            "📋 *List Videos* - View all videos\n\n👆 Select an option below:",
            parse_mode="Markdown",
            reply_markup=keyboard
        )
        return
    if not videos:
        await update.message.reply_text("📹 *No Videos Available*\n\nThere are no video tutorials yet.\nPlease check back later!", parse_mode="Markdown", reply_markup=get_back_to_menu_keyboard())
        return
    keyboard = get_video_menu_keyboard(videos)
    text = "📹 *Video Tutorials*\n\n" + "\n".join([f"🎬 {v['title']}" for v in videos.values()]) + "\n\n👆 Click a video to watch:"
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=keyboard)

async def handle_video_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    message_text = update.message.text if update.message.text else ""
    videos = load_videos()

    if message_text == "🔙 Back to Menu":
        admin_states.pop(user_id, None)
        await show_main_menu(update, context)
        return

    if message_text == "📹 Add Video":
        if update.effective_user.id != ADMIN_ID:
            await update.message.reply_text("⛔ *Unauthorized!*", parse_mode="Markdown")
            return
        admin_states[str(user_id)] = {"action": "add_video", "step": "waiting_for_video"}
        await update.message.reply_text(
            "📹 *Add Video Tutorial*\n\n📤 *Step 1/2:* Send me the video file\n\nType /cancel to cancel.",
            parse_mode="Markdown",
            reply_markup=get_back_to_menu_keyboard()
        )
        return

    if message_text == "🗑️ Delete Video":
        if update.effective_user.id != ADMIN_ID:
            await update.message.reply_text("⛔ *Unauthorized!*", parse_mode="Markdown")
            return
        if not videos:
            await update.message.reply_text("📭 *No videos to delete!*", parse_mode="Markdown")
            return
        keyboard = [[KeyboardButton(f"🗑️ {v['title']}")] for v in videos.values()] + [["🔙 Back to Menu"]]
        admin_states[user_id] = {"action": "delete_video", "step": "select"}
        await update.message.reply_text("🗑️ *Delete Video*\n\nSelect the video you want to delete:", parse_mode="Markdown", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        return

    if message_text == "📋 List Videos":
        if update.effective_user.id != ADMIN_ID:
            await update.message.reply_text("⛔ *Unauthorized!*", parse_mode="Markdown")
            return
        if not videos:
            await update.message.reply_text("📭 *No videos available.*", parse_mode="Markdown")
            return
        text = "📋 *Video List*\n\n" + "\n".join([f"🆔 ID: `{vid}`\n🎬 Title: {data['title']}\n📅 Added: {data.get('created_at', 'Unknown')}\n" for vid, data in videos.items()])
        await update.message.reply_text(text, parse_mode="Markdown")
        return

    if message_text.startswith("🗑️ "):
        if user_id in admin_states and admin_states[user_id].get("action") == "delete_video":
            title = message_text.replace("🗑️ ", "")
            for vid, data in videos.items():
                if data['title'] == title:
                    del videos[vid]
                    save_videos(videos)
                    admin_states.pop(user_id, None)
                    await update.message.reply_text(f"✅ *Video Deleted!*\n\nRemoved: {title}", parse_mode="Markdown", reply_markup=get_admin_video_keyboard())
                    return
            await update.message.reply_text(f"❌ *Video '{title}' not found!*", parse_mode="Markdown")
        return

    if message_text.startswith("🎬 "):
        title = message_text.replace("🎬 ", "")
        for data in videos.values():
            if data['title'] == title:
                try:
                    await update.message.reply_video(video=data['file_id'], caption=f"🎬 *{data['title']}*\n\n📹 Tutorial Video\n📅 Added: {data.get('created_at', 'Unknown')}", parse_mode="Markdown")
                    return
                except Exception as e:
                    print(f"Error sending video: {e}")
                    await update.message.reply_text("❌ *Error sending video!*", parse_mode="Markdown")
                    return
        await update.message.reply_text(f"❌ *Video '{title}' not found!*", parse_mode="Markdown")
        return

    # Add video state
    if user_id in admin_states and admin_states[user_id].get("action") == "add_video":
        state = admin_states[user_id]
        step = state.get("step")
        if step == "waiting_for_video":
            if update.message.video:
                state["file_id"] = update.message.video.file_id
                state["step"] = "waiting_for_title"
                await update.message.reply_text("✅ *Video Received!*\n\n📝 *Step 2/2:* Send me the title for this video\n\nType /cancel to cancel.", parse_mode="Markdown", reply_markup=get_back_to_menu_keyboard())
                return
            elif update.message.document and update.message.document.mime_type and update.message.document.mime_type.startswith('video/'):
                state["file_id"] = update.message.document.file_id
                state["step"] = "waiting_for_title"
                await update.message.reply_text("✅ *Video Received!*\n\n📝 *Step 2/2:* Send me the title for this video\n\nType /cancel to cancel.", parse_mode="Markdown", reply_markup=get_back_to_menu_keyboard())
                return
            else:
                await update.message.reply_text("❌ *Please send a video!*", parse_mode="Markdown")
                return
        elif step == "waiting_for_title":
            title = message_text.strip()
            if len(title) < 3:
                await update.message.reply_text("❌ *Title too short!*\n\nPlease enter at least 3 characters.", parse_mode="Markdown")
                return
            for data in videos.values():
                if data['title'].lower() == title.lower():
                    await update.message.reply_text(f"❌ *A video with title '{title}' already exists!*", parse_mode="Markdown")
                    return
            vid = f"VID_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            videos[vid] = {"title": title, "file_id": state.get("file_id"), "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            save_videos(videos)
            admin_states.pop(user_id, None)
            await update.message.reply_text(f"✅ *Video Added!*\n\n🎬 *Title:* {title}\n🆔 *ID:* `{vid}`\n📹 *Total Videos:* {len(videos)}", parse_mode="Markdown", reply_markup=get_admin_video_keyboard())

# ============================================
# DEPOSIT & WITHDRAW SYSTEM
# ============================================

async def show_deposit_withdraw_menu(update, context):
    await update.message.reply_text(
        "💳 *Deposit & Withdrawal*\n\n👇 *Select an option below:*",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup([["💰 Deposit", "💸 Withdraw"], ["🔙 Back to Menu"]], resize_keyboard=True)
    )

# --- Deposit Flow ---

async def start_deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    user_states[user_id] = {"action": "deposit", "step": "player_id"}
    await update.message.reply_text("💰 *Deposit Process*\n\nStep 1/4: Enter your Player ID\n\n📝 Please enter your 1xBet Player ID:", parse_mode="Markdown", reply_markup=get_back_to_menu_keyboard())

async def process_deposit_player_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    player_id = update.message.text.strip()
    if not player_id.isdigit():
        await update.message.reply_text("❌ *Invalid Player ID!*\n\nPlease enter a valid numeric Player ID.", parse_mode="Markdown")
        return
    user_states[user_id]["player_id"] = player_id
    user_states[user_id]["step"] = "method"
    methods = load_payment_methods()
    keyboard = [[KeyboardButton(m["name"])] for m in methods.values()] + [["🔙 Back to Menu"]]
    await update.message.reply_text(
        f"💰 *Deposit Process*\n\n✅ Player ID: `{player_id}`\n\nStep 2/4: Select payment method\n\nChoose your payment method:",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

async def process_deposit_method(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    method_name = update.message.text
    methods = load_payment_methods()
    method_key = None
    for key, method in methods.items():
        if method["name"] == method_name:
            method_key = key
            break
    if not method_key:
        await update.message.reply_text("❌ *Invalid method!*", parse_mode="Markdown")
        return
    user_states[user_id]["method"] = method_key
    user_states[user_id]["step"] = "amount"
    method = methods[method_key]
    details_text = "\n".join([f"📋 {field}: {value}" for field, value in method["details"].items()])
    keyboard = [
        ["10 SAR", "25 SAR", "50 SAR"],
        ["100 SAR", "200 SAR", "500 SAR"],
        ["✏️ Enter Custom Amount"],
        ["🔙 Back to Menu"]
    ]
    await update.message.reply_text(
        f"💰 *Deposit Process*\n\n✅ Player ID: `{user_states[user_id]['player_id']}`\n"
        f"✅ Method: {method_name}\n\n📋 *Send to:*\n{details_text}\n\n"
        "Step 3/4: Enter amount\n\nSelect an amount below or enter custom:",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

async def process_deposit_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    amount_text = update.message.text.replace(" SAR", "").strip()
    if amount_text == "✏️ Enter Custom Amount":
        await update.message.reply_text("📝 *Enter custom amount:*\n\nPlease enter the amount in SAR (10-500 SAR):", parse_mode="Markdown")
        return
    try:
        amount = float(amount_text)
        if amount < 10 or amount > 500:
            await update.message.reply_text(f"❌ *Amount must be between 10 and 500 SAR!*", parse_mode="Markdown")
            return
    except ValueError:
        await update.message.reply_text("❌ *Invalid amount!*\n\nPlease enter a valid number.", parse_mode="Markdown")
        return
    user_states[user_id]["amount"] = amount
    user_states[user_id]["step"] = "receipt"
    methods = load_payment_methods()
    method_name = methods[user_states[user_id]["method"]]["name"]
    await update.message.reply_text(
        f"💰 *Deposit Process*\n\n✅ Player ID: `{user_states[user_id]['player_id']}`\n"
        f"✅ Method: {method_name}\n✅ Amount: {amount} SAR\n\n"
        "Step 4/4: Send receipt\n\n📸 Please send a screenshot or photo of your transfer receipt.\n\n"
        "📌 *Instructions:*\n• Take a screenshot of the transfer confirmation\n• Send it as a photo to this chat\n\n"
        "⚠️ *Important:* The receipt must show:\n• The amount transferred\n• The recipient details\n• The transaction reference\n\nType /cancel to cancel.",
        parse_mode="Markdown"
    )

async def handle_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id not in user_states or user_states[user_id].get("action") != "deposit" or user_states[user_id].get("step") != "receipt":
        return
    if not update.message.photo:
        await update.message.reply_text("❌ *Please send a photo!*", parse_mode="Markdown")
        return
    photo = update.message.photo[-1]
    file = await photo.get_file()
    file_path = os.path.join(DATA_DIR, f"receipt_{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg")
    await file.download_to_drive(file_path)

    deposits = load_deposits()
    deposit_id = f"DEP_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    deposits[deposit_id] = {
        "user_id": user_id,
        "username": update.effective_user.username or "NoUsername",
        "player_id": user_states[user_id].get("player_id"),
        "method": user_states[user_id].get("method"),
        "amount": user_states[user_id].get("amount"),
        "receipt": file_path,
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }
    save_deposits(deposits)
    user_states[user_id] = {}
    await update.message.reply_text(
        "✅ *Receipt Received!*\n\n⏳ Please wait while our team verifies your transfer.\n\nYou will be notified once your deposit is confirmed.\n\n📞 For urgent inquiries, contact our agent.",
        parse_mode="Markdown",
        reply_markup=get_back_to_menu_keyboard()
    )
    await notify_accountant_deposit(update, context, deposit_id, deposits[deposit_id])

async def notify_accountant_deposit(update, context, deposit_id, deposit_data):
    methods = load_payment_methods()
    method_name = methods[deposit_data["method"]]["name"]
    keyboard = [
        [InlineKeyboardButton("✅ Accept", callback_data=f"deposit_accept_{deposit_id}"),
         InlineKeyboardButton("❌ Reject", callback_data=f"deposit_reject_{deposit_id}")]
    ]
    message = (
        f"💰 *New Deposit Request*\n\n"
        f"🆔 ID: {deposit_id}\n"
        f"👤 User: @{deposit_data['username']}\n"
        f"🆔 Player ID: {deposit_data['player_id']}\n"
        f"💳 Method: {method_name}\n"
        f"💵 Amount: {deposit_data['amount']} SAR\n"
        f"📅 Time: {deposit_data['created_at']}\n\n"
        f"Please verify the transfer and respond:"
    )
    await context.bot.send_message(chat_id=ACCOUNTANT_ID, text=message, parse_mode=None, reply_markup=InlineKeyboardMarkup(keyboard))
    if os.path.exists(deposit_data['receipt']):
        with open(deposit_data['receipt'], 'rb') as photo:
            await context.bot.send_photo(chat_id=ACCOUNTANT_ID, photo=photo, caption=f"📸 Receipt for Deposit {deposit_id}")

# --- Withdraw Flow ---

async def start_withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    user_states[user_id] = {"action": "withdraw", "step": "method"}
    methods = load_payment_methods()
    keyboard = [[KeyboardButton(m["name"])] for m in methods.values()] + [["🔙 Back to Menu"]]
    await update.message.reply_text(
        "💸 *Withdraw Process*\n\nStep 1/4: Select withdrawal method\n\nChoose your withdrawal method:",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

async def process_withdraw_method(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    method_name = update.message.text
    methods = load_payment_methods()
    method_key = None
    for key, method in methods.items():
        if method["name"] == method_name:
            method_key = key
            break
    if not method_key:
        await update.message.reply_text("❌ *Invalid method!*", parse_mode="Markdown")
        return
    user_states[user_id]["method"] = method_key
    user_states[user_id]["step"] = "player_id"
    await update.message.reply_text(
        f"💸 *Withdraw Process*\n\nStep 2/4: Enter your Player ID\n\n📝 Please enter your 1xBet Player ID:",
        parse_mode="Markdown",
        reply_markup=get_back_to_menu_keyboard()
    )

async def process_withdraw_player_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    player_id = update.message.text.strip()
    if not player_id.isdigit():
        await update.message.reply_text("❌ *Invalid Player ID!*\n\nPlease enter a valid numeric Player ID.", parse_mode="Markdown")
        return
    user_states[user_id]["player_id"] = player_id
    user_states[user_id]["step"] = "details"
    user_states[user_id]["details"] = {}
    fields = load_payment_methods()[user_states[user_id]["method"]]["fields"]
    user_states[user_id]["fields"] = fields
    user_states[user_id]["field_index"] = 0
    await ask_withdraw_field(update, context)

async def ask_withdraw_field(update, context):
    user_id = str(update.effective_user.id)
    state = user_states[user_id]
    fields = state["fields"]
    field_index = state["field_index"]
    if field_index >= len(fields):
        await ask_withdraw_code(update, context)
        return
    field = fields[field_index]
    await update.message.reply_text(
        f"💸 *Withdraw Process*\n\nStep 3/4: Enter your details\n\n📝 *{field}:*\n\nPlease enter your {field.lower()}:",
        parse_mode="Markdown",
        reply_markup=get_back_to_menu_keyboard()
    )

async def process_withdraw_field(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    value = update.message.text.strip()
    if user_id not in user_states:
        return
    state = user_states[user_id]
    field = state["fields"][state["field_index"]]
    state["details"][field] = value
    state["field_index"] += 1
    await ask_withdraw_field(update, context)

async def ask_withdraw_code(update, context):
    user_id = str(update.effective_user.id)
    state = user_states[user_id]
    state["step"] = "code"
    # Send withdrawal video if exists
    videos = load_videos()
    for data in videos.values():
        if "Withdrawal" in data['title'] or "withdrawal" in data['title'].lower():
            try:
                await update.message.reply_video(video=data['file_id'], caption=f"🎬 *{data['title']}*\n\n📹 Watch this tutorial for step-by-step instructions!", parse_mode="Markdown")
            except Exception as e:
                print(f"Error sending withdrawal video: {e}")
            break
    await update.message.reply_text(
        "💸 *Withdraw Process*\n\nStep 4/4: Enter withdrawal code\n\n"
        "📋 *How to get your withdrawal code:*\n\n"
        "1️⃣ Open 1xBet app\n"
        "2️⃣ Go to *Withdraw* section\n"
        "3️⃣ Scroll down and select *1xBet Cash*\n"
        "4️⃣ Enter amount, select:\n"
        "   - City: *Riyadh*\n"
        "   - Street: *ARVEA*\n"
        "5️⃣ Confirm the withdrawal\n"
        "6️⃣ Scroll up and find *Withdrawal Requests*\n"
        "7️⃣ Click *Get Code*\n\n"
        "📝 *Enter the code here:*\n\n"
        "Type /cancel to cancel.",
        parse_mode="Markdown",
        reply_markup=get_back_to_menu_keyboard()
    )

async def process_withdraw_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    code = update.message.text.strip()
    if user_id not in user_states or user_states[user_id].get("step") != "code":
        return
    state = user_states[user_id]
    withdrawals = load_withdrawals()
    withdraw_id = f"WTH_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    withdrawals[withdraw_id] = {
        "user_id": user_id,
        "username": update.effective_user.username or "NoUsername",
        "player_id": state.get("player_id"),
        "method": state.get("method"),
        "details": state.get("details", {}),
        "code": code,
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }
    save_withdrawals(withdrawals)
    user_states[user_id] = {}
    await update.message.reply_text(
        "✅ *Withdrawal Request Submitted!*\n\n⏳ Please wait while our team processes your request.\n\nYou will be notified once your withdrawal is confirmed.\n\n📞 For urgent inquiries, contact our agent.",
        parse_mode="Markdown",
        reply_markup=get_back_to_menu_keyboard()
    )
    await notify_accountant_withdraw(update, context, withdraw_id, withdrawals[withdraw_id])

async def notify_accountant_withdraw(update, context, withdraw_id, withdraw_data):
    try:
        methods = load_payment_methods()
        method_name = methods[withdraw_data["method"]]["name"]
        details_text = "\n".join([f"• {k}: {v}" for k, v in withdraw_data["details"].items()])
        keyboard = [
            [InlineKeyboardButton("✅ Accept", callback_data=f"withdraw_accept_{withdraw_id}"),
             InlineKeyboardButton("❌ Reject", callback_data=f"withdraw_reject_{withdraw_id}")]
        ]
        message = (
            f"💸 *New Withdrawal Request*\n\n"
            f"🆔 ID: {withdraw_id}\n"
            f"👤 User: @{withdraw_data['username']}\n"
            f"🆔 Player ID: {withdraw_data.get('player_id', 'N/A')}\n"
            f"💳 Method: {method_name}\n"
            f"📋 User Details:\n{details_text}\n"
            f"🔑 Withdrawal Code: {withdraw_data['code']}\n"
            f"📅 Time: {withdraw_data['created_at']}\n\n"
            f"Please verify and respond:"
        )
        await context.bot.send_message(chat_id=ACCOUNTANT_ID, text=message, parse_mode=None, reply_markup=InlineKeyboardMarkup(keyboard))
        print(f"✅ Withdrawal notification sent for ID: {withdraw_id}")
    except Exception as e:
        print(f"❌ Error sending withdrawal notification: {e}")
        import traceback
        traceback.print_exc()

# ============================================
# ACCOUNTANT HANDLERS
# ============================================

async def handle_accountant_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    parts = data.split("_")
    action = parts[1]
    type_ = parts[0]
    request_id = "_".join(parts[2:])

    if type_ == "deposit":
        deposits = load_deposits()
        if request_id not in deposits:
            await query.edit_message_text("❌ Deposit request not found!")
            return
        if action == "accept":
            deposits[request_id]["status"] = "completed"
            save_deposits(deposits)
            user_id = deposits[request_id]["user_id"]
            await context.bot.send_message(
                chat_id=user_id,
                text=f"✅ *Your deposit has been confirmed!*\n\n💰 Amount: {deposits[request_id]['amount']} SAR\n🎉 Funds have been added to your 1xBet account!",
                parse_mode="Markdown"
            )
            await query.edit_message_text("✅ Deposit accepted!")
        else:
            context.user_data["reject_deposit"] = request_id
            await query.edit_message_text(f"❌ *Reject Deposit*\n\nRequest ID: `{request_id}`\n\nPlease send the reason for rejection:", parse_mode="Markdown")

    elif type_ == "withdraw":
        withdrawals = load_withdrawals()
        if request_id not in withdrawals:
            await query.edit_message_text("❌ Withdrawal request not found!")
            return
        if action == "accept":
            # ✅ Set the admin state for amount entry
            admin_states[str(update.effective_user.id)] = {
                "action": "withdraw_amount",
                "withdraw_id": request_id
            }
            print(f"🔍 DEBUG: Set admin state for user {update.effective_user.id}: {admin_states[str(update.effective_user.id)]}")
            await query.edit_message_text(
                f"✅ *Accept Withdrawal*\n\nRequest ID: `{request_id}`\n\nPlease enter the withdrawal amount in SAR:",
                parse_mode="Markdown"
            )
        else:
            context.user_data["reject_withdraw"] = request_id
            await query.edit_message_text(f"❌ *Reject Withdrawal*\n\nRequest ID: `{request_id}`\n\nPlease send the reason for rejection:", parse_mode="Markdown")

async def process_withdraw_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"🔍 DEBUG: process_withdraw_amount called with text: {update.message.text}")
    user_id = str(update.effective_user.id)
    amount_text = update.message.text.strip()

    try:
        amount = float(amount_text)
        if amount <= 0:
            raise ValueError
    except ValueError:
        await update.message.reply_text("❌ *Invalid amount!*\n\nPlease enter a valid positive number.", parse_mode="Markdown")
        return

    state = admin_states.get(user_id)
    if not state or state.get("action") != "withdraw_amount":
        await update.message.reply_text("❌ *Session expired!*\n\nPlease try accepting the withdrawal again.", parse_mode="Markdown")
        return

    withdraw_id = state.get("withdraw_id")
    withdrawals = load_withdrawals()
    if withdraw_id not in withdrawals:
        await update.message.reply_text("❌ *Withdrawal request not found!*", parse_mode="Markdown")
        admin_states.pop(user_id, None)
        return

    withdrawals[withdraw_id]["amount"] = amount
    withdrawals[withdraw_id]["status"] = "completed"
    save_withdrawals(withdrawals)
    admin_states.pop(user_id, None)

    user_id_user = withdrawals[withdraw_id]["user_id"]
    await context.bot.send_message(
        chat_id=user_id_user,
        text=f"✅ *Your withdrawal has been processed!*\n\n💰 Amount: {amount:,.0f} SAR\n💸 Funds have been sent to your selected method.",
        parse_mode="Markdown"
    )
    await update.message.reply_text(
        f"✅ *Withdrawal accepted!*\n\nRequest ID: `{withdraw_id}`\nAmount: {amount:,.0f} SAR",
        parse_mode="Markdown"
    )

async def process_rejection_reason(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "reject_deposit" in context.user_data:
        request_id = context.user_data.pop("reject_deposit")
        deposits = load_deposits()
        if request_id in deposits and update.message.text:
            reason = update.message.text
            deposits[request_id]["status"] = "rejected"
            deposits[request_id]["reason"] = reason
            save_deposits(deposits)
            user_id = deposits[request_id]["user_id"]
            await context.bot.send_message(
                chat_id=user_id,
                text=f"❌ *Deposit Rejected!*\n\n💰 Amount: {deposits[request_id]['amount']} SAR\n\n📋 *Reason:*\n{reason}",
                parse_mode="Markdown"
            )
            await update.message.reply_text("✅ Rejection reason sent to user.", reply_markup=get_pm_menu_keyboard() if update.effective_user.id == ADMIN_ID else get_main_menu_keyboard())
            return True
        else:
            await update.message.reply_text("❌ *Please send a text reason for rejection.*", parse_mode="Markdown")
            return True

    if "reject_withdraw" in context.user_data:
        request_id = context.user_data.pop("reject_withdraw")
        withdrawals = load_withdrawals()
        if request_id in withdrawals and update.message.text:
            reason = update.message.text
            withdrawals[request_id]["status"] = "rejected"
            withdrawals[request_id]["reason"] = reason
            save_withdrawals(withdrawals)
            user_id = withdrawals[request_id]["user_id"]
            await context.bot.send_message(
                chat_id=user_id,
                text=f"❌ *Withdrawal Rejected!*\n\n📋 *Reason:*\n{reason}",
                parse_mode="Markdown"
            )
            await update.message.reply_text("✅ Rejection reason sent to user.", reply_markup=get_pm_menu_keyboard() if update.effective_user.id == ADMIN_ID else get_main_menu_keyboard())
            return True
        else:
            await update.message.reply_text("❌ *Please send a text reason for rejection.*", parse_mode="Markdown")
            return True

    return False

# ============================================
# PAYMENT METHODS MANAGEMENT
# ============================================

async def manage_payment_methods(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ *Unauthorized!*", parse_mode="Markdown")
        return
    admin_states.pop(str(update.effective_user.id), None)
    await update.message.reply_text("📋 *Payment Methods Management*\n\nSelect an option below:", parse_mode="Markdown", reply_markup=get_pm_menu_keyboard())

async def handle_pm_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    message_text = update.message.text
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ *Unauthorized!*", parse_mode="Markdown")
        return
    if user_id in admin_states:
        await handle_pm_state(update, context)
        return
    methods = load_payment_methods()

    if message_text == "📋 List Methods":
        if not methods:
            await update.message.reply_text("📭 *No payment methods available.*", parse_mode="Markdown")
            return
        text = "📋 *Payment Methods*\n\n"
        for key, method in methods.items():
            details = "\n".join([f"   📋 {f}: {v}" for f, v in method["details"].items()])
            text += f"🔹 *{method['name']}*\n   📌 ID: `{key}`\n   📝 Fields: {', '.join(method['fields'])}\n{details}\n\n"
        await update.message.reply_text(text, parse_mode="Markdown")
        return

    elif message_text == "➕ Add Method":
        admin_states[user_id] = {"action": "add", "step": "key"}
        await update.message.reply_text(
            "➕ *Add Payment Method*\n\nStep 1/6: Enter a unique ID\n\n📝 *Example:* `barq`, `newpay`\n\nType /cancel to cancel.",
            parse_mode="Markdown",
            reply_markup=get_back_to_menu_keyboard()
        )
        return

    elif message_text == "✏️ Edit Method":
        if not methods:
            await update.message.reply_text("📭 *No payment methods to edit.*", parse_mode="Markdown")
            return
        keyboard = [[KeyboardButton(key)] for key in methods.keys()] + [["🔙 Back to Menu"]]
        admin_states[user_id] = {"action": "edit", "step": "select"}
        await update.message.reply_text("✏️ *Edit Payment Method*\n\nSelect the method you want to edit:", parse_mode="Markdown", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        return

    elif message_text == "🗑️ Delete Method":
        if not methods:
            await update.message.reply_text("📭 *No payment methods to delete.*", parse_mode="Markdown")
            return
        keyboard = [[KeyboardButton(key)] for key in methods.keys()] + [["🔙 Back to Menu"]]
        admin_states[user_id] = {"action": "delete", "step": "select"}
        await update.message.reply_text("🗑️ *Delete Payment Method*\n\nSelect the method you want to delete:", parse_mode="Markdown", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        return

async def handle_pm_state(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    message_text = update.message.text
    state = admin_states[user_id]
    action = state.get("action")
    step = state.get("step")
    methods = load_payment_methods()

    if message_text in ["🔙 Back to Menu", "/cancel"]:
        admin_states.pop(user_id, None)
        await update.message.reply_text("❌ *Cancelled!*", parse_mode="Markdown", reply_markup=get_pm_menu_keyboard())
        return

    if action == "add":
        if step == "key":
            if not re.match(r'^[a-zA-Z0-9_]+$', message_text):
                await update.message.reply_text("❌ *Invalid ID!*\n\nUse only letters, numbers, and underscores.", parse_mode="Markdown")
                return
            if message_text in methods:
                await update.message.reply_text(f"❌ *ID `{message_text}` already exists!*", parse_mode="Markdown")
                return
            state["key"] = message_text
            state["step"] = "name"
            await update.message.reply_text(f"✅ ID: `{message_text}`\n\nStep 2/6: Enter the display name\n\n📝 *Example:* `💳 Barq Wallet`", parse_mode="Markdown", reply_markup=get_back_to_menu_keyboard())
            return
        elif step == "name":
            state["name"] = message_text
            state["step"] = "fields_count"
            await update.message.reply_text(
                f"✅ Name: {message_text}\n\nStep 3/6: How many fields does this method need?\n\n"
                "📝 *Examples:*\n• Barq: 1 field (phone_number)\n• Bank Transfer: 2 fields (phone_number, iban)\n\nChoose a number:",
                parse_mode="Markdown",
                reply_markup=ReplyKeyboardMarkup([["1", "2", "3"], ["4", "5"], ["🔙 Back to Menu"]], resize_keyboard=True)
            )
            return
        elif step == "fields_count":
            try:
                count = int(message_text)
                if count < 1 or count > 5:
                    raise ValueError
                state["fields_count"] = count
                state["fields"] = []
                state["field_index"] = 0
                state["step"] = "fields"
                field_labels = {0: "📱 Phone number", 1: "🏦 IBAN", 2: "🏛️ Bank name", 3: "🔗 Wallet address", 4: "👤 Full name", 5: "📧 Email"}
                await update.message.reply_text(
                    f"✅ {count} fields selected.\n\nStep 4/6: Enter field #{state['field_index'] + 1}\n\n"
                    f"📝 *Examples:* {field_labels.get(0, '')}\n\nEnter the field name:",
                    parse_mode="Markdown",
                    reply_markup=get_back_to_menu_keyboard()
                )
                return
            except ValueError:
                await update.message.reply_text("❌ *Invalid number!*\n\nPlease enter a number between 1 and 5.", parse_mode="Markdown")
                return
        elif step == "fields":
            field = message_text.strip()
            state["fields"].append(field)
            state["field_index"] += 1
            if state["field_index"] >= state["fields_count"]:
                state["step"] = "value_fields"
                state["value_index"] = 0
                state["values"] = {}
                await update.message.reply_text(
                    f"✅ Fields added: {', '.join(state['fields'])}\n\nStep 5/6: Enter values for each field\n\n📝 Enter value for *{state['fields'][0]}*:",
                    parse_mode="Markdown",
                    reply_markup=get_back_to_menu_keyboard()
                )
                return
            field_labels = {0: "📱 Phone number", 1: "🏦 IBAN", 2: "🏛️ Bank name", 3: "🔗 Wallet address", 4: "👤 Full name", 5: "📧 Email"}
            await update.message.reply_text(
                f"✅ Field #{state['field_index']}: `{field}`\n\nEnter field #{state['field_index'] + 1}\n\n"
                f"📝 *Examples:* {field_labels.get(state['field_index'], '')}",
                parse_mode="Markdown",
                reply_markup=get_back_to_menu_keyboard()
            )
            return
        elif step == "value_fields":
            field = state["fields"][state["value_index"]]
            state["values"][field] = message_text
            state["value_index"] += 1
            if state["value_index"] >= len(state["fields"]):
                key = state["key"]
                methods[key] = {"name": state["name"], "fields": state["fields"], "details": state["values"]}
                save_payment_methods(methods)
                admin_states.pop(user_id, None)
                await update.message.reply_text(
                    f"✅ *Payment Method Added!*\n\n🔹 Name: {state['name']}\n📌 ID: `{key}`\n"
                    f"📝 Fields: {', '.join(state['fields'])}\n📋 Values:\n" + "\n".join([f"   {f}: {v}" for f, v in state["values"].items()]),
                    parse_mode="Markdown",
                    reply_markup=get_pm_menu_keyboard()
                )
                return
            await update.message.reply_text(
                f"📝 Enter value for *{state['fields'][state['value_index']]}*:",
                parse_mode="Markdown",
                reply_markup=get_back_to_menu_keyboard()
            )
            return

    # EDIT METHOD FLOW
    elif action == "edit":
        if step == "select":
            if message_text not in methods:
                await update.message.reply_text(f"❌ *Method `{message_text}` not found!*", parse_mode="Markdown")
                return
            state["edit_key"] = message_text
            state["step"] = "field"
            method = methods[message_text]
            keyboard = [[KeyboardButton(f)] for f in ["name", "fields", "details"] + list(method["details"].keys())] + [["🔙 Back to Menu"]]
            await update.message.reply_text(
                f"✏️ *Editing: {method['name']}*\n\n📌 ID: `{message_text}`\n"
                f"📝 Fields: {', '.join(method['fields'])}\n📋 Details: {method['details']}\n\nSelect which field to edit:",
                parse_mode="Markdown",
                reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            )
            return
        elif step == "field":
            if message_text not in ["name", "fields", "details"] and message_text not in methods[state["edit_key"]]["details"]:
                await update.message.reply_text(f"❌ *Field `{message_text}` not found!*", parse_mode="Markdown")
                return
            state["edit_field"] = message_text
            state["step"] = "value"
            current = methods[state["edit_key"]].get(message_text, "N/A")
            await update.message.reply_text(f"✏️ *Editing: {state['edit_field']}*\n\nCurrent value: `{current}`\n\nEnter the new value:", parse_mode="Markdown", reply_markup=get_back_to_menu_keyboard())
            return
        elif step == "value":
            key = state["edit_key"]
            field = state["edit_field"]
            if field == "fields":
                fields = [f.strip() for f in message_text.replace(",", " ").split() if f.strip()]
                if fields:
                    methods[key]["fields"] = fields
                else:
                    await update.message.reply_text("❌ *Invalid fields!*", parse_mode="Markdown")
                    return
            elif field == "details":
                await update.message.reply_text("❌ *To edit details, edit individual fields.*", parse_mode="Markdown")
                return
            else:
                methods[key][field] = message_text
            save_payment_methods(methods)
            admin_states.pop(user_id, None)
            await update.message.reply_text(f"✅ *Method Updated!*\n\n📌 ID: `{key}`\n📝 {field}: {message_text}", parse_mode="Markdown", reply_markup=get_pm_menu_keyboard())
            return

    # DELETE METHOD FLOW
    elif action == "delete":
        if step == "select":
            if message_text not in methods:
                await update.message.reply_text(f"❌ *Method `{message_text}` not found!*", parse_mode="Markdown")
                return
            state["delete_key"] = message_text
            state["step"] = "confirm"
            method = methods[message_text]
            await update.message.reply_text(
                f"🗑️ *Delete Method?*\n\n🔹 Name: {method['name']}\n📌 ID: `{message_text}`\n\n⚠️ *Are you sure?*\nThis action cannot be undone!",
                parse_mode="Markdown",
                reply_markup=ReplyKeyboardMarkup([["✅ Yes, Delete"], ["❌ No, Cancel"]], resize_keyboard=True)
            )
            return
        elif step == "confirm":
            if message_text == "✅ Yes, Delete":
                key = state["delete_key"]
                del methods[key]
                save_payment_methods(methods)
                admin_states.pop(user_id, None)
                await update.message.reply_text(f"✅ *Method `{key}` deleted!*", parse_mode="Markdown", reply_markup=get_pm_menu_keyboard())
            else:
                admin_states.pop(user_id, None)
                await update.message.reply_text("❌ *Deletion cancelled!*", parse_mode="Markdown", reply_markup=get_pm_menu_keyboard())
            return

# ============================================
# ADMIN COMMANDS
# ============================================

async def add_account_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ *Unauthorized!*", parse_mode="Markdown")
        return
    if not context.args:
        await update.message.reply_text(
            "📝 *How to add an account:*\n\n`/ass Username: 123456789 Password: abcd1234`\n\n"
            "**Example:**\n`/ass Username: Ahmed_123 Password: SecurePass456`\n\n"
            "You can also add multiple:\n`/ass Username: user1 Password: pass1, Username: user2 Password: pass2`",
            parse_mode="Markdown"
        )
        return
    text = " ".join(context.args)
    pattern = r'Username:\s*([^,]+?)\s*Password:\s*([^,]+?)(?:,|$)'
    matches = re.findall(pattern, text, re.IGNORECASE)
    if not matches:
        accounts_input = text.split(",")
        new_accounts = [acc.strip() for acc in accounts_input if ":" in acc]
        if new_accounts:
            matches = [(acc.split(":", 1)[0].strip(), acc.split(":", 1)[1].strip()) for acc in new_accounts]
        else:
            await update.message.reply_text("❌ *Invalid format!*\n\nUse:\n`/ass Username: Ahmed Password: 123456`", parse_mode="Markdown")
            return
    new_accounts = []
    for username, password in matches:
        username = username.strip()
        password = password.strip()
        if username and password:
            new_accounts.append(f"{username}:{password}")
    if not new_accounts:
        await update.message.reply_text("❌ *No valid accounts found!*", parse_mode="Markdown")
        return
    current_accounts = load_accounts()
    current_accounts.extend(new_accounts)
    save_accounts(current_accounts)
    added_text = "\n".join([f"• *Username:* `{u.split(':',1)[0]}`\n   *Password:* `{u.split(':',1)[1]}`" for u in new_accounts])
    await update.message.reply_text(f"✅ *Added {len(new_accounts)} account(s)!*\n\n{added_text}\n\n📦 *Total Available:* {len(current_accounts)}\n💰 *All accounts get 30% cashback!*", parse_mode="Markdown")

async def list_accounts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ *Unauthorized!*", parse_mode="Markdown")
        return
    accounts = load_accounts()
    if not accounts:
        await update.message.reply_text("📭 *No accounts available.*", parse_mode="Markdown")
        return
    formatted = []
    for i, acc in enumerate(accounts):
        parts = acc.split(":", 1)
        formatted.append(f"{i+1}. *Username:* `{parts[0]}`\n   *Password:* `{parts[1]}`" if len(parts) == 2 else f"{i+1}. `{acc}`")
    await update.message.reply_text(f"📋 *Available Accounts ({len(accounts)})*\n\n{'\n\n'.join(formatted)}\n\n💰 *30% Cashback on all losses!*", parse_mode="Markdown")

async def delete_account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ *Unauthorized!*", parse_mode="Markdown")
        return
    if not context.args:
        await update.message.reply_text("📝 `/del Username: player1`", parse_mode="Markdown")
        return
    match = re.search(r'Username:\s*([^,]+)', " ".join(context.args), re.IGNORECASE)
    if not match:
        await update.message.reply_text("❌ *Invalid format!*\n\nUse: `/del Username: player1`", parse_mode="Markdown")
        return
    username = match.group(1).strip()
    accounts = load_accounts()
    account_to_delete = next((a for a in accounts if a.startswith(f"{username}:")), None)
    if not account_to_delete:
        await update.message.reply_text(f"❌ *Account with username `{username}` not found!*", parse_mode="Markdown")
        return
    accounts.remove(account_to_delete)
    save_accounts(accounts)
    await update.message.reply_text(f"✅ *Account Deleted!*\n\nRemoved: `{account_to_delete}`\n📦 *Total Available:* {len(accounts)}", parse_mode="Markdown")

async def clear_accounts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ *Unauthorized!*", parse_mode="Markdown")
        return
    accounts = load_accounts()
    if not accounts:
        await update.message.reply_text("📭 *No accounts to clear!*", parse_mode="Markdown")
        return
    count = len(accounts)
    save_accounts([])
    await update.message.reply_text(f"🗑️ *Cleared {count} account(s)!*\n\n📦 *Total Available:* 0", parse_mode="Markdown")

async def reset_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ *Unauthorized!*", parse_mode="Markdown")
        return
    if not context.args:
        await update.message.reply_text("📝 Usage: `/resetuser user_id`", parse_mode="Markdown")
        return
    target_user = context.args[0]
    used_data = load_used()
    if target_user in used_data:
        del used_data[target_user]
        save_used(used_data)
        await update.message.reply_text(f"✅ *User {target_user} has been reset!*", parse_mode="Markdown")
    else:
        await update.message.reply_text(f"❌ *User {target_user} not found.*", parse_mode="Markdown")

# ============================================
# MAIN FUNCTION
# ============================================

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ass", add_account_command))
    app.add_handler(CommandHandler("add", add_account_command))
    app.add_handler(CommandHandler("stats", show_stats_menu))
    app.add_handler(CommandHandler("listaccounts", list_accounts))
    app.add_handler(CommandHandler("resetuser", reset_user))
    app.add_handler(CommandHandler("del", delete_account))
    app.add_handler(CommandHandler("clearaccounts", clear_accounts))
    app.add_handler(CommandHandler("pm", manage_payment_methods))

    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_message))
    app.add_handler(MessageHandler(filters.VIDEO, handle_message))  # Video is handled inside handle_message
    app.add_handler(MessageHandler(filters.Document.VIDEO, handle_message))  # Same for documents

    print("=" * 50)
    print("🤖 Saudi 1xBet Bot is RUNNING!")
    print("📱 Bot username: @Saudi_1xBet_bot")
    print("=" * 50)
    print("✅ Waiting for users...")
    print("Press Ctrl+C to stop the bot")
    print("=" * 50)

    app.run_polling()

if __name__ == "__main__":
    main()
