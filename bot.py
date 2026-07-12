import socket
socket.setdefaulttimeout(30)

# Force IPv4
import requests
requests.packages.urllib3.util.connection.HAS_IPV6 = False

import os
import json
import re
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ============================================
# CONFIGURATION - CHANGE THESE!
# ============================================
BOT_TOKEN = "8978819633:AAF9si6gH_sqvxC4uExZdwIK0gSkx8ToLq8"  # Your token
ADMIN_ID = 6012442109  # Your Telegram ID
AGENT_USERNAME = "@Saudi_1xbet_agent"  # Your agent's Telegram username

# ============================================
# DATA DIRECTORY - For persistent storage on Railway
# ============================================
if os.path.exists("/app/data"):
    DATA_DIR = "/app/data"
else:
    DATA_DIR = "."

ACCOUNTS_FILE = os.path.join(DATA_DIR, "accounts.json")
USED_FILE = os.path.join(DATA_DIR, "used_accounts.json")

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

# ============================================
# HELPER FUNCTIONS
# ============================================
def get_user_today_count(user_id, used_data):
    if user_id not in used_data:
        return 0
    today = datetime.now().strftime("%Y-%m-%d")
    today_count = 0
    for entry in used_data[user_id]:
        if entry.get("date") == today:
            today_count += 1
    return today_count

def get_user_accounts(user_id, used_data):
    if user_id not in used_data:
        return []
    return [entry["account"] for entry in used_data[user_id]]

def get_main_menu_keyboard():
    """Return the main menu keyboard"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎰 Get Account", callback_data="get_account"),
            InlineKeyboardButton("💬 Talk to Agent", callback_data="talk_agent")
        ],
        [
            InlineKeyboardButton("📋 My Accounts", callback_data="my_accounts")
        ]
    ])

def get_back_to_menu_keyboard():
    """Return a single button to go back to menu"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")]
    ])

def get_action_message(action_name):
    """Return the action message that shows what the user clicked"""
    action_messages = {
        "get_account": "🎰 Get Account",
        "talk_agent": "💬 Talk to Agent",
        "my_accounts": "📋 My Accounts",
        "back_to_menu": "🔙 Back to Menu"
    }
    return action_messages.get(action_name, "🔄 Action")

