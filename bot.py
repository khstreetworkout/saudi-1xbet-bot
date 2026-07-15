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
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Import language support
from languages import t
from user_language import get_user_language, set_user_language, load_languages

# ============================================
# CONFIGURATION
# ============================================
BOT_TOKEN = "8978819633:AAF9si6gH_sqvxC4uExZdwIK0gSkx8ToLq8"
ADMIN_ID = 6012442109
ACCOUNTANT_ID = 6012442109
AGENT_USERNAME = "@Saudi_1xbet_agent"
CASHBACK_PERCENT = 0.25
GROUP_CHAT_ID = -1004309440596  # Your group ID

# ============================================
# DATA DIRECTORY
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
POST_STATES_FILE = os.path.join(DATA_DIR, "post_states.json")
CASHBACK_REQUESTS_FILE = os.path.join(DATA_DIR, "cashback_requests.json")

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

def load_post_states():
    if os.path.exists(POST_STATES_FILE):
        try:
            with open(POST_STATES_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_post_states(states):
    with open(POST_STATES_FILE, 'w') as f:
        json.dump(states, f, indent=2)

def load_cashback_requests():
    if os.path.exists(CASHBACK_REQUESTS_FILE):
        try:
            with open(CASHBACK_REQUESTS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_cashback_requests(requests):
    with open(CASHBACK_REQUESTS_FILE, 'w') as f:
        json.dump(requests, f, indent=2)

def load_cashback_request(request_id):
    requests = load_cashback_requests()
    return requests.get(request_id)

def save_cashback_request(request_id, request_data):
    requests = load_cashback_requests()
    requests[request_id] = request_data
    save_cashback_requests(requests)

# ============================================
# USER STATE STORAGE
# ============================================
user_states = {}
admin_states = {}
post_states = {}
cashback_requests = {}

# ============================================
# HELPER FUNCTIONS
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
def get_main_menu_keyboard(user_id=None):
    if user_id is None:
        user_id = 0
    return ReplyKeyboardMarkup([
        [t(user_id, "get_account"), t(user_id, "talk_to_agent")],
        [t(user_id, "my_accounts"), t(user_id, "deposit_withdraw")],
        [t(user_id, "video_tutorials")],
        ["💰 Request Cashback", t(user_id, "share_bot")],
        [t(user_id, "back_to_menu")]
    ], resize_keyboard=True)

def get_admin_menu_keyboard(user_id=None):
    if user_id is None:
        user_id = 0
    return ReplyKeyboardMarkup([
        [t(user_id, "get_account"), t(user_id, "talk_to_agent")],
        [t(user_id, "my_accounts"), t(user_id, "deposit_withdraw")],
        [t(user_id, "video_tutorials")],
        ["💰 Request Cashback", t(user_id, "share_bot")],
        ["📝 Add Post", t(user_id, "stats")],
        [t(user_id, "list_accounts"), t(user_id, "add_accounts")],
        [t(user_id, "payment_methods"), t(user_id, "back_to_menu")]
    ], resize_keyboard=True)

def get_back_to_menu_keyboard(user_id=None):
    if user_id is None:
        user_id = 0
    return ReplyKeyboardMarkup([[t(user_id, "back_to_menu")]], resize_keyboard=True)

def get_get_another_keyboard(user_id=None):
    if user_id is None:
        user_id = 0
    return ReplyKeyboardMarkup([
        [t(user_id, "get_another_account")],
        [t(user_id, "my_accounts")],
        [t(user_id, "share_bot")],
        [t(user_id, "back_to_menu")]
    ], resize_keyboard=True)

def get_pm_menu_keyboard(user_id=None):
    if user_id is None:
        user_id = 0
    return ReplyKeyboardMarkup([
        [t(user_id, "list_methods"), t(user_id, "add_method")],
        [t(user_id, "edit_method"), t(user_id, "delete_method")],
        [t(user_id, "back_to_menu")]
    ], resize_keyboard=True)

def get_admin_video_keyboard(user_id=None):
    if user_id is None:
        user_id = 0
    return ReplyKeyboardMarkup([
        [t(user_id, "add_video"), t(user_id, "delete_video")],
        [t(user_id, "list_videos")],
        [t(user_id, "back_to_menu")]
    ], resize_keyboard=True)

def get_video_menu_keyboard(videos, user_id=None):
    if user_id is None:
        user_id = 0
    keyboard = []
    for video_id, video_data in videos.items():
        keyboard.append([KeyboardButton(f"🎬 {video_data['title']}")])
    keyboard.append([t(user_id, "back_to_menu")])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_stats_menu_keyboard(user_id=None):
    if user_id is None:
        user_id = 0
    return ReplyKeyboardMarkup([
        [t(user_id, "overall_stats_button")],
        [t(user_id, "user_stats_button")],
        [t(user_id, "cashback_button")],
        [t(user_id, "back_to_menu")]
    ], resize_keyboard=True)

# ============================================
# LANGUAGE COMMAND
# ============================================

async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    keyboard = [
        [InlineKeyboardButton(t(user_id, "english"), callback_data="lang_en")],
        [InlineKeyboardButton(t(user_id, "arabic"), callback_data="lang_ar")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        t(user_id, "language_selection"),
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = query.data.split("_")[1]
    set_user_language(user_id, lang)
    if lang == "ar":
        msg = t(user_id, "language_saved_ar")
    else:
        msg = t(user_id, "language_saved")
    await query.message.reply_text(msg, parse_mode="Markdown")
    await show_main_menu_from_callback(query, context)

async def show_main_menu_from_callback(query, context):
    user_id = query.from_user.id
    username = query.from_user.username or "NoUsername"
    update_user_data(str(user_id), username)
    if user_id == ADMIN_ID:
        keyboard = get_admin_menu_keyboard(user_id)
        menu_text = t(user_id, "admin_welcome")
    else:
        keyboard = get_main_menu_keyboard(user_id)
        menu_text = t(user_id, "welcome_text")
    await query.message.reply_text(menu_text, parse_mode="Markdown", reply_markup=keyboard)

# ============================================
# MAIN BOT COMMANDS
# ============================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    languages = load_languages()
    if str(user_id) not in languages:
        keyboard = [
            [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")],
            [InlineKeyboardButton("🇸🇦 العربية", callback_data="lang_ar")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            t(user_id, "language_selection"),
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
        return

    is_member = await is_user_member(user_id, "saudi_1xbet_accounts", context)
    if not is_member:
        keyboard = [
            [InlineKeyboardButton(t(user_id, "join_channel_button"), url="https://t.me/saudi_1xbet_accounts")],
            [InlineKeyboardButton(t(user_id, "check_subscription"), callback_data="check_subscription")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            t(user_id, "join_channel"),
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

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or "NoUsername"
    update_user_data(str(user_id), username)
    if user_id == ADMIN_ID:
        keyboard = get_admin_menu_keyboard(user_id)
        menu_text = t(user_id, "admin_welcome")
    else:
        keyboard = get_main_menu_keyboard(user_id)
        menu_text = t(user_id, "welcome_text")
    await update.message.reply_text(menu_text, parse_mode="Markdown", reply_markup=keyboard)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # Cashback admin actions
    if query.data.startswith(("cb_accept_", "cb_reject_")):
        await handle_cashback_admin_action(update, context)
        return
    
    # Cashback user confirm/cancel
    if query.data.startswith("cashback_confirm_"):
        await process_cashback_confirm(update, context)
        return
    
    if query.data.startswith("cashback_cancel_"):
        await process_cashback_cancel(update, context)
        return
    
    if query.data.startswith(("deposit_accept_", "deposit_reject_", "withdraw_accept_", "withdraw_reject_")):
        await handle_accountant_action(update, context)
        return
    
    if query.data == "check_subscription":
        user_id = query.from_user.id
        is_member = await is_user_member(user_id, "saudi_1xbet_accounts", context)
        if is_member:
            await query.message.reply_text(t(user_id, "subscription_verified"), reply_markup=get_main_menu_keyboard(user_id))
        else:
            keyboard = [
                [InlineKeyboardButton(t(user_id, "join_channel_button"), url="https://t.me/saudi_1xbet_accounts")],
                [InlineKeyboardButton(t(user_id, "check_subscription"), callback_data="check_subscription")]
            ]
            await query.message.reply_text(
                t(user_id, "not_member"),
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        return
    
    if query.data.startswith("lang_"):
        await language_callback(update, context)
        return

# ============================================
# GROUP WELCOME HANDLER
# ============================================

async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message - Private DM with name + buttons, Public group without name + buttons"""
    chat_id = update.effective_chat.id
    
    # Only trigger in your group
    if chat_id != GROUP_CHAT_ID:
        return
    
    # Check if there are new members
    if not update.message or not update.message.new_chat_members:
        return
    
    # For each new member (except the bot itself)
    for new_member in update.message.new_chat_members:
        if new_member.id == context.bot.id:
            continue  # Skip if bot itself joins
        
        user_id = new_member.id
        first_name = new_member.first_name or "User"
        username = f"@{new_member.username}" if new_member.username else first_name
        
        # Get user's preferred language (default to English if not set)
        lang = get_user_language(user_id)
        
        # ============================================
        # CREATE BUTTONS (SAME FOR BOTH MESSAGES)
        # ============================================
        keyboard = [
            [InlineKeyboardButton("🎰 Open Bot" if lang == "en" else "🎰 افتح البوت", url="https://t.me/Saudi_1xBet_bot?start=group")],
            [InlineKeyboardButton("📞 Contact Agent" if lang == "en" else "📞 تواصل مع الوكيل", url="https://t.me/Saudi_1xbet_agent")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # ============================================
        # 1. SEND PRIVATE DM WITH NAME + BUTTONS
        # ============================================
        if lang == "ar":
            dm_text = (
                f"👋 *مرحباً {username}!*\n\n"
                f"🎰 *مرحباً بك في مجموعة 1xBet السعودية!*\n\n"
                f"📌 *للحصول على حساب مجاني:*\n"
                f"• اضغط على الزر أدناه لفتح البوت\n\n"
                f"📞 *للاستفسارات والدعم:*\n"
                f"• تواصل مع وكيلنا مباشرة\n\n"
                f"🔥 *استمتع بخدماتنا!*"
            )
        else:
            dm_text = (
                f"👋 *Welcome {username}!*\n\n"
                f"🎰 *Welcome to 1xBet Saudi Arabia group!*\n\n"
                f"📌 *To get a free account:*\n"
                f"• Click the button below to open the bot\n\n"
                f"📞 *For inquiries and support:*\n"
                f"• Contact our agent directly\n\n"
                f"🔥 *Enjoy our services!*"
            )
        
        # Send PRIVATE DM to the user
        try:
            await context.bot.send_message(
                chat_id=user_id,  # Send to user's private chat
                text=dm_text,
                parse_mode="Markdown",
                reply_markup=reply_markup  # ✅ WITH buttons
            )
            print(f"✅ Welcome DM sent to {user_id} ({username})")
        except Exception as e:
            print(f"❌ Could not send DM to {user_id}: {e}")
        
        # ============================================
        # 2. SEND PUBLIC GROUP WELCOME (NO NAME) + BUTTONS
        # ============================================
        if lang == "ar":
            group_text = (
                f"👋 *مرحباً!*\n\n"
                f"🎰 *مرحباً بك في مجموعة 1xBet السعودية!*\n\n"
                f"📌 *للحصول على حساب مجاني:*\n"
                f"• اضغط على الزر أدناه لفتح البوت\n\n"
                f"📞 *للاستفسارات والدعم:*\n"
                f"• تواصل مع وكيلنا مباشرة\n\n"
                f"🔥 *استمتع بخدماتنا!*"
            )
        else:
            group_text = (
                f"👋 *Welcome!*\n\n"
                f"🎰 *Welcome to 1xBet Saudi Arabia group!*\n\n"
                f"📌 *To get a free account:*\n"
                f"• Click the button below to open the bot\n\n"
                f"📞 *For inquiries and support:*\n"
                f"• Contact our agent directly\n\n"
                f"🔥 *Enjoy our services!*"
            )
        
        # Send to the group WITH buttons
        await context.bot.send_message(
            chat_id=chat_id,  # Send to the group
            text=group_text,
            parse_mode="Markdown",
            reply_markup=reply_markup  # ✅ WITH buttons
        )

# ============================================
# CASHBACK REQUEST SYSTEM
# ============================================

async def cashback_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle cashback request from user"""
    user_id = str(update.effective_user.id)
    
    # Send the tutorial video
    videos = load_videos()
    video_found = False
    
    # Look for video with specific ID or cashback in title
    for vid, data in videos.items():
        if vid == "VID_20260715013849" or "cashback" in data['title'].lower():
            try:
                await update.message.reply_video(
                    video=data['file_id'],
                    caption=t(user_id, "cashback_video_caption"),
                    parse_mode="Markdown"
                )
                video_found = True
                break
            except Exception as e:
                print(f"Error sending cashback video: {e}")
    
    if not video_found:
        await update.message.reply_text(
            t(user_id, "cashback_video_not_found"),
            parse_mode="Markdown"
        )
        return
    
    # Ask for player ID
    cashback_requests[user_id] = {"step": "waiting_for_player_id"}
    
    await update.message.reply_text(
        t(user_id, "cashback_request_message"),
        parse_mode="Markdown"
    )

async def process_cashback_player_id_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process player ID for cashback request"""
    user_id = str(update.effective_user.id)
    
    if user_id not in cashback_requests:
        return
    
    if cashback_requests[user_id].get("step") != "waiting_for_player_id":
        return
    
    player_id = update.message.text.strip()
    if not player_id.isdigit():
        await update.message.reply_text(
            t(user_id, "invalid_player_id"),
            parse_mode="Markdown"
        )
        return
    
    cashback_requests[user_id]["player_id"] = player_id
    cashback_requests[user_id]["step"] = "waiting_for_confirmation"
    cashback_requests[user_id]["username"] = update.effective_user.username or "NoUsername"
    cashback_requests[user_id]["user_id"] = user_id
    
    # Show confirmation
    keyboard = [
        [InlineKeyboardButton(t(user_id, "confirm_button"), callback_data=f"cashback_confirm_{user_id}")],
        [InlineKeyboardButton(t(user_id, "cancel_button"), callback_data=f"cashback_cancel_{user_id}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        t(user_id, "cashback_confirm_message", player_id=player_id),
        parse_mode="Markdown",
        reply_markup=reply_markup
    )
    
async def process_cashback_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Confirm and send cashback request to admin"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    parts = data.split("_")
    user_id = parts[2]
    
    if user_id not in cashback_requests:
        await query.edit_message_text(
            t(user_id, "cashback_session_expired"),
            parse_mode="Markdown"
        )
        return
    
    state = cashback_requests[user_id]
    player_id = state.get("player_id")
    username = state.get("username")
    
    # Calculate cashback
    deposits = load_deposits()
    withdrawals = load_withdrawals()
    
    total_deposits = 0
    total_withdrawals = 0
    
    for d in deposits.values():
        if d.get("player_id") == player_id and d.get("status") == "completed":
            total_deposits += d.get("amount", 0)
    
    for w in withdrawals.values():
        if w.get("player_id") == player_id and w.get("status") == "completed":
            total_withdrawals += w.get("amount", 0)
    
    net_amount = total_deposits - total_withdrawals
    cashback_amount = net_amount * 0.25  # 25% cashback
    
    # Store the request
    request_id = f"CB_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    cashback_requests[user_id]["request_id"] = request_id
    cashback_requests[user_id]["total_deposits"] = total_deposits
    cashback_requests[user_id]["total_withdrawals"] = total_withdrawals
    cashback_requests[user_id]["net_amount"] = net_amount
    cashback_requests[user_id]["cashback_amount"] = cashback_amount
    cashback_requests[user_id]["status"] = "pending"
    
    # Notify admin (use admin's language)
    admin_id = ADMIN_ID
    keyboard = [
        [InlineKeyboardButton(t(admin_id, "deposit_accept"), callback_data=f"cb_accept_{request_id}"),
         InlineKeyboardButton(t(admin_id, "deposit_reject"), callback_data=f"cb_reject_{request_id}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    admin_message = t(admin_id, "cashback_admin_notification",
                      request_id=request_id,
                      username=username,
                      player_id=player_id,
                      total_deposits=total_deposits,
                      total_withdrawals=total_withdrawals,
                      net_amount=net_amount,
                      cashback_amount=cashback_amount)
    
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=admin_message,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )
    
    # Save request to file
    save_cashback_request(request_id, cashback_requests[user_id])
    
    # Clear the state
    cashback_requests.pop(user_id, None)
    
    await query.edit_message_text(
        t(user_id, "cashback_submitted",
          player_id=player_id,
          cashback_amount=cashback_amount),
        parse_mode="Markdown"
    )

async def process_cashback_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel cashback request"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    parts = data.split("_")
    user_id = parts[2]
    
    if user_id in cashback_requests:
        cashback_requests.pop(user_id, None)
    
    await query.edit_message_text(
        t(user_id, "cashback_cancelled"),
        parse_mode="Markdown"
    )

async def handle_cashback_admin_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle admin accept/reject for cashback"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    parts = data.split("_")
    action = parts[1]  # accept or reject
    request_id = "_".join(parts[2:])
    admin_id = update.effective_user.id
    
    # Load the request
    request = load_cashback_request(request_id)
    if not request:
        await query.edit_message_text(t(admin_id, "cashback_request_not_found"), parse_mode="Markdown")
        return
    
    if action == "accept":
        # Process acceptance
        user_id = request.get("user_id")
        cashback_amount = request.get("cashback_amount", 0)
        player_id = request.get("player_id")
        
        # Update request status
        request["status"] = "completed"
        save_cashback_request(request_id, request)
        
        # Notify user (in user's language)
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=t(user_id, "cashback_approved",
                      cashback_amount=cashback_amount,
                      player_id=player_id),
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Error notifying user: {e}")
        
        await query.edit_message_text(
            t(admin_id, "cashback_accepted_admin",
              request_id=request_id,
              cashback_amount=cashback_amount),
            parse_mode="Markdown"
        )
        
    else:  # reject
        context.user_data["reject_cashback"] = request_id
        await query.edit_message_text(
            t(admin_id, "cashback_reject_prompt", request_id=request_id),
            parse_mode="Markdown"
        )
async def process_cashback_rejection_reason(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process cashback rejection reason"""
    user_id = update.effective_user.id
    
    if "reject_cashback" not in context.user_data:
        return False
    
    request_id = context.user_data.pop("reject_cashback")
    reason = update.message.text
    
    if not reason:
        await update.message.reply_text(
            t(user_id, "rejection_prompt"),
            parse_mode="Markdown"
        )
        return True
    
    request = load_cashback_request(request_id)
    if not request:
        await update.message.reply_text(
            t(user_id, "cashback_request_not_found"),
            parse_mode="Markdown"
        )
        return True
    
    # Update request status
    request["status"] = "rejected"
    request["reason"] = reason
    save_cashback_request(request_id, request)
    
    # Notify user (in user's language)
    user_id_user = request.get("user_id")
    try:
        await context.bot.send_message(
            chat_id=user_id_user,
            text=t(user_id_user, "cashback_rejected", reason=reason),
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"Error notifying user: {e}")
    
    await update.message.reply_text(
        t(user_id, "rejection_sent"),
        parse_mode="Markdown",
        reply_markup=get_admin_menu_keyboard(user_id)
    )
    
    return True

# ============================================
# ADMIN POST CREATION SYSTEM
# ============================================

async def add_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the post creation process"""
    user_id = str(update.effective_user.id)
    
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ Unauthorized!", parse_mode=None)
        return
    
    post_states[user_id] = {"step": "content"}
    await update.message.reply_text(
        "📝 Create a New Post\n\n"
        "Step 1/6: Send me the post content\n\n"
        "You can send:\n"
        "• 📝 Text message\n"
        "• 🖼️ Photo (with or without caption)\n"
        "• 🎥 Video (with or without caption)\n\n"
        "Type /cancel to cancel.",
        parse_mode=None,
        reply_markup=ReplyKeyboardMarkup([["🔙 Cancel Post"]], resize_keyboard=True)
    )

async def process_post_content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle content submission (text, photo, video)"""
    user_id = str(update.effective_user.id)
    
    if user_id not in post_states:
        return
    
    if post_states[user_id].get("step") != "content":
        return
    
    if update.message.text and update.message.text == "🔙 Cancel Post":
        await cancel_post(update, context)
        return
    
    if update.message.text:
        post_states[user_id]["content_type"] = "text"
        post_states[user_id]["text"] = update.message.text
        post_states[user_id]["caption"] = None
    elif update.message.photo:
        post_states[user_id]["content_type"] = "photo"
        post_states[user_id]["file_id"] = update.message.photo[-1].file_id
        post_states[user_id]["caption"] = update.message.caption
    elif update.message.video:
        post_states[user_id]["content_type"] = "video"
        post_states[user_id]["file_id"] = update.message.video.file_id
        post_states[user_id]["caption"] = update.message.caption
    elif update.message.document:
        post_states[user_id]["content_type"] = "document"
        post_states[user_id]["file_id"] = update.message.document.file_id
        post_states[user_id]["caption"] = update.message.caption
    else:
        await update.message.reply_text("❌ Please send text, photo, or video.", parse_mode=None)
        return
    
    post_states[user_id]["step"] = "button_count"
    await update.message.reply_text(
        "✅ Content Received!\n\n"
        "Step 2/6: How many buttons do you want?\n"
        "Choose a number from 0 to 9:",
        parse_mode=None,
        reply_markup=ReplyKeyboardMarkup(
            [["0", "1", "2", "3", "4", "5"], ["6", "7", "8", "9"]],
            resize_keyboard=True
        )
    )

async def process_button_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button count selection"""
    user_id = str(update.effective_user.id)
    
    if user_id not in post_states:
        return
    
    if post_states[user_id].get("step") != "button_count":
        return
    
    if update.message.text == "🔙 Cancel Post":
        await cancel_post(update, context)
        return
    
    try:
        count = int(update.message.text)
        if count < 0 or count > 9:
            raise ValueError
    except:
        await update.message.reply_text("❌ Please enter a number between 0 and 9.", parse_mode=None)
        return
    
    if count == 0:
        post_states[user_id]["buttons"] = []
        post_states[user_id]["step"] = "confirm"
        await show_confirmation(update, context)
        return
    
    post_states[user_id]["button_count"] = count
    post_states[user_id]["buttons"] = []
    post_states[user_id]["current_button"] = 0
    post_states[user_id]["step"] = "button_config"
    await ask_button_config(update, context)

async def ask_button_config(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask for button configuration"""
    user_id = str(update.effective_user.id)
    state = post_states[user_id]
    current = state["current_button"]
    total = state["button_count"]
    
    keyboard = ReplyKeyboardMarkup([
        ["🔗 URL", "📋 Callback Data"],
        ["🌐 Web App", "👤 User"],
        ["🤖 Bot", "🔄 Switch Inline"],
        ["🔙 Cancel Post"]
    ], resize_keyboard=True)
    
    await update.message.reply_text(
        f"Button {current + 1} of {total}\n\n"
        "Step 3/6: Select the button type:\n\n"
        "• URL - Opens a website\n"
        "• Callback Data - Sends data to bot (e.g., claim_bonus)\n"
        "• Web App - Opens a Mini App\n"
        "• User - Opens a user profile\n"
        "• Bot - Opens a bot chat\n"
        "• Switch Inline - Switches to inline mode",
        parse_mode=None
    )
    
    await update.message.reply_text(
        "Select a button type:",
        reply_markup=keyboard
    )

async def process_button_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button type selection"""
    user_id = str(update.effective_user.id)
    
    if user_id not in post_states:
        return
    
    if post_states[user_id].get("step") != "button_config":
        return
    
    if update.message.text == "🔙 Cancel Post":
        await cancel_post(update, context)
        return
    
    button_type_map = {
        "🔗 URL": "url",
        "📋 Callback Data": "callback_data",
        "🌐 Web App": "web_app",
        "👤 User": "user",
        "🤖 Bot": "bot",
        "🔄 Switch Inline": "switch_inline_query"
    }
    
    button_type = button_type_map.get(update.message.text)
    if not button_type:
        await update.message.reply_text("❌ Please select a valid button type.", parse_mode=None)
        return
    
    # Store the button type and move to name step
    post_states[user_id]["current_button_type"] = button_type
    post_states[user_id]["step"] = "button_name"
    
    await update.message.reply_text(
        f"Button {post_states[user_id]['current_button'] + 1} of {post_states[user_id]['button_count']}\n\n"
        "Step 4/6: Enter the button text (display name):\n\n"
        "Example: 🎰 Get Account",
        parse_mode=None,
        reply_markup=ReplyKeyboardMarkup([["🔙 Cancel Post"]], resize_keyboard=True)
    )

async def process_button_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button name entry"""
    user_id = str(update.effective_user.id)
    
    if user_id not in post_states:
        return
    
    if post_states[user_id].get("step") != "button_name":
        return
    
    if update.message.text == "🔙 Cancel Post":
        await cancel_post(update, context)
        return
    
    # Save the button name
    post_states[user_id]["current_button_name"] = update.message.text
    
    # Move to value step
    post_states[user_id]["step"] = "button_value"
    
    button_type = post_states[user_id]["current_button_type"]
    examples = {
        "url": "Example: https://t.me/yourbot",
        "callback_data": "Example: claim_bonus or get_account",
        "web_app": "Example: https://your-app.com",
        "user": "Example: @username (or numeric ID)",
        "bot": "Example: @yourbot",
        "switch_inline_query": "Example: text to search"
    }
    
    await update.message.reply_text(
        f"Button {post_states[user_id]['current_button'] + 1} of {post_states[user_id]['button_count']}\n\n"
        f"Step 5/6: Enter the button value:\n\n"
        f"📌 Type: {button_type}\n"
        f"{examples.get(button_type, '')}\n\n"
        "Type the value:",
        parse_mode=None,
        reply_markup=ReplyKeyboardMarkup([["🔙 Cancel Post"]], resize_keyboard=True)
    )

async def process_button_value(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button value entry and save button"""
    user_id = str(update.effective_user.id)
    
    if user_id not in post_states:
        return
    
    if post_states[user_id].get("step") != "button_value":
        return
    
    if update.message.text == "🔙 Cancel Post":
        await cancel_post(update, context)
        return
    
    state = post_states[user_id]
    
    # Save the button with text, type, and value
    button_data = {
        "text": state["current_button_name"],
        "type": state["current_button_type"],
        "value": update.message.text
    }
    state["buttons"].append(button_data)
    state["current_button"] += 1
    
    # Check if all buttons are configured
    if state["current_button"] >= state["button_count"]:
        # All buttons done - show confirmation
        state["step"] = "confirm"
        await show_confirmation(update, context)
    else:
        # Still more buttons - ask for next button type
        state["step"] = "button_config"
        await ask_button_config(update, context)

async def show_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show post preview and ask for confirmation"""
    user_id = str(update.effective_user.id)
    state = post_states[user_id]
    
    preview_text = "📋 Post Preview\n\n"
    
    if state.get("content_type") == "text":
        preview_text += f"📝 Text:\n{state['text']}\n\n"
    else:
        preview_text += f"🖼️ Media Type: {state['content_type']}\n"
        if state.get("caption"):
            preview_text += f"📝 Caption:\n{state['caption']}\n\n"
    
    if state.get("buttons"):
        preview_text += "🔘 Buttons:\n"
        for i, btn in enumerate(state["buttons"]):
            preview_text += f"  {i+1}. {btn['text']} → {btn['type']}: {btn['value']}\n"
    else:
        preview_text += "📌 No buttons\n"
    
    preview_text += "\n📤 Send to:\n• 📢 Channel: @saudi_1xbet_accounts\n• 👥 Group: (auto-synced via discussion)\n\n"
    preview_text += "Choose an option below:"
    
    keyboard = ReplyKeyboardMarkup([
        ["✅ Confirm & Post", "✏️ Edit Content"],
        ["🔘 Edit Buttons", "🔙 Cancel Post"]
    ], resize_keyboard=True)
    
    await update.message.reply_text(
        preview_text,
        parse_mode=None
    )
    
    await update.message.reply_text(
        "Choose an option:",
        reply_markup=keyboard
    )

async def confirm_and_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Post to channel only (Telegram handles discussion group automatically)"""
    user_id = str(update.effective_user.id)
    
    if user_id not in post_states:
        return
    
    state = post_states[user_id]
    
    # Build buttons
    keyboard = []
    for btn in state.get("buttons", []):
        button = None
        if btn["type"] == "url":
            button = InlineKeyboardButton(btn["text"], url=btn["value"])
        elif btn["type"] == "callback_data":
            button = InlineKeyboardButton(btn["text"], callback_data=btn["value"])
        elif btn["type"] == "web_app":
            button = InlineKeyboardButton(btn["text"], web_app={"url": btn["value"]})
        elif btn["type"] == "user":
            button = InlineKeyboardButton(btn["text"], url=f"tg://user?id={btn['value']}")
        elif btn["type"] == "bot":
            button = InlineKeyboardButton(btn["text"], url=f"t.me/{btn['value'].replace('@', '')}")
        elif btn["type"] == "switch_inline_query":
            button = InlineKeyboardButton(btn["text"], switch_inline_query=btn["value"])
        
        if button:
            keyboard.append([button])
    
    reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None
    
    # Prepare message
    if state["content_type"] == "text":
        text = state["text"]
        caption = None
    else:
        text = state.get("caption") or ""
        caption = text
        if len(caption) > 1000:
            caption = caption[:997] + "..."
        text = None
    
    # ============================================
    # SEND TO CHANNEL ONLY
    # ============================================
    try:
        if state["content_type"] == "text":
            await context.bot.send_message(
                chat_id="@saudi_1xbet_accounts",
                text=text,
                reply_markup=reply_markup,
                parse_mode=None
            )
        else:
            if state["content_type"] == "photo":
                await context.bot.send_photo(
                    chat_id="@saudi_1xbet_accounts",
                    photo=state["file_id"],
                    caption=caption,
                    reply_markup=reply_markup,
                    parse_mode=None
                )
            elif state["content_type"] == "video":
                await context.bot.send_video(
                    chat_id="@saudi_1xbet_accounts",
                    video=state["file_id"],
                    caption=caption,
                    reply_markup=reply_markup,
                    parse_mode=None
                )
            elif state["content_type"] == "document":
                await context.bot.send_document(
                    chat_id="@saudi_1xbet_accounts",
                    document=state["file_id"],
                    caption=caption,
                    reply_markup=reply_markup,
                    parse_mode=None
                )
        
        # ============================================
        # SUCCESS CONFIRMATION
        # ============================================
        await update.message.reply_text(
            f"✅ Post Published Successfully!\n\n"
            f"📢 Sent to:\n"
            f"• ✅ Channel: @saudi_1xbet_accounts\n"
            f"• ✅ Group: (auto-synced via discussion)\n\n"
            f"🔘 Buttons: {len(keyboard)}",
            parse_mode=None,
            reply_markup=get_admin_menu_keyboard(user_id)
        )
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}", parse_mode=None)
    
    # Clean up
    post_states.pop(user_id, None)

async def edit_content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Allow editing content"""
    user_id = str(update.effective_user.id)
    if user_id in post_states:
        post_states[user_id]["step"] = "content"
        await update.message.reply_text(
            "✏️ Edit Content\n\nSend the new content:",
            parse_mode=None
        )

async def edit_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reset button configuration"""
    user_id = str(update.effective_user.id)
    if user_id in post_states:
        post_states[user_id]["buttons"] = []
        post_states[user_id]["current_button"] = 0
        post_states[user_id]["step"] = "button_count"
        await update.message.reply_text(
            "✏️ Edit Buttons\n\nHow many buttons do you want? (0-9)",
            parse_mode=None,
            reply_markup=ReplyKeyboardMarkup(
                [["0", "1", "2", "3", "4", "5"], ["6", "7", "8", "9"]],
                resize_keyboard=True
            )
        )

async def cancel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the post creation"""
    user_id = str(update.effective_user.id)
    post_states.pop(user_id, None)
    await update.message.reply_text(
        "❌ Post Creation Cancelled!",
        parse_mode=None,
        reply_markup=get_admin_menu_keyboard(user_id)
    )

async def get_group_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get the ID of the group where command is sent"""
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"🆔 *Group ID:* `{chat_id}`", parse_mode="Markdown")

# ============================================
# MESSAGE HANDLER
# ============================================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    chat_id = update.effective_chat.id
    used_data = load_used()
    
    # ============================================
    # COMPLETELY IGNORE ALL MESSAGES IN THE GROUP
    # ============================================
    if chat_id == GROUP_CHAT_ID:
        # Only handle new member welcome messages
        if update.message and update.message.new_chat_members:
            # Let the welcome handler do its job
            pass
        # Ignore EVERYTHING else in the group - no replies, no buttons, nothing
        return
    
    await update.message.chat.send_action(action="typing")

    # ============================================
    # CASHBACK REQUEST FLOW
    # ============================================
    if user_id in cashback_requests:
        state = cashback_requests[user_id]
        step = state.get("step")
        if step == "waiting_for_player_id":
            await process_cashback_player_id_request(update, context)
            return

    # ============================================
    # POST CREATION FLOW
    # ============================================
    if user_id in post_states:
        state = post_states[user_id]
        step = state.get("step")
        
        if step == "content":
            await process_post_content(update, context)
            return
        elif step == "button_count":
            await process_button_count(update, context)
            return
        elif step == "button_config":
            await process_button_type(update, context)
            return
        elif step == "button_name":
            await process_button_name(update, context)
            return
        elif step == "button_value":
            await process_button_value(update, context)
            return
        elif step == "confirm":
            if update.message.text == "✅ Confirm & Post":
                await confirm_and_post(update, context)
                return
            elif update.message.text == "✏️ Edit Content":
                await edit_content(update, context)
                return
            elif update.message.text == "🔘 Edit Buttons":
                await edit_buttons(update, context)
                return
            elif update.message.text == "🔙 Cancel Post":
                await cancel_post(update, context)
                return

    # Admin states
    if user_id in admin_states:
        state = admin_states[user_id]
        action = state.get("action")
        if action == "delete_video":
            await handle_video_buttons(update, context)
            return
        elif action == "user_stats":
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
            await process_withdraw_amount(update, context)
            return

    if await process_rejection_reason(update, context):
        return

    # Video state check (add_video)
    if user_id in admin_states and admin_states[user_id].get("action") == "add_video":
        if update.message.video or (update.message.document and update.message.document.mime_type and update.message.document.mime_type.startswith('video/')):
            await handle_video_buttons(update, context)
            return
        elif update.message.text:
            if update.message.text.lower() == "/cancel":
                admin_states.pop(user_id, None)
                await update.message.reply_text(t(user_id, "rejection_cancelled"), parse_mode="Markdown", reply_markup=get_admin_video_keyboard(user_id))
                return
            else:
                await handle_video_buttons(update, context)
                return
        else:
            await update.message.reply_text(t(user_id, "please_send_video"), parse_mode="Markdown")
            return

    if update.message.photo:
        await handle_receipt(update, context)
        return

    message_text = update.message.text if update.message.text else ""

    if message_text == t(user_id, "back_to_menu"):
        admin_states.pop(user_id, None)
        post_states.pop(user_id, None)
        await show_main_menu(update, context)
        return

    # Admin: Add Post Button
    if message_text == "📝 Add Post":
        if update.effective_user.id != ADMIN_ID:
            await update.message.reply_text(t(user_id, "unauthorized"), parse_mode="Markdown")
            return
        await add_post(update, context)
        return

    # Cashback Request Button
    if message_text == "💰 Request Cashback":
        await cashback_request(update, context)
        return

    # Admin: Stats Menu
    if update.effective_user.id == ADMIN_ID:
        if message_text in [t(user_id, "overall_stats_button"), t(user_id, "user_stats_button"), t(user_id, "cashback_button")]:
            await handle_stats_buttons(update, context)
            return

    # Admin: Payment Methods Management
    if update.effective_user.id == ADMIN_ID:
        if user_id in admin_states:
            await handle_pm_state(update, context)
            return
        if message_text in [t(user_id, "list_methods"), t(user_id, "add_method"), t(user_id, "edit_method"), t(user_id, "delete_method")]:
            await handle_pm_buttons(update, context)
            return

    # Admin Commands from buttons
    if message_text == t(user_id, "add_accounts"):
        if update.effective_user.id != ADMIN_ID:
            await update.message.reply_text(t(user_id, "unauthorized"), parse_mode="Markdown")
            return
        await update.message.reply_text(t(user_id, "add_account_help"), parse_mode="Markdown")
        return

    if message_text == t(user_id, "stats"):
        if update.effective_user.id != ADMIN_ID:
            await update.message.reply_text(t(user_id, "unauthorized"), parse_mode="Markdown")
            return
        await show_stats_menu(update, context)
        return

    if message_text == t(user_id, "list_accounts"):
        if update.effective_user.id != ADMIN_ID:
            await update.message.reply_text(t(user_id, "unauthorized"), parse_mode="Markdown")
            return
        await list_accounts(update, context)
        return

    if message_text == t(user_id, "payment_methods"):
        if update.effective_user.id != ADMIN_ID:
            await update.message.reply_text(t(user_id, "unauthorized"), parse_mode="Markdown")
            return
        await manage_payment_methods(update, context)
        return

    # Video Tutorials
    if message_text == t(user_id, "video_tutorials"):
        await show_video_tutorials(update, context)
        return
    if message_text in [t(user_id, "add_video"), t(user_id, "delete_video"), t(user_id, "list_videos")] or message_text.startswith(("🎬 ", "🗑️ ")):
        await handle_video_buttons(update, context)
        return

    # Share Bot
    if message_text == t(user_id, "share_bot"):
        await handle_share_bot(update, context)
        return

    # User Features
    if message_text in [t(user_id, "get_account"), t(user_id, "get_another_account")]:
        await handle_get_account(update, user_id, used_data)
        return

    if message_text == t(user_id, "talk_to_agent"):
        keyboard = [[InlineKeyboardButton(t(user_id, "contact_agent_button"), url="https://t.me/Saudi_1xbet_agent")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            t(user_id, "contact_agent", agent_username=AGENT_USERNAME),
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
        return

    if message_text == t(user_id, "my_accounts"):
        await handle_my_accounts(update, user_id, used_data)
        return

    if message_text == t(user_id, "deposit_withdraw"):
        await show_deposit_withdraw_menu(update, context)
        return

    if message_text == t(user_id, "deposit"):
        await start_deposit(update, context)
        return

    if message_text == t(user_id, "withdraw"):
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

    # Default reply
    await update.message.reply_text(
        t(user_id, "unknown_command"),
        parse_mode="Markdown",
        reply_markup=get_main_menu_keyboard(user_id)
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
    bot_link = f"https://t.me/{bot_username}"
    
    keyboard = [[InlineKeyboardButton(t(user_id, "share_bot_button"), url=f"https://t.me/share/url?url={bot_link}&text=🎰%20Get%20FREE%201xBet%20accounts%20with%2030%25%20CASHBACK!%20Join%20now%3A%20{bot_link}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    share_text = t(user_id, "share_bot_title",
                   bot_username=bot_username,
                   share_count=share_count + 1,
                   bot_link=bot_link,
                   agent_username=AGENT_USERNAME)
    
    await update.message.reply_text(
        share_text,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

# ============================================
# STATS SYSTEM
# ============================================

async def show_stats_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text(t(user_id, "unauthorized"), parse_mode="Markdown")
        return
    await show_overall_stats(update, context)

async def handle_stats_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message_text = update.message.text
    if message_text == t(user_id, "overall_stats_button"):
        await show_overall_stats(update, context)
    elif message_text == t(user_id, "user_stats_button"):
        await show_user_stats(update, context)
    elif message_text == t(user_id, "cashback_button"):
        await show_cashback_calculator(update, context)

async def show_overall_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
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

    keyboard = get_stats_menu_keyboard(user_id)
    await update.message.reply_text(
        t(user_id, "overall_stats",
          available_accounts=len(accounts),
          total_users=total_users,
          total_accounts_given=total_accounts_given,
          today_given=today_given,
          deposits_accepted=deposits_accepted,
          deposits_rejected=deposits_rejected,
          total_deposit_amount=total_deposit_amount,
          withdrawals_accepted=withdrawals_accepted,
          withdrawals_rejected=withdrawals_rejected,
          total_withdraw_amount=total_withdraw_amount),
        parse_mode="Markdown",
        reply_markup=keyboard
    )

async def show_user_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    admin_states[user_id] = {"action": "user_stats", "step": "waiting_for_username"}
    await update.message.reply_text(
        t(user_id, "user_stats_prompt"),
        parse_mode="Markdown",
        reply_markup=get_back_to_menu_keyboard(user_id)
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
        await update.message.reply_text(
            t(user_id, "user_not_found", username=username_input),
            parse_mode="Markdown",
            reply_markup=get_stats_menu_keyboard(user_id)
        )
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
        t(user_id, "user_stats_result",
          username=found_username,
          total_accounts=total_accounts,
          given_today=given_today,
          deposits_accepted=deposits_accepted,
          deposits_rejected=deposits_rejected,
          total_deposit_amount=total_deposit_amount,
          withdrawals_accepted=withdrawals_accepted,
          withdrawals_rejected=withdrawals_rejected,
          total_withdraw_amount=total_withdraw_amount,
          share_count=share_count),
        parse_mode="Markdown",
        reply_markup=get_stats_menu_keyboard(user_id)
    )

# ============================================
# CASHBACK CALCULATOR (Admin)
# ============================================

async def show_cashback_calculator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    admin_states[user_id] = {"action": "cashback", "step": "waiting_for_player_id"}
    await update.message.reply_text(
        t(user_id, "cashback_title") + "\n\n" + t(user_id, "cashback_step1"),
        parse_mode="Markdown",
        reply_markup=get_back_to_menu_keyboard(user_id)
    )

async def process_cashback_player_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    player_id = update.message.text.strip()
    if not player_id.isdigit():
        await update.message.reply_text(t(user_id, "invalid_player_id"), parse_mode="Markdown")
        return
    admin_states[user_id]["player_id"] = player_id
    admin_states[user_id]["step"] = "waiting_for_start_date"
    await update.message.reply_text(
        t(user_id, "cashback_step2", player_id=player_id),
        parse_mode="Markdown",
        reply_markup=get_back_to_menu_keyboard(user_id)
    )

async def process_cashback_start_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    start_date = update.message.text.strip()
    try:
        datetime.strptime(start_date, "%Y-%m-%d")
    except ValueError:
        await update.message.reply_text(t(user_id, "invalid_date"), parse_mode="Markdown")
        return
    admin_states[user_id]["start_date"] = start_date
    admin_states[user_id]["step"] = "waiting_for_end_date"
    await update.message.reply_text(
        t(user_id, "cashback_step3", start_date=start_date),
        parse_mode="Markdown",
        reply_markup=get_back_to_menu_keyboard(user_id)
    )

async def process_cashback_end_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    end_date = update.message.text.strip()
    try:
        datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        await update.message.reply_text(t(user_id, "invalid_date"), parse_mode="Markdown")
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
        t(user_id, "cashback_result",
          player_id=player_id,
          start_date=start_date,
          end_date=end_date,
          deposits_count=deposits_count,
          total_deposits=total_deposits,
          withdrawals_count=withdrawals_count,
          total_withdrawals=total_withdrawals,
          net_amount=net_amount,
          percent=int(CASHBACK_PERCENT*100),
          cashback=cashback),
        parse_mode="Markdown",
        reply_markup=get_stats_menu_keyboard(user_id)
    )

# ============================================
# ACCOUNT HANDLING
# ============================================

async def handle_get_account(update, user_id, used_data):
    user_id_str = str(user_id)
    today_count = get_user_today_count(user_id_str, used_data)
    if today_count >= 2:
        await update.message.reply_text(
            t(user_id_str, "daily_limit_reached", today_count=today_count),
            parse_mode="Markdown",
            reply_markup=get_back_to_menu_keyboard(user_id_str)
        )
        return
    accounts = load_accounts()
    if not accounts:
        await update.message.reply_text(
            t(user_id_str, "no_accounts_available"),
            parse_mode="Markdown",
            reply_markup=get_back_to_menu_keyboard(user_id_str)
        )
        return
    account = accounts.pop(0)
    save_accounts(accounts)
    today = datetime.now().strftime("%Y-%m-%d")
    username = update.effective_user.username or "NoUsername"
    update_user_data(user_id_str, username, {"account": account, "date": today, "timestamp": datetime.now().isoformat()})
    remaining = len(accounts)
    parts = account.split(":", 1)
    account_display = f"*Username:* `{parts[0]}`\n*Password:* `{parts[1]}`" if len(parts) == 2 else f"`{account}`"
    await update.message.reply_text(
        t(user_id_str, "account_assigned",
          account_display=account_display,
          today_usage=get_user_today_count(user_id_str, used_data),
          remaining=remaining),
        parse_mode="Markdown",
        reply_markup=get_get_another_keyboard(user_id_str)
    )

async def handle_my_accounts(update, user_id, used_data):
    user_id_str = str(user_id)
    accounts = get_user_accounts(user_id_str, used_data)
    if not accounts:
        await update.message.reply_text(
            t(user_id_str, "no_accounts_found"),
            parse_mode="Markdown",
            reply_markup=get_back_to_menu_keyboard(user_id_str)
        )
        return
    formatted = []
    for acc in accounts:
        parts = acc.split(":", 1)
        formatted.append(f"• *Username:* `{parts[0]}`\n  *Password:* `{parts[1]}`" if len(parts) == 2 else f"• `{acc}`")
    await update.message.reply_text(
        t(user_id_str, "your_accounts",
          accounts_list='\n\n'.join(formatted),
          today_usage=get_user_today_count(user_id_str, used_data),
          total_accounts=len(accounts)),
        parse_mode="Markdown",
        reply_markup=get_get_another_keyboard(user_id_str)
    )

# ============================================
# VIDEO TUTORIALS
# ============================================

async def show_video_tutorials(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_id_str = str(user_id)
    videos = load_videos()
    if user_id == ADMIN_ID:
        keyboard = get_admin_video_keyboard(user_id)
        await update.message.reply_text(
            t(user_id, "video_admin_panel", total_videos=len(videos)),
            parse_mode="Markdown",
            reply_markup=keyboard
        )
        return
    if not videos:
        await update.message.reply_text(
            t(user_id, "video_tutorials_empty"),
            parse_mode="Markdown",
            reply_markup=get_back_to_menu_keyboard(user_id)
        )
        return
    keyboard = get_video_menu_keyboard(videos, user_id)
    video_list = "\n".join([f"🎬 {v['title']}" for v in videos.values()])
    text = t(user_id, "video_tutorials_title", video_list=video_list)
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=keyboard)

async def handle_video_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    message_text = update.message.text if update.message.text else ""
    videos = load_videos()

    if message_text == t(user_id, "back_to_menu"):
        admin_states.pop(user_id, None)
        await show_main_menu(update, context)
        return

    if message_text == t(user_id, "add_video"):
        if update.effective_user.id != ADMIN_ID:
            await update.message.reply_text(t(user_id, "unauthorized"), parse_mode="Markdown")
            return
        admin_states[user_id] = {"action": "add_video", "step": "waiting_for_video"}
        await update.message.reply_text(
            t(user_id, "add_video_step1"),
            parse_mode="Markdown",
            reply_markup=get_back_to_menu_keyboard(user_id)
        )
        return

    if message_text == t(user_id, "delete_video"):
        if update.effective_user.id != ADMIN_ID:
            await update.message.reply_text(t(user_id, "unauthorized"), parse_mode="Markdown")
            return
        if not videos:
            await update.message.reply_text(t(user_id, "no_videos_to_delete"), parse_mode="Markdown")
            return
        keyboard = [[KeyboardButton(f"🗑️ {v['title']}")] for v in videos.values()] + [[t(user_id, "back_to_menu")]]
        admin_states[user_id] = {"action": "delete_video", "step": "select"}
        await update.message.reply_text(
            t(user_id, "delete_video_prompt"),
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
        return

    if message_text == t(user_id, "list_videos"):
        if update.effective_user.id != ADMIN_ID:
            await update.message.reply_text(t(user_id, "unauthorized"), parse_mode="Markdown")
            return
        if not videos:
            await update.message.reply_text(t(user_id, "no_videos"), parse_mode="Markdown")
            return
        video_list = "\n".join([t(user_id, "video_list_item", vid=vid, title=data['title'], date=data.get('created_at', 'Unknown')) for vid, data in videos.items()])
        await update.message.reply_text(t(user_id, "video_list_title", video_list=video_list), parse_mode="Markdown")
        return

    # Delete logic
    if message_text.startswith("🗑️ "):
        if user_id in admin_states and admin_states[user_id].get("action") == "delete_video":
            title = message_text.replace("🗑️ ", "")
            found = False
            for vid, data in videos.items():
                if data['title'] == title:
                    del videos[vid]
                    save_videos(videos)
                    admin_states.pop(user_id, None)
                    found = True
                    await update.message.reply_text(
                        t(user_id, "delete_video_success", title=title),
                        parse_mode="Markdown",
                        reply_markup=get_admin_video_keyboard(user_id)
                    )
                    break
            if not found:
                await update.message.reply_text(t(user_id, "delete_video_not_found", title=title), parse_mode="Markdown")
        else:
            await update.message.reply_text(t(user_id, "video_not_in_delete_mode"), parse_mode="Markdown")
        return

    # Play video
    if message_text.startswith("🎬 "):
        title = message_text.replace("🎬 ", "")
        for data in videos.values():
            if data['title'] == title:
                try:
                    caption = t(user_id, "video_play_caption", title=data['title'], date=data.get('created_at', 'Unknown'))
                    await update.message.reply_video(video=data['file_id'], caption=caption, parse_mode="Markdown")
                    return
                except Exception as e:
                    print(f"Error sending video: {e}")
                    await update.message.reply_text(t(user_id, "error_sending_video"), parse_mode="Markdown")
                    return
        await update.message.reply_text(t(user_id, "video_not_found"), parse_mode="Markdown")
        return

    # Add video state
    if user_id in admin_states and admin_states[user_id].get("action") == "add_video":
        state = admin_states[user_id]
        step = state.get("step")
        if step == "waiting_for_video":
            if update.message.video:
                state["file_id"] = update.message.video.file_id
                state["step"] = "waiting_for_title"
                await update.message.reply_text(
                    t(user_id, "add_video_step2"),
                    parse_mode="Markdown",
                    reply_markup=get_back_to_menu_keyboard(user_id)
                )
                return
            elif update.message.document and update.message.document.mime_type and update.message.document.mime_type.startswith('video/'):
                state["file_id"] = update.message.document.file_id
                state["step"] = "waiting_for_title"
                await update.message.reply_text(
                    t(user_id, "add_video_step2"),
                    parse_mode="Markdown",
                    reply_markup=get_back_to_menu_keyboard(user_id)
                )
                return
            else:
                await update.message.reply_text(t(user_id, "please_send_video"), parse_mode="Markdown")
                return
        elif step == "waiting_for_title":
            title = message_text.strip()
            if len(title) < 3:
                await update.message.reply_text(t(user_id, "add_video_title_short"), parse_mode="Markdown")
                return
            for data in videos.values():
                if data['title'].lower() == title.lower():
                    await update.message.reply_text(t(user_id, "add_video_exists", title=title), parse_mode="Markdown")
                    return
            vid = f"VID_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            videos[vid] = {"title": title, "file_id": state.get("file_id"), "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            save_videos(videos)
            admin_states.pop(user_id, None)
            await update.message.reply_text(
                t(user_id, "add_video_success", title=title, vid=vid, total_videos=len(videos)),
                parse_mode="Markdown",
                reply_markup=get_admin_video_keyboard(user_id)
            )
            return

    # Fallback
    await update.message.reply_text(t(user_id, "unknown_video_action"), parse_mode="Markdown", reply_markup=get_back_to_menu_keyboard(user_id))

# ============================================
# DEPOSIT & WITHDRAW SYSTEM
# ============================================

async def show_deposit_withdraw_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await update.message.reply_text(
        t(user_id, "deposit_withdraw_menu"),
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup([[t(user_id, "deposit"), t(user_id, "withdraw")], [t(user_id, "back_to_menu")]], resize_keyboard=True)
    )

# --- Deposit Flow ---

async def start_deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    user_states[user_id] = {"action": "deposit", "step": "player_id"}
    await update.message.reply_text(
        t(user_id, "deposit_start"),
        parse_mode="Markdown",
        reply_markup=get_back_to_menu_keyboard(user_id)
    )

async def process_deposit_player_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    player_id = update.message.text.strip()
    if not player_id.isdigit():
        await update.message.reply_text(t(user_id, "invalid_player_id"), parse_mode="Markdown")
        return
    user_states[user_id]["player_id"] = player_id
    user_states[user_id]["step"] = "method"
    methods = load_payment_methods()
    keyboard = [[KeyboardButton(m["name"])] for m in methods.values()] + [[t(user_id, "back_to_menu")]]
    await update.message.reply_text(
        t(user_id, "deposit_player_id", player_id=player_id),
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
        await update.message.reply_text(t(user_id, "invalid_method"), parse_mode="Markdown")
        return
    user_states[user_id]["method"] = method_key
    user_states[user_id]["step"] = "amount"
    method = methods[method_key]
    details_text = "\n".join([f"📋 {field}: {value}" for field, value in method["details"].items()])
    keyboard = [
        ["10 SAR", "25 SAR", "50 SAR"],
        ["100 SAR", "200 SAR", "500 SAR"],
        [t(user_id, "custom_amount")],
        [t(user_id, "back_to_menu")]
    ]
    await update.message.reply_text(
        t(user_id, "deposit_method",
          player_id=user_states[user_id]['player_id'],
          method_name=method_name,
          details=details_text),
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

async def process_deposit_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    amount_text = update.message.text.replace(" SAR", "").strip()
    if amount_text == t(user_id, "custom_amount"):
        await update.message.reply_text(t(user_id, "enter_amount"), parse_mode="Markdown")
        return
    try:
        amount = float(amount_text)
        if amount < 10 or amount > 500:
            await update.message.reply_text(t(user_id, "deposit_invalid_amount"), parse_mode="Markdown")
            return
    except ValueError:
        await update.message.reply_text(t(user_id, "deposit_invalid_number"), parse_mode="Markdown")
        return
    user_states[user_id]["amount"] = amount
    user_states[user_id]["step"] = "receipt"
    methods = load_payment_methods()
    method_name = methods[user_states[user_id]["method"]]["name"]
    await update.message.reply_text(
        t(user_id, "deposit_amount",
          player_id=user_states[user_id]['player_id'],
          method_name=method_name,
          amount=amount),
        parse_mode="Markdown"
    )

async def handle_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id not in user_states or user_states[user_id].get("action") != "deposit" or user_states[user_id].get("step") != "receipt":
        return
    if not update.message.photo:
        await update.message.reply_text(t(user_id, "please_send_photo"), parse_mode="Markdown")
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
        t(user_id, "deposit_receipt_received"),
        parse_mode="Markdown",
        reply_markup=get_back_to_menu_keyboard(user_id)
    )
    await notify_accountant_deposit(update, context, deposit_id, deposits[deposit_id])

async def notify_accountant_deposit(update, context, deposit_id, deposit_data):
    admin_id = ACCOUNTANT_ID
    methods = load_payment_methods()
    method_name = methods[deposit_data["method"]]["name"]
    keyboard = [
        [InlineKeyboardButton(t(admin_id, "deposit_accept"), callback_data=f"deposit_accept_{deposit_id}"),
         InlineKeyboardButton(t(admin_id, "deposit_reject"), callback_data=f"deposit_reject_{deposit_id}")]
    ]
    message = t(admin_id, "new_deposit",
                deposit_id=deposit_id,
                username=deposit_data['username'],
                player_id=deposit_data['player_id'],
                method_name=method_name,
                amount=deposit_data['amount'],
                created_at=deposit_data['created_at'])
    await context.bot.send_message(chat_id=ACCOUNTANT_ID, text=message, parse_mode=None, reply_markup=InlineKeyboardMarkup(keyboard))
    if os.path.exists(deposit_data['receipt']):
        with open(deposit_data['receipt'], 'rb') as photo:
            caption = t(admin_id, "receipt_caption", deposit_id=deposit_id)
            await context.bot.send_photo(chat_id=ACCOUNTANT_ID, photo=photo, caption=caption)

# --- Withdraw Flow ---

async def start_withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    user_states[user_id] = {"action": "withdraw", "step": "method"}
    methods = load_payment_methods()
    keyboard = [[KeyboardButton(m["name"])] for m in methods.values()] + [[t(user_id, "back_to_menu")]]
    await update.message.reply_text(
        t(user_id, "withdraw_start"),
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
        await update.message.reply_text(t(user_id, "invalid_method"), parse_mode="Markdown")
        return
    user_states[user_id]["method"] = method_key
    user_states[user_id]["step"] = "player_id"
    await update.message.reply_text(
        t(user_id, "withdraw_player_id"),
        parse_mode="Markdown",
        reply_markup=get_back_to_menu_keyboard(user_id)
    )

async def process_withdraw_player_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    player_id = update.message.text.strip()
    if not player_id.isdigit():
        await update.message.reply_text(t(user_id, "invalid_player_id"), parse_mode="Markdown")
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
        t(user_id, "withdraw_details", field=field, field_lower=field.lower()),
        parse_mode="Markdown",
        reply_markup=get_back_to_menu_keyboard(user_id)
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
    videos = load_videos()
    for data in videos.values():
        if "Withdrawal" in data['title'] or "withdrawal" in data['title'].lower():
            try:
                caption = t(user_id, "withdraw_video_caption", title=data['title'])
                await update.message.reply_video(video=data['file_id'], caption=caption, parse_mode="Markdown")
            except Exception as e:
                print(f"Error sending withdrawal video: {e}")
            break
    await update.message.reply_text(
        t(user_id, "withdraw_code"),
        parse_mode="Markdown",
        reply_markup=get_back_to_menu_keyboard(user_id)
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
        t(user_id, "withdraw_code_entered"),
        parse_mode="Markdown",
        reply_markup=get_back_to_menu_keyboard(user_id)
    )
    await notify_accountant_withdraw(update, context, withdraw_id, withdrawals[withdraw_id])

async def notify_accountant_withdraw(update, context, withdraw_id, withdraw_data):
    try:
        admin_id = ACCOUNTANT_ID
        methods = load_payment_methods()
        method_name = methods[withdraw_data["method"]]["name"]
        details_text = "\n".join([f"• {k}: {v}" for k, v in withdraw_data["details"].items()])
        keyboard = [
            [InlineKeyboardButton(t(admin_id, "withdraw_accept"), callback_data=f"withdraw_accept_{withdraw_id}"),
             InlineKeyboardButton(t(admin_id, "withdraw_reject"), callback_data=f"withdraw_reject_{withdraw_id}")]
        ]
        message = t(admin_id, "new_withdraw",
                    withdraw_id=withdraw_id,
                    username=withdraw_data['username'],
                    player_id=withdraw_data.get('player_id', 'N/A'),
                    method_name=method_name,
                    details=details_text,
                    code=withdraw_data['code'],
                    created_at=withdraw_data['created_at'])
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
    admin_id = update.effective_user.id

    if type_ == "deposit":
        deposits = load_deposits()
        if request_id not in deposits:
            await query.edit_message_text(t(admin_id, "deposit_not_found"))
            return
        if action == "accept":
            deposits[request_id]["status"] = "completed"
            save_deposits(deposits)
            user_id = deposits[request_id]["user_id"]
            await context.bot.send_message(
                chat_id=user_id,
                text=t(user_id, "deposit_confirmed", amount=deposits[request_id]['amount']),
                parse_mode="Markdown"
            )
            await query.edit_message_text(t(admin_id, "deposit_accept_success"))
        else:
            context.user_data["reject_deposit"] = request_id
            await query.edit_message_text(t(admin_id, "deposit_reject_prompt", request_id=request_id), parse_mode="Markdown")

    elif type_ == "withdraw":
        withdrawals = load_withdrawals()
        if request_id not in withdrawals:
            await query.edit_message_text(t(admin_id, "withdraw_not_found"))
            return
        if action == "accept":
            admin_states[str(admin_id)] = {
                "action": "withdraw_amount",
                "withdraw_id": request_id
            }
            await query.edit_message_text(
                t(admin_id, "withdraw_accept_prompt", request_id=request_id),
                parse_mode="Markdown"
            )
        else:
            context.user_data["reject_withdraw"] = request_id
            await query.edit_message_text(t(admin_id, "withdraw_reject_prompt", request_id=request_id), parse_mode="Markdown")

async def process_withdraw_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    amount_text = update.message.text.strip()
    try:
        amount = float(amount_text)
        if amount <= 0:
            raise ValueError
    except ValueError:
        await update.message.reply_text(t(user_id, "withdraw_amount_invalid"), parse_mode="Markdown")
        return

    state = admin_states.get(user_id)
    if not state or state.get("action") != "withdraw_amount":
        await update.message.reply_text(t(user_id, "withdraw_amount_session_expired"), parse_mode="Markdown")
        return

    withdraw_id = state.get("withdraw_id")
    withdrawals = load_withdrawals()
    if withdraw_id not in withdrawals:
        await update.message.reply_text(t(user_id, "withdraw_not_found"), parse_mode="Markdown")
        admin_states.pop(user_id, None)
        return

    withdrawals[withdraw_id]["amount"] = amount
    withdrawals[withdraw_id]["status"] = "completed"
    save_withdrawals(withdrawals)
    admin_states.pop(user_id, None)

    user_id_user = withdrawals[withdraw_id]["user_id"]
    await context.bot.send_message(
        chat_id=user_id_user,
        text=t(user_id, "withdraw_confirmed", amount=amount),
        parse_mode="Markdown"
    )
    await update.message.reply_text(
        t(user_id, "withdraw_accept_success", withdraw_id=withdraw_id, amount=amount),
        parse_mode="Markdown"
    )

async def process_rejection_reason(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # Cashback rejection
    if "reject_cashback" in context.user_data:
        return await process_cashback_rejection_reason(update, context)
    
    if "reject_deposit" in context.user_data:
        request_id = context.user_data.pop("reject_deposit")
        deposits = load_deposits()
        if request_id in deposits and update.message.text:
            reason = update.message.text
            deposits[request_id]["status"] = "rejected"
            deposits[request_id]["reason"] = reason
            save_deposits(deposits)
            user_id_user = deposits[request_id]["user_id"]
            await context.bot.send_message(
                chat_id=user_id_user,
                text=t(user_id_user, "deposit_rejected", amount=deposits[request_id]['amount'], reason=reason),
                parse_mode="Markdown"
            )
            await update.message.reply_text(t(user_id, "rejection_sent"), reply_markup=get_pm_menu_keyboard(user_id) if update.effective_user.id == ADMIN_ID else get_main_menu_keyboard(user_id))
            return True
        else:
            await update.message.reply_text(t(user_id, "rejection_prompt"), parse_mode="Markdown")
            return True

    if "reject_withdraw" in context.user_data:
        request_id = context.user_data.pop("reject_withdraw")
        withdrawals = load_withdrawals()
        if request_id in withdrawals and update.message.text:
            reason = update.message.text
            withdrawals[request_id]["status"] = "rejected"
            withdrawals[request_id]["reason"] = reason
            save_withdrawals(withdrawals)
            user_id_user = withdrawals[request_id]["user_id"]
            await context.bot.send_message(
                chat_id=user_id_user,
                text=t(user_id_user, "withdraw_rejected", reason=reason),
                parse_mode="Markdown"
            )
            await update.message.reply_text(t(user_id, "rejection_sent"), reply_markup=get_pm_menu_keyboard(user_id) if update.effective_user.id == ADMIN_ID else get_main_menu_keyboard(user_id))
            return True
        else:
            await update.message.reply_text(t(user_id, "rejection_prompt"), parse_mode="Markdown")
            return True

    return False

# ============================================
# PAYMENT METHODS MANAGEMENT
# ============================================

async def manage_payment_methods(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text(t(user_id, "unauthorized"), parse_mode="Markdown")
        return
    admin_states.pop(str(user_id), None)
    await update.message.reply_text(
        t(user_id, "pm_management"),
        parse_mode="Markdown",
        reply_markup=get_pm_menu_keyboard(user_id)
    )

async def handle_pm_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    message_text = update.message.text
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text(t(user_id, "unauthorized"), parse_mode="Markdown")
        return
    if user_id in admin_states:
        await handle_pm_state(update, context)
        return
    methods = load_payment_methods()

    if message_text == t(user_id, "list_methods"):
        if not methods:
            await update.message.reply_text(t(user_id, "no_methods"), parse_mode="Markdown")
            return
        methods_text = ""
        for key, method in methods.items():
            details = "\n".join([f"   📋 {f}: {v}" for f, v in method["details"].items()])
            methods_text += f"🔹 *{method['name']}*\n   📌 ID: `{key}`\n   📝 Fields: {', '.join(method['fields'])}\n{details}\n\n"
        await update.message.reply_text(t(user_id, "pm_list", methods_list=methods_text), parse_mode="Markdown")
        return

    elif message_text == t(user_id, "add_method"):
        admin_states[user_id] = {"action": "add", "step": "key"}
        await update.message.reply_text(
            t(user_id, "add_method_step1"),
            parse_mode="Markdown",
            reply_markup=get_back_to_menu_keyboard(user_id)
        )
        return

    elif message_text == t(user_id, "edit_method"):
        if not methods:
            await update.message.reply_text(t(user_id, "no_methods"), parse_mode="Markdown")
            return
        keyboard = [[KeyboardButton(key)] for key in methods.keys()] + [[t(user_id, "back_to_menu")]]
        admin_states[user_id] = {"action": "edit", "step": "select"}
        await update.message.reply_text(
            t(user_id, "edit_method_prompt"),
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
        return

    elif message_text == t(user_id, "delete_method"):
        if not methods:
            await update.message.reply_text(t(user_id, "no_methods"), parse_mode="Markdown")
            return
        keyboard = [[KeyboardButton(key)] for key in methods.keys()] + [[t(user_id, "back_to_menu")]]
        admin_states[user_id] = {"action": "delete", "step": "select"}
        await update.message.reply_text(
            t(user_id, "delete_method_prompt"),
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
        return

async def handle_pm_state(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    message_text = update.message.text
    state = admin_states[user_id]
    action = state.get("action")
    step = state.get("step")
    methods = load_payment_methods()

    if message_text in [t(user_id, "back_to_menu"), "/cancel"]:
        admin_states.pop(user_id, None)
        await update.message.reply_text(t(user_id, "rejection_cancelled"), parse_mode="Markdown", reply_markup=get_pm_menu_keyboard(user_id))
        return

    if action == "add":
        if step == "key":
            if not re.match(r'^[a-zA-Z0-9_]+$', message_text):
                await update.message.reply_text(t(user_id, "invalid_id"), parse_mode="Markdown")
                return
            if message_text in methods:
                await update.message.reply_text(t(user_id, "id_exists", id=message_text), parse_mode="Markdown")
                return
            state["key"] = message_text
            state["step"] = "name"
            await update.message.reply_text(
                t(user_id, "add_method_step2", key=message_text),
                parse_mode="Markdown",
                reply_markup=get_back_to_menu_keyboard(user_id)
            )
            return
        elif step == "name":
            state["name"] = message_text
            state["step"] = "fields_count"
            await update.message.reply_text(
                t(user_id, "add_method_step3", name=message_text),
                parse_mode="Markdown",
                reply_markup=ReplyKeyboardMarkup([["1", "2", "3"], ["4", "5"], [t(user_id, "back_to_menu")]], resize_keyboard=True)
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
                    t(user_id, "add_method_step4", count=count, index=state['field_index']+1, examples=field_labels.get(0, '')),
                    parse_mode="Markdown",
                    reply_markup=get_back_to_menu_keyboard(user_id)
                )
                return
            except ValueError:
                await update.message.reply_text(t(user_id, "invalid_number"), parse_mode="Markdown")
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
                    t(user_id, "add_method_step5", fields=', '.join(state['fields']), field=state['fields'][0]),
                    parse_mode="Markdown",
                    reply_markup=get_back_to_menu_keyboard(user_id)
                )
                return
            field_labels = {0: "📱 Phone number", 1: "🏦 IBAN", 2: "🏛️ Bank name", 3: "🔗 Wallet address", 4: "👤 Full name", 5: "📧 Email"}
            await update.message.reply_text(
                t(user_id, "add_method_step6", field=field),
                parse_mode="Markdown",
                reply_markup=get_back_to_menu_keyboard(user_id)
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
                values_text = "\n".join([f"   {f}: {v}" for f, v in state["values"].items()])
                await update.message.reply_text(
                    t(user_id, "add_method_success",
                      name=state['name'],
                      key=key,
                      fields=', '.join(state['fields']),
                      values=values_text),
                    parse_mode="Markdown",
                    reply_markup=get_pm_menu_keyboard(user_id)
                )
                return
            await update.message.reply_text(
                t(user_id, "add_method_step6", field=state['fields'][state['value_index']]),
                parse_mode="Markdown",
                reply_markup=get_back_to_menu_keyboard(user_id)
            )
            return

    # EDIT METHOD FLOW
    elif action == "edit":
        if step == "select":
            if message_text not in methods:
                await update.message.reply_text(t(user_id, "method_not_found", key=message_text), parse_mode="Markdown")
                return
            state["edit_key"] = message_text
            state["step"] = "field"
            method = methods[message_text]
            keyboard = [[KeyboardButton(f)] for f in ["name", "fields", "details"] + list(method["details"].keys())] + [[t(user_id, "back_to_menu")]]
            await update.message.reply_text(
                t(user_id, "edit_method_selected",
                  name=method['name'],
                  key=message_text,
                  fields=', '.join(method['fields']),
                  details=str(method['details'])),
                parse_mode="Markdown",
                reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            )
            return
        elif step == "field":
            if message_text not in ["name", "fields", "details"] and message_text not in methods[state["edit_key"]]["details"]:
                await update.message.reply_text(t(user_id, "field_not_found", field=message_text), parse_mode="Markdown")
                return
            state["edit_field"] = message_text
            state["step"] = "value"
            current = methods[state["edit_key"]].get(message_text, "N/A")
            await update.message.reply_text(
                t(user_id, "edit_method_field", field=state['edit_field'], current=current),
                parse_mode="Markdown",
                reply_markup=get_back_to_menu_keyboard(user_id)
            )
            return
        elif step == "value":
            key = state["edit_key"]
            field = state["edit_field"]
            if field == "fields":
                fields = [f.strip() for f in message_text.replace(",", " ").split() if f.strip()]
                if fields:
                    methods[key]["fields"] = fields
                else:
                    await update.message.reply_text(t(user_id, "invalid_fields"), parse_mode="Markdown")
                    return
            elif field == "details":
                await update.message.reply_text(t(user_id, "edit_details_not_allowed"), parse_mode="Markdown")
                return
            else:
                methods[key][field] = message_text
            save_payment_methods(methods)
            admin_states.pop(user_id, None)
            await update.message.reply_text(
                t(user_id, "edit_method_success", key=key, field=field, value=message_text),
                parse_mode="Markdown",
                reply_markup=get_pm_menu_keyboard(user_id)
            )
            return

    # DELETE METHOD FLOW
    elif action == "delete":
        if step == "select":
            if message_text not in methods:
                await update.message.reply_text(t(user_id, "method_not_found", key=message_text), parse_mode="Markdown")
                return
            state["delete_key"] = message_text
            state["step"] = "confirm"
            method = methods[message_text]
            await update.message.reply_text(
                t(user_id, "delete_method_confirm", name=method['name'], key=message_text),
                parse_mode="Markdown",
                reply_markup=ReplyKeyboardMarkup([[t(user_id, "delete_method_yes")], [t(user_id, "delete_method_no")]], resize_keyboard=True)
            )
            return
        elif step == "confirm":
            if message_text == t(user_id, "delete_method_yes"):
                key = state["delete_key"]
                del methods[key]
                save_payment_methods(methods)
                admin_states.pop(user_id, None)
                await update.message.reply_text(t(user_id, "delete_method_success", key=key), parse_mode="Markdown", reply_markup=get_pm_menu_keyboard(user_id))
            else:
                admin_states.pop(user_id, None)
                await update.message.reply_text(t(user_id, "delete_method_cancelled"), parse_mode="Markdown", reply_markup=get_pm_menu_keyboard(user_id))
            return

# ============================================
# ADMIN COMMANDS
# ============================================

async def add_account_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text(t(user_id, "unauthorized"), parse_mode="Markdown")
        return
    if not context.args:
        await update.message.reply_text(t(user_id, "add_account_help"), parse_mode="Markdown")
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
            await update.message.reply_text(t(user_id, "add_account_invalid"), parse_mode="Markdown")
            return
    new_accounts = []
    for username, password in matches:
        username = username.strip()
        password = password.strip()
        if username and password:
            new_accounts.append(f"{username}:{password}")
    if not new_accounts:
        await update.message.reply_text(t(user_id, "add_account_no_valid"), parse_mode="Markdown")
        return
    current_accounts = load_accounts()
    current_accounts.extend(new_accounts)
    save_accounts(current_accounts)
    added_text = "\n".join([f"• *Username:* `{u.split(':',1)[0]}`\n   *Password:* `{u.split(':',1)[1]}`" for u in new_accounts])
    await update.message.reply_text(
        t(user_id, "add_account_success",
          count=len(new_accounts),
          accounts=added_text,
          total=len(current_accounts)),
        parse_mode="Markdown"
    )

async def list_accounts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text(t(user_id, "unauthorized"), parse_mode="Markdown")
        return
    accounts = load_accounts()
    if not accounts:
        await update.message.reply_text(t(user_id, "no_accounts_to_list"), parse_mode="Markdown")
        return
    formatted = []
    for i, acc in enumerate(accounts):
        parts = acc.split(":", 1)
        formatted.append(f"{i+1}. *Username:* `{parts[0]}`\n   *Password:* `{parts[1]}`" if len(parts) == 2 else f"{i+1}. `{acc}`")
    await update.message.reply_text(
        t(user_id, "accounts_list_admin", count=len(accounts), accounts='\n\n'.join(formatted)),
        parse_mode="Markdown"
    )

async def delete_account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text(t(user_id, "unauthorized"), parse_mode="Markdown")
        return
    if not context.args:
        await update.message.reply_text(t(user_id, "delete_account_help"), parse_mode="Markdown")
        return
    match = re.search(r'Username:\s*([^,]+)', " ".join(context.args), re.IGNORECASE)
    if not match:
        await update.message.reply_text(t(user_id, "delete_account_invalid"), parse_mode="Markdown")
        return
    username = match.group(1).strip()
    accounts = load_accounts()
    account_to_delete = next((a for a in accounts if a.startswith(f"{username}:")), None)
    if not account_to_delete:
        await update.message.reply_text(t(user_id, "delete_account_not_found", username=username), parse_mode="Markdown")
        return
    accounts.remove(account_to_delete)
    save_accounts(accounts)
    await update.message.reply_text(
        t(user_id, "delete_account_success", account=account_to_delete, total=len(accounts)),
        parse_mode="Markdown"
    )

async def clear_accounts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text(t(user_id, "unauthorized"), parse_mode="Markdown")
        return
    accounts = load_accounts()
    if not accounts:
        await update.message.reply_text(t(user_id, "no_accounts_to_clear"), parse_mode="Markdown")
        return
    count = len(accounts)
    save_accounts([])
    await update.message.reply_text(t(user_id, "clear_accounts_confirm", count=count), parse_mode="Markdown")

async def reset_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text(t(user_id, "unauthorized"), parse_mode="Markdown")
        return
    if not context.args:
        await update.message.reply_text(t(user_id, "reset_user_help"), parse_mode="Markdown")
        return
    target_user = context.args[0]
    used_data = load_used()
    if target_user in used_data:
        del used_data[target_user]
        save_used(used_data)
        await update.message.reply_text(t(user_id, "reset_user_success", user_id=target_user), parse_mode="Markdown")
    else:
        await update.message.reply_text(t(user_id, "reset_user_not_found", user_id=target_user), parse_mode="Markdown")

# ============================================
# MAIN FUNCTION
# ============================================

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("language", language_command))
    app.add_handler(CommandHandler("ass", add_account_command))
    app.add_handler(CommandHandler("add", add_account_command))
    app.add_handler(CommandHandler("stats", show_stats_menu))
    app.add_handler(CommandHandler("listaccounts", list_accounts))
    app.add_handler(CommandHandler("resetuser", reset_user))
    app.add_handler(CommandHandler("del", delete_account))
    app.add_handler(CommandHandler("clearaccounts", clear_accounts))
    app.add_handler(CommandHandler("pm", manage_payment_methods))
    app.add_handler(CommandHandler("getid", get_group_id))
    app.add_handler(CommandHandler("addpost", add_post))
    app.add_handler(CommandHandler("cancelpost", cancel_post))

    # ============================================
    # GROUP WELCOME HANDLER
    # ============================================
    app.add_handler(MessageHandler(
        filters.StatusUpdate.NEW_CHAT_MEMBERS, 
        welcome_new_member
    ))

    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_message))
    app.add_handler(MessageHandler(filters.VIDEO, handle_message))
    app.add_handler(MessageHandler(filters.Document.VIDEO, handle_message))

    print("=" * 50)
    print("🤖 Saudi 1xBet Bot is RUNNING with multi-language support!")
    print("📱 Bot username: @Saudi_1xBet_bot")
    print("=" * 50)
    print("✅ Waiting for users...")
    print("Press Ctrl+C to stop the bot")
    print("=" * 50)

    app.run_polling()

if __name__ == "__main__":
    main()
