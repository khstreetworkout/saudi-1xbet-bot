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
# CONFIGURATION - CHANGE THESE!
# ============================================
BOT_TOKEN = "8978819633:AAF9si6gH_sqvxC4uExZdwIK0gSkx8ToLq8"  # Your token
ADMIN_ID = 6012442109  # Your Telegram ID
ACCOUNTANT_ID = 6012442109  # Accountant's Telegram ID (can be same as admin)
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
DEPOSIT_FILE = os.path.join(DATA_DIR, "deposits.json")
WITHDRAW_FILE = os.path.join(DATA_DIR, "withdrawals.json")
STREAK_FILE = os.path.join(DATA_DIR, "streaks.json")

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

def load_streaks():
    if os.path.exists(STREAK_FILE):
        with open(STREAK_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_streaks(streaks):
    with open(STREAK_FILE, 'w') as f:
        json.dump(streaks, f, indent=2)

# ============================================
# PAYMENT METHODS
# ============================================
PAYMENT_METHODS = {
    "barq": {
        "name": "💳 Barq Wallet",
        "fields": ["phone_number"],
        "details": "📱 Transfer to: 05XXXXXXXX"
    },
    "bank_transfer": {
        "name": "🏦 Bank Transfer",
        "fields": ["phone_number", "iban"],
        "details": "🏦 IBAN: SA1234567890\n📱 Phone: 05XXXXXXXX"
    },
    "stc_pay": {
        "name": "📱 STC Pay",
        "fields": ["phone_number"],
        "details": "📱 Transfer to: 05XXXXXXXX"
    },
    "urpay": {
        "name": "💳 UrPay",
        "fields": ["phone_number", "wallet_address"],
        "details": "📱 Phone: 05XXXXXXXX\n🔗 Wallet: example@urpay.com"
    }
}

WITHDRAW_METHODS = {
    "bank_transfer": {
        "name": "🏦 Bank Transfer",
        "fields": ["full_name", "iban", "bank_name"]
    },
    "barq": {
        "name": "💳 Barq Wallet",
        "fields": ["phone_number"]
    },
    "stc_pay": {
        "name": "📱 STC Pay",
        "fields": ["phone_number"]
    }
}

# ============================================
# TASKS FOR STREAK CHALLENGE
# ============================================
TASKS = {
    1: {"task": "Login to 1xBet app with your account", "reward": 10, "week": 1},
    2: {"task": "Place 1 bet", "reward": 10, "week": 1},
    3: {"task": "Share bot with 2 friends", "reward": 10, "week": 1},
    4: {"task": "Login again + Place 1 bet", "reward": 10, "week": 1},
    5: {"task": "Share your referral link", "reward": 10, "week": 1},
    6: {"task": "Deposit 50+ SAR", "reward": 10, "week": 1},
    7: {"task": "Login + Place 1 bet + Share", "reward": 10, "week": 1},
    8: {"task": "Login daily (3 days streak)", "reward": 20, "week": 2},
    9: {"task": "Place 2 bets", "reward": 20, "week": 2},
    10: {"task": "Share bot with 3 friends", "reward": 20, "week": 2},
    11: {"task": "Deposit 100+ SAR", "reward": 20, "week": 2},
    12: {"task": "Login + Place 2 bets", "reward": 20, "week": 2},
    13: {"task": "Refer 1 new user", "reward": 20, "week": 2},
    14: {"task": "Weekly check-in", "reward": 20, "week": 2},
    15: {"task": "Login streak (7 days)", "reward": 30, "week": 3},
    16: {"task": "Place 3 bets", "reward": 30, "week": 3},
    17: {"task": "Share bot with 5 friends", "reward": 30, "week": 3},
    18: {"task": "Deposit 150+ SAR", "reward": 30, "week": 3},
    19: {"task": "Login + Place 3 bets", "reward": 30, "week": 3},
    20: {"task": "Refer 2 new users", "reward": 30, "week": 3},
    21: {"task": "Weekly check-in", "reward": 30, "week": 3},
    22: {"task": "Login streak (14 days)", "reward": 40, "week": 4},
    23: {"task": "Place 5 bets", "reward": 40, "week": 4},
    24: {"task": "Share bot with 7 friends", "reward": 40, "week": 4},
    25: {"task": "Deposit 200+ SAR", "reward": 40, "week": 4},
    26: {"task": "Login + Place 5 bets", "reward": 40, "week": 4},
    27: {"task": "Refer 3 new users", "reward": 40, "week": 4},
    28: {"task": "VIP Celebration!", "reward": 40, "week": 4},
}

# ============================================
# USER STATE STORAGE
# ============================================
user_states = {}

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
    """Return the main menu keyboard (reply keyboard)"""
    keyboard = [
        ["🎰 Get Account", "💬 Talk to Agent"],
        ["📋 My Accounts", "🔥 Streak Challenge"],
        ["💳 Deposit & Withdraw"],
        ["🔙 Back to Menu"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_back_to_menu_keyboard():
    """Return back button (reply keyboard)"""
    keyboard = [
        ["🔙 Back to Menu"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_get_another_keyboard():
    """Return get another + back menu"""
    keyboard = [
        ["🎰 Get Another Account"],
        ["📋 My Accounts"],
        ["🔙 Back to Menu"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_deposit_withdraw_keyboard():
    """Return deposit/withdraw menu"""
    keyboard = [
        ["💰 Deposit", "💸 Withdraw"],
        ["🔙 Back to Menu"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

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
    
    await update.message.reply_text(
        "🎰 *Welcome to Saudi 1xBet Bot!*\n\n"
        "💰 *Get 30% CASHBACK on all losses!*\n"
        "📌 You can get up to *2 accounts per day*\n"
        "🔥 *Complete daily tasks and earn rewards!*\n"
        "💳 *Deposit & Withdraw easily!*\n\n"
        "👆 Click the buttons below:",
        parse_mode="Markdown",
        reply_markup=keyboard
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # Handle accountant actions
    if query.data.startswith("deposit_accept_") or query.data.startswith("deposit_reject_"):
        await handle_accountant_action(update, context)
        return
    
    if query.data.startswith("withdraw_accept_") or query.data.startswith("withdraw_reject_"):
        await handle_accountant_action(update, context)
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

# ============================================
# MESSAGE HANDLER
# ============================================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user messages from reply keyboard"""
    user_id = str(update.effective_user.id)
    message_text = update.message.text
    used_data = load_used()
    
    # Show typing indicator
    await update.message.chat.send_action(action="typing")
    
    # Handle photo (receipt)
    if update.message.photo:
        await handle_receipt(update, context)
        return
    
    # Handle Back to Menu
    if message_text == "🔙 Back to Menu":
        await show_main_menu(update, context)
        return
    
    # Handle Get Account
    if message_text == "🎰 Get Account" or message_text == "🎰 Get Another Account":
        await handle_get_account(update, user_id, used_data)
        return
    
    # Handle Talk to Agent
    if message_text == "💬 Talk to Agent":
        await update.message.reply_text(
            f"💬 *Contact Our Agent*\n\n"
            f"📞 Reach out to *{AGENT_USERNAME}* for:\n"
            "• Account issues\n"
            "• Technical support\n"
            "• Questions about 1xBet\n"
            "• Cashback inquiries\n\n"
            f"👉 Click here: {AGENT_USERNAME}",
            parse_mode="Markdown",
            reply_markup=get_back_to_menu_keyboard()
        )
        return
    
    # Handle My Accounts
    if message_text == "📋 My Accounts":
        await handle_my_accounts(update, user_id, used_data)
        return
    
    # Handle Streak Challenge
    if message_text == "🔥 Streak Challenge":
        await show_streak(update, context)
        return
    
    # Handle Deposit & Withdraw
    if message_text == "💳 Deposit & Withdraw":
        await show_deposit_withdraw_menu(update, context)
        return
    
    # Handle Deposit
    if message_text == "💰 Deposit":
        await start_deposit(update, context)
        return
    
    # Handle Withdraw
    if message_text == "💸 Withdraw":
        await start_withdraw(update, context)
        return
    
    # Handle user states (deposit/withdraw steps)
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
            elif step == "details":
                await process_withdraw_field(update, context)
                return
            elif step == "code":
                await process_withdraw_code(update, context)
                return
    
    # Handle streak task completion
    if message_text.startswith("✅ Complete Day"):
        await complete_task(update, context)
        return
    
    if message_text == "📊 My Progress":
        await show_progress(update, context)
        return
    
    if message_text == "🏆 Claim VIP Reward":
        await claim_vip_reward(update, context)
        return
    
    # If unknown message
    await update.message.reply_text(
        "❌ *I don't understand that command.*\n\n"
        "Please use the buttons below:",
        parse_mode="Markdown",
        reply_markup=get_main_menu_keyboard()
    )

# ============================================
# ACCOUNT HANDLING
# ============================================

async def handle_get_account(update, user_id, used_data):
    """Handle account distribution - 2 per day max"""
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
    
    parts = account.split(":", 1)
    if len(parts) == 2:
        username, password = parts
        account_display = f"*Username:* `{username}`\n*Password:* `{password}`"
    else:
        account_display = f"`{account}`"
    
    await update.message.reply_text(
        f"✅ *Account Assigned!*\n\n"
        f"{account_display}\n\n"
        f"💰 *30% CASHBACK on all losses!*\n\n"
        f"📊 *Today's Usage:* {get_user_today_count(user_id, used_data)}/2\n"
        f"📦 *Accounts Remaining:* {remaining}\n\n"
        f"💡 *Tap to copy!*\n"
        f"🔒 Save it securely.",
        parse_mode="Markdown",
        reply_markup=get_get_another_keyboard()
    )

async def handle_my_accounts(update, user_id, used_data):
    """Handle My Accounts"""
    accounts = get_user_accounts(user_id, used_data)
    
    if not accounts:
        await update.message.reply_text(
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
    
    await update.message.reply_text(
        f"📋 *Your Accounts*\n\n"
        f"{account_list}\n\n"
        f"📊 *Today's Usage:* {today_count}/2\n"
        f"📦 *Total Accounts:* {len(accounts)}\n\n"
        f"💰 *30% Cashback on all losses!*\n"
        f"💡 *Tap any to copy*",
        parse_mode="Markdown",
        reply_markup=get_get_another_keyboard()
    )

# ============================================
# STREAK CHALLENGE
# ============================================

async def show_streak(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user's current streak and tasks"""
    user_id = str(update.effective_user.id)
    streaks = load_streaks()
    
    if user_id not in streaks:
        streaks[user_id] = {
            "current_day": 0,
            "completed_tasks": [],
            "total_rewards": 0,
            "last_completed": None,
            "week": 1
        }
        save_streaks(streaks)
    
    user_streak = streaks[user_id]
    current_day = user_streak.get("current_day", 0)
    
    next_day = current_day + 1
    if next_day > 28:
        keyboard = [
            [KeyboardButton("🏆 Claim VIP Reward")],
            [KeyboardButton("🔙 Back to Menu")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "🏆 *CONGRATULATIONS!*\n\n"
            "You've completed ALL 28 days of tasks! 🎉\n\n"
            "🎁 *Your Rewards:*\n"
            "• FREE VIP Account\n"
            "• 20% Permanent Cashback\n"
            "• 500 SAR Bonus\n"
            "• Exclusive Agent Support\n\n"
            "Click below to claim your VIP reward!",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
        return
    
    task = TASKS.get(next_day)
    if not task:
        await update.message.reply_text(
            "❌ *Task not found!*\n\n"
            "Please contact support.",
            parse_mode="Markdown"
        )
        return
    
    week = task.get("week", 1)
    reward = task.get("reward", 10)
    
    today = datetime.now().strftime("%Y-%m-%d")
    today_completed = user_streak.get("last_completed") == today
    
    if today_completed:
        keyboard = [
            [KeyboardButton("📊 My Progress")],
            [KeyboardButton("🔙 Back to Menu")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            f"✅ *Great job! You've completed today's task!*\n\n"
            f"🔥 *Current Streak:* {current_day} days\n"
            f"📅 *Day {next_day} waiting...*\n"
            f"💰 *Total Rewards:* {user_streak.get('total_rewards', 0)} SAR\n\n"
            f"⏳ Come back tomorrow for Day {next_day}!",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
        return
    
    keyboard = [
        [KeyboardButton(f"✅ Complete Day {next_day} Task")],
        [KeyboardButton("📊 My Progress")],
        [KeyboardButton("🔙 Back to Menu")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        f"🔥 *Daily Streak Challenge*\n\n"
        f"📅 *Day {next_day} of 28*\n"
        f"📆 *Week {week}*\n"
        f"💰 *Daily Reward:* {reward} SAR\n\n"
        f"📋 *Your Task:*\n"
        f"✅ {task['task']}\n\n"
        f"💡 *Total earned so far:* {user_streak.get('total_rewards', 0)} SAR\n"
        f"🔥 *Current Streak:* {current_day} days\n\n"
        f"Complete the task and click the button below!",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def complete_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mark current day's task as complete"""
    user_id = str(update.effective_user.id)
    streaks = load_streaks()
    
    if user_id not in streaks:
        await update.message.reply_text(
            "❌ *No streak found!*\n\n"
            "Use '🔥 Streak Challenge' to start your journey!",
            parse_mode="Markdown"
        )
        return
    
    user_streak = streaks[user_id]
    current_day = user_streak.get("current_day", 0)
    next_day = current_day + 1
    
    if next_day > 28:
        await update.message.reply_text(
            "🏆 *You've completed ALL tasks!*\n\n"
            "Claim your VIP reward!",
            parse_mode="Markdown"
        )
        return
    
    today = datetime.now().strftime("%Y-%m-%d")
    if user_streak.get("last_completed") == today:
        await update.message.reply_text(
            "✅ *You already completed today's task!*\n\n"
            "Come back tomorrow for the next one!",
            parse_mode="Markdown"
        )
        return
    
    task = TASKS.get(next_day, {"reward": 10})
    reward = task.get("reward", 10)
    
    user_streak["current_day"] = next_day
    user_streak["last_completed"] = today
    user_streak["total_rewards"] = user_streak.get("total_rewards", 0) + reward
    save_streaks(streaks)
    
    keyboard = [
        [KeyboardButton("📊 My Progress")],
        [KeyboardButton("🔙 Back to Menu")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        f"🎉 *AMAZING! You completed Day {next_day}!*\n\n"
        f"💰 *Reward Earned:* {reward} SAR\n"
        f"🔥 *Streak:* {next_day} days\n"
        f"📦 *Total Earned:* {user_streak.get('total_rewards', 0)} SAR\n\n"
        f"📅 *Tomorrow's Task:*\n"
        f"Day {next_day + 1} task will be available!\n\n"
        f"Keep going! You're doing great! 💪",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def show_progress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user's progress"""
    user_id = str(update.effective_user.id)
    streaks = load_streaks()
    
    if user_id not in streaks:
        await update.message.reply_text(
            "❌ *No progress found!*\n\n"
            "Use '🔥 Streak Challenge' to start your journey!",
            parse_mode="Markdown"
        )
        return
    
    user_streak = streaks[user_id]
    current_day = user_streak.get("current_day", 0)
    total_rewards = user_streak.get("total_rewards", 0)
    
    progress = min((current_day / 28) * 100, 100)
    filled = int(progress / 10)
    progress_bar = "█" * filled + "░" * (10 - filled)
    
    keyboard = [
        [KeyboardButton("🔥 Continue Challenge")],
        [KeyboardButton("🔙 Back to Menu")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        f"📊 *Your Progress*\n\n"
        f"📅 *Days Completed:* {current_day}/28\n"
        f"💰 *Total Rewards:* {total_rewards} SAR\n"
        f"🔥 *Progress:* {progress:.0f}%\n"
        f"📊 `{progress_bar}`\n\n"
        f"🏆 *Next Reward:*\n"
        f"• {7 - (current_day % 7)} days until weekly bonus!\n"
        f"• {28 - current_day} days until VIP Account!\n\n"
        f"💪 Keep going! You're amazing!",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def claim_vip_reward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Claim VIP reward after completing all tasks"""
    user_id = str(update.effective_user.id)
    streaks = load_streaks()
    
    if user_id not in streaks:
        await update.message.reply_text(
            "❌ *No progress found!*",
            parse_mode="Markdown"
        )
        return
    
    user_streak = streaks[user_id]
    current_day = user_streak.get("current_day", 0)
    
    if current_day < 28:
        await update.message.reply_text(
            f"❌ *You need to complete all 28 days first!*\n\n"
            f"Current progress: {current_day}/28 days",
            parse_mode="Markdown"
        )
        return
    
    # Check if already claimed
    if user_streak.get("vip_claimed", False):
        await update.message.reply_text(
            "✅ *You've already claimed your VIP reward!*\n\n"
            "Contact your agent for VIP support.",
            parse_mode="Markdown"
        )
        return
    
    # Mark as claimed
    user_streak["vip_claimed"] = True
    save_streaks(streaks)
    
    await update.message.reply_text(
        "🏆 *VIP REWARD CLAIMED!*\n\n"
        "🎁 *You are now a VIP member!*\n\n"
        "✅ *Benefits:*\n"
        "• 20% Permanent Cashback\n"
        "• Priority Support\n"
        "• Exclusive Bonuses\n"
        "• VIP Account\n\n"
        "📞 Your agent will contact you shortly!\n"
        f"Agent: {AGENT_USERNAME}",
        parse_mode="Markdown",
        reply_markup=get_main_menu_keyboard()
    )

# ============================================
# DEPOSIT & WITHDRAW SYSTEM
# ============================================

async def show_deposit_withdraw_menu(update, context):
    """Show deposit and withdraw options"""
    keyboard = [
        ["💰 Deposit", "💸 Withdraw"],
        ["🔙 Back to Menu"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "💳 *Deposit & Withdrawal*\n\n"
        "💰 *Deposit* - Add funds to your 1xBet account\n"
        "💸 *Withdraw* - Withdraw your winnings\n\n"
        "Select an option below:",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

# --- Deposit Flow ---

async def start_deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start deposit process"""
    user_id = str(update.effective_user.id)
    
    user_states[user_id] = {"action": "deposit", "step": "player_id"}
    
    await update.message.reply_text(
        "💰 *Deposit Process*\n\n"
        "Step 1/4: Enter your Player ID\n\n"
        "📝 Please enter your 1xBet Player ID:",
        parse_mode="Markdown",
        reply_markup=get_back_to_menu_keyboard()
    )

async def process_deposit_player_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process player ID input"""
    user_id = str(update.effective_user.id)
    player_id = update.message.text.strip()
    
    if not player_id.isdigit():
        await update.message.reply_text(
            "❌ *Invalid Player ID!*\n\n"
            "Please enter a valid numeric Player ID.",
            parse_mode="Markdown"
        )
        return
    
    user_states[user_id]["player_id"] = player_id
    user_states[user_id]["step"] = "method"
    
    keyboard = []
    for key, method in PAYMENT_METHODS.items():
        keyboard.append([KeyboardButton(method["name"])])
    keyboard.append([KeyboardButton("🔙 Back to Menu")])
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "💰 *Deposit Process*\n\n"
        f"✅ Player ID: `{player_id}`\n\n"
        "Step 2/4: Select payment method\n\n"
        "Choose your payment method:",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def process_deposit_method(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process payment method selection"""
    user_id = str(update.effective_user.id)
    method_name = update.message.text
    
    method_key = None
    for key, method in PAYMENT_METHODS.items():
        if method["name"] == method_name:
            method_key = key
            break
    
    if not method_key:
        await update.message.reply_text(
            "❌ *Invalid method!*\n\n"
            "Please select a valid payment method.",
            parse_mode="Markdown"
        )
        return
    
    user_states[user_id]["method"] = method_key
    user_states[user_id]["step"] = "amount"
    
    keyboard = [
        ["10 SAR", "25 SAR", "50 SAR"],
        ["100 SAR", "200 SAR", "500 SAR"],
        ["✏️ Enter Custom Amount"],
        ["🔙 Back to Menu"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    method_details = PAYMENT_METHODS[method_key]["details"]
    
    await update.message.reply_text(
        f"💰 *Deposit Process*\n\n"
        f"✅ Player ID: `{user_states[user_id]['player_id']}`\n"
        f"✅ Method: {method_name}\n\n"
        f"📋 *Method Details:*\n{method_details}\n\n"
        "Step 3/4: Enter amount\n\n"
        "Select an amount below or enter custom:",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def process_deposit_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process amount input"""
    user_id = str(update.effective_user.id)
    amount_text = update.message.text.replace(" SAR", "").strip()
    
    if amount_text == "✏️ Enter Custom Amount":
        await update.message.reply_text(
            "📝 *Enter custom amount:*\n\n"
            "Please enter the amount in SAR (10-500 SAR):",
            parse_mode="Markdown"
        )
        return
    
    try:
        amount = float(amount_text)
        if amount < 10:
            await update.message.reply_text(
                "❌ *Minimum amount is 10 SAR!*",
                parse_mode="Markdown"
            )
            return
        if amount > 500:
            await update.message.reply_text(
                "❌ *Maximum amount is 500 SAR!*",
                parse_mode="Markdown"
            )
            return
    except ValueError:
        await update.message.reply_text(
            "❌ *Invalid amount!*\n\n"
            "Please enter a valid number.",
            parse_mode="Markdown"
        )
        return
    
    user_states[user_id]["amount"] = amount
    user_states[user_id]["step"] = "receipt"
    
    await update.message.reply_text(
        f"💰 *Deposit Process*\n\n"
        f"✅ Player ID: `{user_states[user_id]['player_id']}`\n"
        f"✅ Method: {PAYMENT_METHODS[user_states[user_id]['method']]['name']}\n"
        f"✅ Amount: {amount} SAR\n\n"
        "Step 4/4: Send receipt\n\n"
        "📸 Please send a screenshot or photo of your transfer receipt.\n\n"
        "📌 *Instructions:*\n"
        "• Take a screenshot of the transfer confirmation\n"
        "• Send it as a photo to this chat\n\n"
        "⚠️ *Important:* The receipt must show:\n"
        "• The amount transferred\n"
        "• The recipient details\n"
        "• The transaction reference\n\n"
        "Type /cancel to cancel this request.",
        parse_mode="Markdown"
    )

async def handle_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle receipt photo from user"""
    user_id = str(update.effective_user.id)
    
    if user_id not in user_states or user_states[user_id].get("action") != "deposit":
        await update.message.reply_text(
            "❌ *No active deposit request!*\n\n"
            "Use '💰 Deposit' to start a new deposit.",
            parse_mode="Markdown"
        )
        return
    
    if user_states[user_id].get("step") != "receipt":
        return
    
    if not update.message.photo:
        await update.message.reply_text(
            "❌ *Please send a photo!*\n\n"
            "Take a screenshot of your transfer receipt and send it as a photo.",
            parse_mode="Markdown"
        )
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
        "created_at": datetime.now().isoformat(),
        "user_message_id": update.message.message_id
    }
    save_deposits(deposits)
    
    user_states[user_id] = {}
    
    await update.message.reply_text(
        "✅ *Receipt Received!*\n\n"
        "⏳ Please wait while our team verifies your transfer.\n\n"
        "You will be notified once your deposit is confirmed.\n\n"
        "📞 For urgent inquiries, contact our agent.",
        parse_mode="Markdown",
        reply_markup=get_back_to_menu_keyboard()
    )
    
    await notify_accountant_deposit(update, context, deposit_id, deposits[deposit_id])

async def notify_accountant_deposit(update, context, deposit_id, deposit_data):
    """Send deposit request to accountant"""
    method_name = PAYMENT_METHODS[deposit_data["method"]]["name"]
    
    keyboard = [
        [
            InlineKeyboardButton("✅ Accept", callback_data=f"deposit_accept_{deposit_id}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"deposit_reject_{deposit_id}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = (
        f"💰 *New Deposit Request*\n\n"
        f"🆔 ID: `{deposit_id}`\n"
        f"👤 User: @{deposit_data['username']}\n"
        f"🆔 Player ID: `{deposit_data['player_id']}`\n"
        f"💳 Method: {method_name}\n"
        f"💵 Amount: {deposit_data['amount']} SAR\n"
        f"📅 Time: {deposit_data['created_at']}\n\n"
        f"Please verify the transfer and respond:"
    )
    
    await context.bot.send_message(
        chat_id=ACCOUNTANT_ID,
        text=message,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

# --- Withdraw Flow ---

async def start_withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start withdraw process"""
    user_id = str(update.effective_user.id)
    user_states[user_id] = {"action": "withdraw", "step": "method"}
    
    keyboard = []
    for key, method in WITHDRAW_METHODS.items():
        keyboard.append([KeyboardButton(method["name"])])
    keyboard.append([KeyboardButton("🔙 Back to Menu")])
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "💸 *Withdraw Process*\n\n"
        "Step 1/3: Select withdrawal method\n\n"
        "Choose your withdrawal method:",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def process_withdraw_method(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process withdrawal method selection"""
    user_id = str(update.effective_user.id)
    method_name = update.message.text
    
    method_key = None
    for key, method in WITHDRAW_METHODS.items():
        if method["name"] == method_name:
            method_key = key
            break
    
    if not method_key:
        await update.message.reply_text(
            "❌ *Invalid method!*",
            parse_mode="Markdown"
        )
        return
    
    user_states[user_id]["method"] = method_key
    user_states[user_id]["step"] = "details"
    user_states[user_id]["details"] = {}
    
    fields = WITHDRAW_METHODS[method_key]["fields"]
    user_states[user_id]["fields"] = fields
    user_states[user_id]["field_index"] = 0
    
    await ask_withdraw_field(update, context)

async def ask_withdraw_field(update, context):
    """Ask for next withdrawal field"""
    user_id = str(update.effective_user.id)
    state = user_states[user_id]
    fields = state["fields"]
    field_index = state["field_index"]
    
    if field_index >= len(fields):
        await ask_withdraw_code(update, context)
        return
    
    field = fields[field_index]
    field_labels = {
        "full_name": "👤 Your full name",
        "iban": "🏦 IBAN number",
        "bank_name": "🏛️ Bank name",
        "phone_number": "📱 Phone number"
    }
    
    await update.message.reply_text(
        f"💸 *Withdraw Process*\n\n"
        f"Step 2/3: Enter your details\n\n"
        f"{field_labels.get(field, field)}:\n\n"
        f"📝 Please enter the information:",
        parse_mode="Markdown",
        reply_markup=get_back_to_menu_keyboard()
    )

async def process_withdraw_field(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process withdrawal field input"""
    user_id = str(update.effective_user.id)
    value = update.message.text.strip()
    
    if user_id not in user_states:
        return
    
    state = user_states[user_id]
    fields = state["fields"]
    field_index = state["field_index"]
    field = fields[field_index]
    
    state["details"][field] = value
    state["field_index"] += 1
    
    await ask_withdraw_field(update, context)

async def ask_withdraw_code(update, context):
    """Ask user for withdrawal code"""
    user_id = str(update.effective_user.id)
    state = user_states[user_id]
    state["step"] = "code"
    
    await update.message.reply_text(
        "💸 *Withdraw Process*\n\n"
        "Step 3/3: Enter withdrawal code\n\n"
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
        "Type /cancel to cancel this request.",
        parse_mode="Markdown",
        reply_markup=get_back_to_menu_keyboard()
    )

async def process_withdraw_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process withdrawal code input"""
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
        "method": state.get("method"),
        "details": state.get("details", {}),
        "code": code,
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }
    save_withdrawals(withdrawals)
    
    user_states[user_id] = {}
    
    await update.message.reply_text(
        "✅ *Withdrawal Request Submitted!*\n\n"
        "⏳ Please wait while our team processes your request.\n\n"
        "You will be notified once your withdrawal is confirmed.\n\n"
        "📞 For urgent inquiries, contact our agent.",
        parse_mode="Markdown",
        reply_markup=get_back_to_menu_keyboard()
    )
    
    await notify_accountant_withdraw(update, context, withdraw_id, withdrawals[withdraw_id])

async def notify_accountant_withdraw(update, context, withdraw_id, withdraw_data):
    """Send withdrawal request to accountant"""
    method_name = WITHDRAW_METHODS[withdraw_data["method"]]["name"]
    details_text = "\n".join([f"• {k}: {v}" for k, v in withdraw_data["details"].items()])
    
    keyboard = [
        [
            InlineKeyboardButton("✅ Accept", callback_data=f"withdraw_accept_{withdraw_id}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"withdraw_reject_{withdraw_id}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = (
        f"💸 *New Withdrawal Request*\n\n"
        f"🆔 ID: `{withdraw_id}`\n"
        f"👤 User: @{withdraw_data['username']}\n"
        f"💳 Method: {method_name}\n"
        f"📋 Details:\n{details_text}\n"
        f"🔑 Withdrawal Code: `{withdraw_data['code']}`\n"
        f"📅 Time: {withdraw_data['created_at']}\n\n"
        f"Please verify and respond:"
    )
    
    await context.bot.send_message(
        chat_id=ACCOUNTANT_ID,
        text=message,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

# ============================================
# ACCOUNTANT HANDLERS
# ============================================

async def handle_accountant_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle accountant accept/reject actions"""
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
                text="✅ *Your deposit has been confirmed!*\n\n"
                     f"💰 Amount: {deposits[request_id]['amount']} SAR\n"
                     "🎉 Funds have been added to your 1xBet account!\n\n"
                     "💡 Use 'Get Account' if you need another account.",
                parse_mode="Markdown"
            )
            
            await query.edit_message_text("✅ Deposit accepted!")
        else:
            context.user_data["reject_deposit"] = request_id
            await query.edit_message_text(
                f"❌ *Reject Deposit*\n\n"
                f"Request ID: `{request_id}`\n\n"
                "Please send the reason for rejection:",
                parse_mode="Markdown"
            )
    
    elif type_ == "withdraw":
        withdrawals = load_withdrawals()
        if request_id not in withdrawals:
            await query.edit_message_text("❌ Withdrawal request not found!")
            return
        
        if action == "accept":
            withdrawals[request_id]["status"] = "completed"
            save_withdrawals(withdrawals)
            
            user_id = withdrawals[request_id]["user_id"]
            await context.bot.send_message(
                chat_id=user_id,
                text="✅ *Your withdrawal has been processed!*\n\n"
                     "💰 Your funds have been sent to your selected method.\n\n"
                     "📞 Contact our agent if you have any questions.",
                parse_mode="Markdown"
            )
            
            await query.edit_message_text("✅ Withdrawal accepted!")
        else:
            context.user_data["reject_withdraw"] = request_id
            await query.edit_message_text(
                f"❌ *Reject Withdrawal*\n\n"
                f"Request ID: `{request_id}`\n\n"
                "Please send the reason for rejection:",
                parse_mode="Markdown"
            )

async def process_rejection_reason(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process rejection reason from accountant"""
    if "reject_deposit" in context.user_data:
        request_id = context.user_data.pop("reject_deposit")
        deposits = load_deposits()
        if request_id in deposits:
            deposits[request_id]["status"] = "rejected"
            deposits[request_id]["reason"] = update.message.text
            save_deposits(deposits)
            
            user_id = deposits[request_id]["user_id"]
            await context.bot.send_message(
                chat_id=user_id,
                text=f"❌ *Deposit Rejected!*\n\n"
                     f"💰 Amount: {deposits[request_id]['amount']} SAR\n\n"
                     f"📋 *Reason:*\n{update.message.text}\n\n"
                     f"📞 Contact our agent for assistance.",
                parse_mode="Markdown"
            )
            
            await update.message.reply_text("✅ Rejection reason sent to user.")
            return
    
    if "reject_withdraw" in context.user_data:
        request_id = context.user_data.pop("reject_withdraw")
        withdrawals = load_withdrawals()
        if request_id in withdrawals:
            withdrawals[request_id]["status"] = "rejected"
            withdrawals[request_id]["reason"] = update.message.text
            save_withdrawals(withdrawals)
            
            user_id = withdrawals[request_id]["user_id"]
            await context.bot.send_message(
                chat_id=user_id,
                text=f"❌ *Withdrawal Rejected!*\n\n"
                     f"📋 *Reason:*\n{update.message.text}\n\n"
                     f"📞 Contact our agent for assistance.",
                parse_mode="Markdown"
            )
            
            await update.message.reply_text("✅ Rejection reason sent to user.")
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
    deposits = load_deposits()
    withdrawals = load_withdrawals()
    
    total_users = len(used_data)
    total_accounts_given = sum(len(entries) for entries in used_data.values())
    today = datetime.now().strftime("%Y-%m-%d")
    today_given = sum(1 for entries in used_data.values() for e in entries if e.get("date") == today)
    
    pending_deposits = sum(1 for d in deposits.values() if d.get("status") == "pending")
    pending_withdrawals = sum(1 for w in withdrawals.values() if w.get("status") == "pending")
    
    await update.message.reply_text(
        f"📊 *Bot Statistics*\n\n"
        f"📦 *Available Accounts:* {len(accounts)}\n"
        f"👤 *Total Users:* {total_users}\n"
        f"📤 *Total Accounts Given:* {total_accounts_given}\n"
        f"📅 *Given Today:* {today_given}\n"
        f"💰 *Cashback:* 30% on all losses\n"
        f"💳 *Pending Deposits:* {pending_deposits}\n"
        f"💸 *Pending Withdrawals:* {pending_withdrawals}\n\n"
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
    
    # Handle inline button callbacks
    app.add_handler(CallbackQueryHandler(button_handler))
    
    # Handle messages from reply keyboard
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Handle photos for receipts
    app.add_handler(MessageHandler(filters.PHOTO, handle_message))
    
    # Handle rejection reasons from accountant
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_rejection_reason))
    
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