# ============================================
# MAIN BOT COMMANDS
# ============================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Check if the user is a member of your channel
    is_member = await is_user_member(user_id, "saudi_1xbet_accounts", context)
    
    if not is_member:
        keyboard = [
            [InlineKeyboardButton("📢 Join Our Channel", url="https://t.me/saudi_1xbet_accounts")],
            [InlineKeyboardButton("✅ I've Joined! Check Subscription", callback_data="check_subscription")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "👋 *Welcome!*\n\n"
            "To use this bot, you must first join our channel:\n"
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
        if chat_member.status in ["member", "administrator", "creator"]:
            return True
        return False
    except Exception as e:
        print(f"Error checking membership: {e}")
        return False

async def show_main_menu(update, context):
    """Display the main menu with account options."""
    keyboard = get_main_menu_keyboard()
    
    # Always send a NEW message
    await update.message.reply_text(
        "🎰 *Welcome to Saudi 1xBet Bot!*\n\n"
        "💰 *Get 30% CASHBACK on all losses!*\n"
        "📌 You can get up to *3 accounts per day*\n\n"
        "💡 Click the buttons below:",
        parse_mode="Markdown",
        reply_markup=keyboard
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # Get the user who clicked
    user_id = str(query.from_user.id)
    used_data = load_used()
    
    # Get the action name for the message
    action_name = query.data
    action_message = get_action_message(action_name)

    # FIRST: Send the user's action as a text message (like they typed it)
    await query.message.reply_text(f"👉 *{action_message}*", parse_mode="Markdown")

    # Handle "Back to Menu"
    if query.data == "back_to_menu":
        await query.message.reply_text(
            "🎰 *Welcome to Saudi 1xBet Bot!*\n\n"
            "💰 *Get 30% CASHBACK on all losses!*\n"
            "📌 You can get up to *3 accounts per day*\n\n"
            "💡 Click the buttons below:",
            parse_mode="Markdown",
            reply_markup=get_main_menu_keyboard()
        )
        return

    if query.data == "check_subscription":
        user_id = query.from_user.id
        is_member = await is_user_member(user_id, "saudi_1xbet_accounts", context)
        if is_member:
            await query.message.reply_text(
                "✅ Subscription verified! Welcome!",
                reply_markup=get_main_menu_keyboard()
            )
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
    
    if query.data == "get_account":
        await handle_get_account(query, user_id, used_data)
    elif query.data == "talk_agent":
        await query.message.reply_text(
            f"💬 *Contact Our Agent*\n\n"
            f"📞 Reach out to *{AGENT_USERNAME}* for:\n"
            "• Account issues\n"
            "• Technical support\n"
            "• Questions about 1xBet\n"
            "• Cashback inquiries\n\n"
            f"👉 Click here: https://t.me/*Saudi_1xbet_agent*",
            parse_mode="Markdown",
            reply_markup=get_back_to_menu_keyboard()
        )
    elif query.data == "my_accounts":
        await handle_my_accounts(query, user_id, used_data)

async def handle_get_account(query, user_id, used_data):
    today_count = get_user_today_count(user_id, used_data)
    
    if today_count >= 3:
        await query.message.reply_text(
            "❌ *Daily Limit Reached!*\n\n"
            f"You've already received *{today_count}* accounts today.\n"
            "Maximum is *3 accounts per day*.\n\n"
            "⏳ Please try again tomorrow.\n"
            "📋 Use 'My Accounts' to see your accounts.",
            parse_mode="Markdown",
            reply_markup=get_back_to_menu_keyboard()
        )
        return
    
    accounts = load_accounts()
    
    if not accounts:
        await query.message.reply_text(
            "❌ *No Accounts Available!*\n\n"
            "All accounts have been distributed.\n"
            "Please check back later or contact our agent.",
            parse_mode="Markdown",
            reply_markup=get_back_to_menu_keyboard()
        )
        return
    
    account = accounts.pop(0)
    save_accounts(accounts)
    
    today = datetime.now().strftime("%Y-%m-%d")
    if user_id not in used_data:
        used_data[user_id] = []
    
    used_data[user_id].append({
        "account": account,
        "date": today,
        "timestamp": datetime.now().isoformat()
    })
    save_used(used_data)
    
    remaining = len(accounts)
    
    # Format the account nicely
    parts = account.split(":", 1)
    if len(parts) == 2:
        username, password = parts
        account_display = f"*Username:* `{username}`\n*Password:* `{password}`"
    else:
        account_display = f"`{account}`"
    
    # Keyboard with Get Another, My Accounts, and Back to Menu
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎰 Get Another", callback_data="get_account"),
            InlineKeyboardButton("📋 My Accounts", callback_data="my_accounts")
        ],
        [
            InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")
        ]
    ])
    
    await query.message.reply_text(
        f"✅ *Account Assigned!*\n\n"
        f"{account_display}\n\n"
        f"💰 *30% CASHBACK on all losses!*\n\n"
        f"📊 *Today's Usage:* {get_user_today_count(user_id, used_data)}/3\n"
        f"📦 *Accounts Remaining:* {remaining}\n\n"
        f"💡 *Tap to copy!*\n"
        f"🔒 Save it securely.",
        parse_mode="Markdown",
        reply_markup=keyboard
    )

async def handle_my_accounts(query, user_id, used_data):
    accounts = get_user_accounts(user_id, used_data)
    
    if not accounts:
        await query.message.reply_text(
            "📋 *No Accounts Found*\n\n"
            "You haven't received any accounts yet.\n"
            "Use 'Get Account' to get your first one!",
            parse_mode="Markdown",
            reply_markup=get_back_to_menu_keyboard()
        )
        return
    
    formatted_accounts = []
    for acc in accounts:
        acc_parts = acc.split(":", 1)
        if len(acc_parts) == 2:
            username, password = acc_parts
            formatted_accounts.append(f"• *Username:* `{username}`\n  *Password:* `{password}`")
        else:
            formatted_accounts.append(f"• `{acc}`")
    
    account_list = "\n\n".join(formatted_accounts)
    today_count = get_user_today_count(user_id, used_data)
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎰 Get Another", callback_data="get_account")],
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")]
    ])
    
    await query.message.reply_text(
        f"📋 *Your Accounts*\n\n"
        f"{account_list}\n\n"
        f"📊 *Today's Usage:* {today_count}/3\n"
        f"📦 *Total Accounts:* {len(accounts)}\n\n"
        f"💰 *30% Cashback on all losses!*\n"
        f"💡 *Tap any to copy*",
        parse_mode="Markdown",
        reply_markup=keyboard
    )

# ============================================
# ADMIN COMMANDS
# ============================================

async def add_account_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ *Unauthorized!*", parse_mode="Markdown")
        return
    
    if not context.args:
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
    
    text = " ".join(context.args)
    pattern = r'Username:\s*([^,]+?)\s*Password:\s*([^,]+?)(?:,|$)'
    matches = re.findall(pattern, text, re.IGNORECASE)
    
    if not matches:
        accounts_input = text.split(",")
        new_accounts = [acc.strip() for acc in accounts_input if ":" in acc]
        if new_accounts:
            matches = [(acc.split(":", 1)[0].strip(), acc.split(":", 1)[1].strip()) for acc in new_accounts]
        else:
            await update.message.reply_text(
                "❌ *Invalid format!*\n\n"
                "Use:\n"
                "`/ass Username: Ahmed Password: 123456`\n\n"
                "Or:\n"
                "`/ass user1:pass1, user2:pass2`",
                parse_mode="Markdown"
            )
            return
    
    new_accounts = []
    for username, password in matches:
        username = username.strip()
        password = password.strip()
        if username and password:
            new_accounts.append(f"{username}:{password}")
    
    if not new_accounts:
        await update.message.reply_text(
            "❌ *No valid accounts found!*\n\n"
            "Use format:\n"
            "`/ass Username: Ahmed Password: 123456`",
            parse_mode="Markdown"
        )
        return
    
    current_accounts = load_accounts()
    current_accounts.extend(new_accounts)
    save_accounts(current_accounts)

    added_display = []
    for acc in new_accounts:
        parts = acc.split(":", 1)
        if len(parts) == 2:
            added_display.append(f"• *Username:* `{parts[0]}`\n   *Password:* `{parts[1]}`")

    added_text = "\n\n".join(added_display)

    await update.message.reply_text(
        f"✅ *Added {len(new_accounts)} account(s)!*\n\n"
        f"{added_text}\n\n"
        f"📦 *Total Available:* {len(current_accounts)}\n"
        f"💰 *All accounts get 30% cashback!*",
        parse_mode="Markdown"
    )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ *Unauthorized!*", parse_mode="Markdown")
        return
    
    accounts = load_accounts()
    used_data = load_used()
    
    total_users = len(used_data)
    total_accounts_given = sum(len(entries) for entries in used_data.values())
    today = datetime.now().strftime("%Y-%m-%d")
    today_given = sum(1 for entries in used_data.values() for e in entries if e.get("date") == today)
    
    await update.message.reply_text(
        f"📊 *Bot Statistics*\n\n"
        f"📦 *Available Accounts:* {len(accounts)}\n"
        f"👤 *Total Users:* {total_users}\n"
        f"📤 *Total Accounts Given:* {total_accounts_given}\n"
        f"📅 *Given Today:* {today_given}\n"
        f"💰 *Cashback:* 30% on all losses\n\n"
        f"📋 Use /listaccounts to see all available",
        parse_mode="Markdown"
    )

async def list_accounts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ *Unauthorized!*", parse_mode="Markdown")
        return
    
    accounts = load_accounts()
    
    if not accounts:
        await update.message.reply_text("📭 *No accounts available.*", parse_mode="Markdown")
        return
    
    formatted_accounts = []
    for i, acc in enumerate(accounts):
        parts = acc.split(":", 1)
        if len(parts) == 2:
            username, password = parts
            formatted_accounts.append(f"{i+1}. *Username:* `{username}`\n   *Password:* `{password}`")
        else:
            formatted_accounts.append(f"{i+1}. `{acc}`")
    
    account_list = "\n\n".join(formatted_accounts)
    
    await update.message.reply_text(
        f"📋 *Available Accounts ({len(accounts)})*\n\n"
        f"{account_list}\n\n"
        f"💰 *30% Cashback on all losses!*",
        parse_mode="Markdown"
    )

async def delete_account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ *Unauthorized!*", parse_mode="Markdown")
        return
    
    if not context.args:
        await update.message.reply_text(
            "📝 *How to delete an account:*\n\n"
            "`/del Username: player1`\n\n"
            "**Example:**\n"
            "`/del Username: 1736011027`",
            parse_mode="Markdown"
        )
        return
    
    text = " ".join(context.args)
    match = re.search(r'Username:\s*([^,]+)', text, re.IGNORECASE)
    if not match:
        await update.message.reply_text(
            "❌ *Invalid format!*\n\n"
            "Use:\n"
            "`/del Username: player1`",
            parse_mode="Markdown"
        )
        return
    
    username_to_delete = match.group(1).strip()
    accounts = load_accounts()
    
    account_to_delete = None
    for account in accounts:
        if account.startswith(f"{username_to_delete}:"):
            account_to_delete = account
            break
    
    if not account_to_delete:
        await update.message.reply_text(
            f"❌ *Account with username `{username_to_delete}` not found!*\n\n"
            "Use `/listaccounts` to see available accounts.",
            parse_mode="Markdown"
        )
        return
    
    accounts.remove(account_to_delete)
    save_accounts(accounts)
    
    await update.message.reply_text(
        f"✅ *Account Deleted!*\n\n"
        f"Removed: `{account_to_delete}`\n\n"
        f"📦 *Total Available:* {len(accounts)}",
        parse_mode="Markdown"
    )
    
async def clear_accounts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ *Unauthorized!*", parse_mode="Markdown")
        return
    
    accounts = load_accounts()
    
    if not accounts:
        await update.message.reply_text(
            "📭 *No accounts to clear!*",
            parse_mode="Markdown"
        )
        return
    
    count = len(accounts)
    save_accounts([])
    
    await update.message.reply_text(
        f"🗑️ *Cleared {count} account(s)!*\n\n"
        f"📦 *Total Available:* 0\n\n"
        f"⚠️ You can now add new accounts with `/ass`",
        parse_mode="Markdown"
    )

async def reset_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ *Unauthorized!*", parse_mode="Markdown")
        return
    
    if not context.args:
        await update.message.reply_text(
            "📝 Usage: `/resetuser user_id`\n"
            "Example: `/resetuser 123456789`\n\n"
            "⚠️ This removes all accounts the user has received!",
            parse_mode="Markdown"
        )
        return
    
    target_user = context.args[0]
    used_data = load_used()
    
    if target_user in used_data:
        del used_data[target_user]
        save_used(used_data)
        await update.message.reply_text(
            f"✅ *User {target_user} has been reset!*",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            f"❌ *User {target_user} not found.*",
            parse_mode="Markdown"
        )

# ============================================
# MAIN FUNCTION
# ============================================

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ass", add_account_command))
    app.add_handler(CommandHandler("add", add_account_command))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("listaccounts", list_accounts))
    app.add_handler(CommandHandler("resetuser", reset_user))
    app.add_handler(CommandHandler("del", delete_account))
    app.add_handler(CommandHandler("clearaccounts", clear_accounts))
    app.add_handler(CallbackQueryHandler(button_handler))
    
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
