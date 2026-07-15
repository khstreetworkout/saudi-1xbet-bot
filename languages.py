# languages.py
# All user-visible text in English and Arabic

LANGUAGES = {
    "en": {
        # Bot name and welcome
        "bot_name": "Saudi 1xBet Bot",
        "welcome_title": "🎰 *Welcome to Saudi 1xBet Bot!*",
        "welcome_text": "🎰 *Welcome to Saudi 1xBet Bot!*\n\n💰 *Get 30% CASHBACK on all losses!*\n📌 You can get up to *2 accounts per day*\n💳 *Deposit & Withdraw easily!*\n\n👆 Click the buttons below:",
        "admin_welcome": "🎰 *Welcome Admin!*\n\n👑 *Admin Panel*\n➕ `/ass` - Add accounts\n📊 `/stats` - View statistics\n📋 `/listaccounts` - View all accounts\n💳 `/pm` - Payment Methods\n\n📌 *User Features:*\n💰 *Get 30% CASHBACK on all losses!*\n📌 You can get up to *2 accounts per day*\n💳 *Deposit & Withdraw easily!*\n\n👆 Click the buttons below:",
        
        # Language selection
        "language_selection": "🌍 *Select your language / اختر لغتك*\n\nPlease choose your preferred language:",
        "english": "🇬🇧 English",
        "arabic": "🇸🇦 العربية",
        "language_saved": "✅ *Language saved!* You will now see all messages in English.",
        "language_saved_ar": "✅ *تم حفظ اللغة!* ستظهر جميع الرسائل الآن باللغة العربية.",
        
        # Main menu buttons
        "get_account": "🎰 Get Account",
        "talk_to_agent": "💬 Talk to Agent",
        "my_accounts": "📋 My Accounts",
        "deposit_withdraw": "💳 Deposit & Withdraw",
        "video_tutorials": "📹 Video Tutorials",
        "share_bot": "📢 Share Bot",
        "back_to_menu": "🔙 Back to Menu",
        "get_another_account": "🎰 Get Another Account",
        
        # Admin buttons
        "stats": "📊 /stats",
        "list_accounts": "📋 /listaccounts",
        "add_accounts": "➕ /ass",
        "payment_methods": "💳 /pm",
        
        # Subscription check
        "join_channel": "👋 *Welcome!*\n\nTo use this bot, you must first join our channel:\n➡️ [1xbet Saudi Arabia](https://t.me/saudi_1xbet_accounts)\n\nAfter joining, click the button below to continue.",
        "join_channel_button": "📢 Join Our Channel",
        "check_subscription": "✅ I've Joined! Check Subscription",
        "not_member": "❌ *Not a member yet!*\n\nPlease join [our channel](https://t.me/saudi_1xbet_accounts) first, then click 'Check Subscription' again.",
        "subscription_verified": "✅ Subscription verified! Welcome!",
        
        # Account related
        "daily_limit_reached": "❌ *Daily Limit Reached!*\n\nYou've already received *{today_count}* accounts today.\nMaximum is *2 accounts per day*.\n\n⏳ Please try again tomorrow.\n📋 Use 'My Accounts' to see your accounts.",
        "no_accounts_available": "❌ *No Accounts Available!*\n\nAll accounts have been distributed.\nPlease check back later or contact our agent.",
        "account_assigned": "✅ *Account Assigned!*\n\n{account_display}\n\n💰 *30% CASHBACK on all losses!*\n\n📊 *Today's Usage:* {today_usage}/2\n📦 *Accounts Remaining:* {remaining}\n\n💡 *Tap to copy!*\n🔒 Save it securely.",
        "no_accounts_found": "📋 *No Accounts Found*\n\nUse 'Get Account' to get your first one!",
        "your_accounts": "📋 *Your Accounts*\n\n{accounts_list}\n\n📊 *Today's Usage:* {today_usage}/2\n📦 *Total Accounts:* {total_accounts}\n\n💰 *30% Cashback on all losses!*\n💡 *Tap any to copy*",
        
        # Agent
        "contact_agent": "💬 *Contact Our Agent*\n\n📞 Reach out to *{agent_username}* for:\n• Account issues\n• Technical support\n• Questions about 1xBet\n• Cashback inquiries",
        "contact_agent_button": "📞 Contact Agent",
        
        # Share bot
        "share_bot_title": "📢 *Share Bot & Earn Rewards!*\n\n🤖 *Bot:* @{bot_username}\n\n📊 *You have shared:* {share_count} times\n🎁 *Rewards:* Ask our agent for special bonuses!\n\n📤 *Share link:*\n`{bot_link}`\n\n💬 Contact agent: {agent_username}",
        "share_bot_button": "📤 Share Bot",
        
        # Stats
        "overall_stats": "📊 *Bot Statistics*\n\n📦 *Available Accounts:* {available_accounts}\n👤 *Total Users used bot:* {total_users}\n📤 *Total Accounts Given:* {total_accounts_given}\n📅 *Given Today:* {today_given}\n💰 *Cashback:* 30% on all losses\n\n💳 *Deposit Stats:*\n   ✅ Accepted: {deposits_accepted}\n   ❌ Rejected: {deposits_rejected}\n   💵 Total Accepted Amount: {total_deposit_amount:,.0f} SAR\n\n💸 *Withdraw Stats:*\n   ✅ Accepted: {withdrawals_accepted}\n   ❌ Rejected: {withdrawals_rejected}\n   💵 Total Accepted Amount: {total_withdraw_amount:,.0f} SAR",
        "stats_menu": "📊 *Statistics Menu*\n\nSelect an option below:",
        "overall_stats_button": "📊 Overall Stats",
        "user_stats_button": "👤 User Stats",
        "cashback_button": "💰 Player ID Cashback",
        
        "user_stats_prompt": "👤 *User Stats*\n\nPlease enter the Telegram username to check stats:\n\n📝 *Example:* `@username` or `username`\n\nType /cancel to cancel.",
        "user_stats_result": "👤 *User Stats for @{username}*\n\n📤 *Total Accounts Given:* {total_accounts}\n📅 *Given Today:* {given_today}\n\n💳 *Deposit Stats:*\n   ✅ Accepted: {deposits_accepted}\n   ❌ Rejected: {deposits_rejected}\n   💵 Total Accepted Amount: {total_deposit_amount:,.0f} SAR\n\n💸 *Withdraw Stats:*\n   ✅ Accepted: {withdrawals_accepted}\n   ❌ Rejected: {withdrawals_rejected}\n   💵 Total Accepted Amount: {total_withdraw_amount:,.0f} SAR\n\n📢 *Times shared bot:* {share_count}",
        "user_not_found": "❌ *User not found!*\n\nNo user found with username `{username}`.",
        
        # Cashback
        "cashback_title": "💰 *Player ID Cashback Calculator*",
        "cashback_step1": "Step 1/3: Enter the Player ID\n\n📝 *Example:* `123456789`\n\nType /cancel to cancel.",
        "cashback_step2": "✅ Player ID: `{player_id}`\n\nStep 2/3: Enter the start date\n\n📝 *Format:* `YYYY-MM-DD`\n📌 *Example:* `2026-07-01`\n\nType /cancel to cancel.",
        "cashback_step3": "✅ Start Date: `{start_date}`\n\nStep 3/3: Enter the end date\n\n📝 *Format:* `YYYY-MM-DD`\n📌 *Example:* `2026-07-14`\n\nType /cancel to cancel.",
        "invalid_player_id": "❌ *Invalid Player ID!*\n\nPlease enter a numeric Player ID.",
        "invalid_date": "❌ *Invalid date format!*\n\nPlease use the format: `YYYY-MM-DD`",
        "cashback_result": "💰 *Cashback Calculation*\n\n🆔 Player ID: `{player_id}`\n📅 Period: {start_date} to {end_date}\n\n📊 *Summary:*\n   💳 Deposits Accepted: {deposits_count} ({total_deposits:,.0f} SAR)\n   💸 Withdrawals Accepted: {withdrawals_count} ({total_withdrawals:,.0f} SAR)\n   📊 Net Amount: {net_amount:,.0f} SAR\n\n🎯 *Cashback ({percent}%):* `{cashback:,.2f} SAR`\n\n📌 *Formula:* {percent}% × (Deposits - Withdrawals)",
        
        # Deposit & Withdraw
        "deposit_withdraw_menu": "💳 *Deposit & Withdrawal*\n\n👇 *Select an option below:*",
        "deposit": "💰 Deposit",
        "withdraw": "💸 Withdraw",
        
        # Deposit flow
        "deposit_start": "💰 *Deposit Process*\n\nStep 1/4: Enter your Player ID\n\n📝 Please enter your 1xBet Player ID:",
        "deposit_player_id": "💰 *Deposit Process*\n\n✅ Player ID: `{player_id}`\n\nStep 2/4: Select payment method\n\nChoose your payment method:",
        "deposit_method": "💰 *Deposit Process*\n\n✅ Player ID: `{player_id}`\n✅ Method: {method_name}\n\n📋 *Send to:*\n{details}\n\nStep 3/4: Enter amount\n\nSelect an amount below or enter custom:",
        "deposit_amount": "💰 *Deposit Process*\n\n✅ Player ID: `{player_id}`\n✅ Method: {method_name}\n✅ Amount: {amount} SAR\n\nStep 4/4: Send receipt\n\n📸 Please send a screenshot or photo of your transfer receipt.\n\n📌 *Instructions:*\n• Take a screenshot of the transfer confirmation\n• Send it as a photo to this chat\n\n⚠️ *Important:* The receipt must show:\n• The amount transferred\n• The recipient details\n• The transaction reference\n\nType /cancel to cancel.",
        "deposit_custom_amount": "📝 *Enter custom amount:*\n\nPlease enter the amount in SAR (10-500 SAR):",
        "deposit_invalid_amount": "❌ *Amount must be between 10 and 500 SAR!*",
        "deposit_invalid_number": "❌ *Invalid amount!*\n\nPlease enter a valid number.",
        "deposit_receipt_received": "✅ *Receipt Received!*\n\n⏳ Please wait while our team verifies your transfer.\n\nYou will be notified once your deposit is confirmed.\n\n📞 For urgent inquiries, contact our agent.",
        "deposit_confirmed": "✅ *Your deposit has been confirmed!*\n\n💰 Amount: {amount} SAR\n🎉 Funds have been added to your 1xBet account!",
        "deposit_rejected": "❌ *Deposit Rejected!*\n\n💰 Amount: {amount} SAR\n\n📋 *Reason:*\n{reason}",
        
        # Deposit admin notifications
        "new_deposit": "💰 *New Deposit Request*\n\n🆔 ID: {deposit_id}\n👤 User: @{username}\n🆔 Player ID: {player_id}\n💳 Method: {method_name}\n💵 Amount: {amount} SAR\n📅 Time: {created_at}\n\nPlease verify the transfer and respond:",
        "deposit_accept": "✅ Accept",
        "deposit_reject": "❌ Reject",
        "deposit_accept_success": "✅ Deposit accepted!",
        "deposit_reject_prompt": "❌ *Reject Deposit*\n\nRequest ID: `{request_id}`\n\nPlease send the reason for rejection:",
        "deposit_not_found": "❌ Deposit request not found!",
        "rejection_sent": "✅ Rejection reason sent to user.",
        "rejection_prompt": "❌ *Please send a text reason for rejection.*",
        "rejection_cancelled": "❌ *Cancelled!*",
        
        # Withdraw flow
        "withdraw_start": "💸 *Withdraw Process*\n\nStep 1/4: Select withdrawal method\n\nChoose your withdrawal method:",
        "withdraw_player_id": "💸 *Withdraw Process*\n\nStep 2/4: Enter your Player ID\n\n📝 Please enter your 1xBet Player ID:",
        "withdraw_details": "💸 *Withdraw Process*\n\nStep 3/4: Enter your details\n\n📝 *{field}:*\n\nPlease enter your {field_lower}:",
        "withdraw_code": "💸 *Withdraw Process*\n\nStep 4/4: Enter withdrawal code\n\n📋 *How to get your withdrawal code:*\n\n1️⃣ Open 1xBet app\n2️⃣ Go to *Withdraw* section\n3️⃣ Scroll down and select *1xBet Cash*\n4️⃣ Enter amount, select:\n   - City: *Riyadh*\n   - Street: *ARVEA*\n5️⃣ Confirm the withdrawal\n6️⃣ Scroll up and find *Withdrawal Requests*\n7️⃣ Click *Get Code*\n\n📝 *Enter the code here:*\n\nType /cancel to cancel.",
        "withdraw_code_entered": "✅ *Withdrawal Request Submitted!*\n\n⏳ Please wait while our team processes your request.\n\nYou will be notified once your withdrawal is confirmed.\n\n📞 For urgent inquiries, contact our agent.",
        "withdraw_confirmed": "✅ *Your withdrawal has been processed!*\n\n💰 Amount: {amount:,.0f} SAR\n💸 Funds have been sent to your selected method.",
        "withdraw_rejected": "❌ *Withdrawal Rejected!*\n\n📋 *Reason:*\n{reason}",
        "invalid_method": "❌ *Invalid method!*",
        "invalid_withdraw_amount": "❌ *Invalid amount!*\n\nPlease enter a valid positive number.",
        
        # Withdraw admin notifications
        "new_withdraw": "💸 *New Withdrawal Request*\n\n🆔 ID: {withdraw_id}\n👤 User: @{username}\n🆔 Player ID: {player_id}\n💳 Method: {method_name}\n📋 User Details:\n{details}\n🔑 Withdrawal Code: {code}\n📅 Time: {created_at}\n\nPlease verify and respond:",
        "withdraw_accept": "✅ Accept",
        "withdraw_reject": "❌ Reject",
        "withdraw_accept_prompt": "✅ *Accept Withdrawal*\n\nRequest ID: `{request_id}`\n\nPlease enter the withdrawal amount in SAR:",
        "withdraw_accept_success": "✅ *Withdrawal accepted!*\n\nRequest ID: `{withdraw_id}`\nAmount: {amount:,.0f} SAR",
        "withdraw_reject_prompt": "❌ *Reject Withdrawal*\n\nRequest ID: `{request_id}`\n\nPlease send the reason for rejection:",
        "withdraw_not_found": "❌ Withdrawal request not found!",
        "withdraw_already_processed": "⚠️ *This withdrawal has already been processed!*",
        "withdraw_session_expired": "❌ *Session expired!*\n\nPlease try accepting the withdrawal again.",
        "withdraw_invalid_action": "❌ *Invalid action!*\n\nPlease try accepting the withdrawal again.",
        "withdraw_id_not_found": "❌ *Withdrawal ID not found!*\n\nPlease try accepting the withdrawal again.",
        
        # Video tutorials
        "video_tutorials_title": "📹 *Video Tutorials*\n\n{video_list}\n\n👆 Click a video to watch:",
        "video_tutorials_empty": "📹 *No Videos Available*\n\nThere are no video tutorials yet.\nPlease check back later!",
        "video_admin_panel": "📹 *Video Tutorials - Admin Panel*\n\n📊 Total Videos: {total_videos}\n\n📹 *Add Video* - Add a new video tutorial\n🗑️ *Delete Video* - Remove a video\n📋 *List Videos* - View all videos\n\n👆 Select an option below:",
        "add_video": "📹 Add Video",
        "delete_video": "🗑️ Delete Video",
        "list_videos": "📋 List Videos",
        "add_video_step1": "📹 *Add Video Tutorial*\n\n📤 *Step 1/2:* Send me the video file\n\nType /cancel to cancel.",
        "add_video_step2": "✅ *Video Received!*\n\n📝 *Step 2/2:* Send me the title for this video\n\nType /cancel to cancel.",
        "add_video_title_short": "❌ *Title too short!*\n\nPlease enter at least 3 characters.",
        "add_video_exists": "❌ *A video with title '{title}' already exists!*",
        "add_video_success": "✅ *Video Added!*\n\n🎬 *Title:* {title}\n🆔 *ID:* `{vid}`\n📹 *Total Videos:* {total_videos}",
        "delete_video_prompt": "🗑️ *Delete Video*\n\nSelect the video you want to delete:",
        "delete_video_success": "✅ *Video Deleted!*\n\nRemoved: {title}",
        "delete_video_not_found": "❌ *Video '{title}' not found!*",
        "no_videos_to_delete": "📭 *No videos to delete!*",
        "video_not_found": "❌ *Video not found!*",
        "video_list_title": "📋 *Video List*\n\n{video_list}",
        "no_videos": "📭 *No videos available.*",
        "error_sending_video": "❌ *Error sending video!*",
        "unknown_video_action": "❌ *Unknown video action.*",
        "video_not_in_delete_mode": "❌ *You are not in delete mode.*",
        "please_send_video": "❌ *Please send a video!*",
        
        # Payment Methods
        "pm_management": "📋 *Payment Methods Management*\n\nSelect an option below:",
        "list_methods": "📋 List Methods",
        "add_method": "➕ Add Method",
        "edit_method": "✏️ Edit Method",
        "delete_method": "🗑️ Delete Method",
        "no_methods": "📭 *No payment methods available.*",
        "pm_list": "📋 *Payment Methods*\n\n{methods_list}",
        "add_method_step1": "➕ *Add Payment Method*\n\nStep 1/6: Enter a unique ID\n\n📝 *Example:* `barq`, `newpay`\n\nType /cancel to cancel.",
        "add_method_step2": "✅ ID: `{key}`\n\nStep 2/6: Enter the display name\n\n📝 *Example:* `💳 Barq Wallet`",
        "add_method_step3": "✅ Name: {name}\n\nStep 3/6: How many fields does this method need?\n\n📝 *Examples:*\n• Barq: 1 field (phone_number)\n• Bank Transfer: 2 fields (phone_number, iban)\n\nChoose a number:",
        "add_method_step4": "✅ {count} fields selected.\n\nStep 4/6: Enter field #{index}\n\n📝 *Examples:* {examples}\n\nEnter the field name:",
        "add_method_step5": "✅ Fields added: {fields}\n\nStep 5/6: Enter values for each field\n\n📝 Enter value for *{field}*:",
        "add_method_step6": "📝 Enter value for *{field}*:",
        "add_method_success": "✅ *Payment Method Added!*\n\n🔹 Name: {name}\n📌 ID: `{key}`\n📝 Fields: {fields}\n📋 Values:\n{values}",
        "edit_method_prompt": "✏️ *Edit Payment Method*\n\nSelect the method you want to edit:",
        "edit_method_selected": "✏️ *Editing: {name}*\n\n📌 ID: `{key}`\n📝 Fields: {fields}\n📋 Details: {details}\n\nSelect which field to edit:",
        "edit_method_field": "✏️ *Editing: {field}*\n\nCurrent value: `{current}`\n\nEnter the new value:",
        "edit_method_success": "✅ *Method Updated!*\n\n📌 ID: `{key}`\n📝 {field}: {value}",
        "delete_method_prompt": "🗑️ *Delete Payment Method*\n\nSelect the method you want to delete:",
        "delete_method_confirm": "🗑️ *Delete Method?*\n\n🔹 Name: {name}\n📌 ID: `{key}`\n\n⚠️ *Are you sure?*\nThis action cannot be undone!",
        "delete_method_yes": "✅ Yes, Delete",
        "delete_method_no": "❌ No, Cancel",
        "delete_method_success": "✅ *Method `{key}` deleted!*",
        "delete_method_cancelled": "❌ *Deletion cancelled!*",
        "invalid_id": "❌ *Invalid ID!*\n\nUse only letters, numbers, and underscores.",
        "id_exists": "❌ *ID `{id}` already exists!*",
        "invalid_number": "❌ *Invalid number!*\n\nPlease enter a number between 1 and 5.",
        "method_not_found": "❌ *Method `{key}` not found!*",
        "field_not_found": "❌ *Field `{field}` not found!*",
        "invalid_fields": "❌ *Invalid fields!*",
        "edit_details_not_allowed": "❌ *To edit details, edit individual fields.*",
        
        # Admin commands
        "unauthorized": "⛔ *Unauthorized!*",
        "add_account_help": "📝 *How to add an account:*\n\n`/ass Username: 123456789 Password: abcd1234`\n\n**Example:**\n`/ass Username: Ahmed_123 Password: SecurePass456`\n\nYou can also add multiple:\n`/ass Username: user1 Password: pass1, Username: user2 Password: pass2`",
        "add_account_invalid": "❌ *Invalid format!*\n\nUse:\n`/ass Username: Ahmed Password: 123456`",
        "add_account_no_valid": "❌ *No valid accounts found!*",
        "add_account_success": "✅ *Added {count} account(s)!*\n\n{accounts}\n\n📦 *Total Available:* {total}\n💰 *All accounts get 30% cashback!*",
        "no_accounts_to_list": "📭 *No accounts available.*",
        "accounts_list_admin": "📋 *Available Accounts ({count})*\n\n{accounts}\n\n💰 *30% Cashback on all losses!*",
        "delete_account_help": "📝 `/del Username: player1`",
        "delete_account_invalid": "❌ *Invalid format!*\n\nUse: `/del Username: player1`",
        "delete_account_not_found": "❌ *Account with username `{username}` not found!*",
        "delete_account_success": "✅ *Account Deleted!*\n\nRemoved: `{account}`\n📦 *Total Available:* {total}",
        "clear_accounts_confirm": "🗑️ *Cleared {count} account(s)!*\n\n📦 *Total Available:* 0",
        "no_accounts_to_clear": "📭 *No accounts to clear!*",
        "reset_user_help": "📝 Usage: `/resetuser user_id`",
        "reset_user_success": "✅ *User {user_id} has been reset!*",
        "reset_user_not_found": "❌ *User {user_id} not found.*",
        
        # Common
        "cancel": "/cancel",
        "custom_amount": "✏️ Enter Custom Amount",
        "unknown_command": "❌ *I don't understand that command.*\n\nPlease use the buttons below:",
        "enter_amount": "📝 *Enter custom amount:*\n\nPlease enter the amount in SAR (10-500 SAR):",
        "please_send_photo": "❌ *Please send a photo!*",
        
        # Admin withdrawal states
        "withdraw_amount_prompt": "Please enter the withdrawal amount in SAR:",
        "withdraw_amount_invalid": "❌ *Invalid amount!*\n\nPlease enter a valid positive number.",
        "withdraw_amount_session_expired": "❌ *Session expired!*\n\nPlease try accepting the withdrawal again.",
        
        # Stats menu options
        "stats_menu_options": "📊 *Statistics Menu*\n\nSelect an option below:",

        # ----- NEW KEYS ADDED -----
        "receipt_caption": "📸 Receipt for Deposit {deposit_id}",
        "video_play_caption": "🎬 *{title}*\n\n📹 Tutorial Video\n📅 Added: {date}",
        "video_list_item": "🆔 ID: `{vid}`\n🎬 Title: {title}\n📅 Added: {date}",
        "withdraw_video_caption": "🎬 *{title}*\n\n📹 Watch this tutorial for step-by-step instructions!",
        # --------------------------
        "cashback_video_caption": "🎬 *Cashback Tutorial*\n\n📹 Watch this tutorial to learn how to get 5% cashback and more in the 1xBet app!\n\n💰 After watching, request your remaining 25% cashback below.",

        "cashback_video_not_found": "📹 *Video not found!*\n\nPlease contact admin.",
        "cashback_request_message": (
            "💰 *30% Cashback Request*\n\n"
            "📌 *How it works:*\n"
            "• You already get 5% cashback in the app\n"
            "• Request the remaining 25% here\n\n"
            "📝 *Step 1/2:* Enter your 1xBet Player ID\n\n"
            "Example: `123456789`\n\n"
            "Type /cancel to cancel."
        ),
    
    
    },
    "ar": {
        # Bot name and welcome
        "bot_name": "بوت 1xBet السعودي",
        "welcome_title": "🎰 *مرحباً بك في بوت 1xBet السعودي!*",
        "welcome_text": "🎰 *مرحباً بك في بوت 1xBet السعودي!*\n\n💰 *احصل على 30% كاش باك على جميع الخسائر!*\n📌 يمكنك الحصول على *حسابين يومياً*\n💳 *الإيداع والسحب بسهولة!*\n\n👆 اضغط على الأزرار أدناه:",
        "admin_welcome": "🎰 *مرحباً أيها المدير!*\n\n👑 *لوحة التحكم*\n➕ `/ass` - إضافة حسابات\n📊 `/stats` - عرض الإحصائيات\n📋 `/listaccounts` - عرض جميع الحسابات\n💳 `/pm` - طرق الدفع\n\n📌 *ميزات المستخدم:*\n💰 *احصل على 30% كاش باك على جميع الخسائر!*\n📌 يمكنك الحصول على *حسابين يومياً*\n💳 *الإيداع والسحب بسهولة!*\n\n👆 اضغط على الأزرار أدناه:",
        
        # Language selection
        "language_selection": "🌍 *اختر لغتك / Select your language*\n\nيرجى اختيار لغتك المفضلة:",
        "english": "🇬🇧 الإنجليزية",
        "arabic": "🇸🇦 العربية",
        "language_saved": "✅ *تم حفظ اللغة!* ستظهر جميع الرسائل الآن باللغة الإنجليزية.",
        "language_saved_ar": "✅ *تم حفظ اللغة!* ستظهر جميع الرسائل الآن باللغة العربية.",
        
        # Main menu buttons
        "get_account": "🎰 احصل على حساب",
        "talk_to_agent": "💬 تحدث مع الوكيل",
        "my_accounts": "📋 حساباتي",
        "deposit_withdraw": "💳 الإيداع والسحب",
        "video_tutorials": "📹 دروس فيديو",
        "share_bot": "📢 مشاركة البوت",
        "back_to_menu": "🔙 العودة للقائمة",
        "get_another_account": "🎰 احصل على حساب آخر",
        
        # Admin buttons
        "stats": "📊 /stats",
        "list_accounts": "📋 /listaccounts",
        "add_accounts": "➕ /ass",
        "payment_methods": "💳 /pm",
        
        # Subscription check
        "join_channel": "👋 *مرحباً!*\n\nلاستخدام هذا البوت، يجب عليك أولاً الانضمام إلى قناتنا:\n➡️ [1xbet السعودية](https://t.me/saudi_1xbet_accounts)\n\nبعد الانضمام، اضغط على الزر أدناه للمتابعة.",
        "join_channel_button": "📢 انضم إلى قناتنا",
        "check_subscription": "✅ انضممت! تحقق من الاشتراك",
        "not_member": "❌ *لست عضواً بعد!*\n\nيرجى الانضمام إلى [قناتنا](https://t.me/saudi_1xbet_accounts) أولاً، ثم اضغط 'تحقق من الاشتراك' مرة أخرى.",
        "subscription_verified": "✅ تم التحقق من الاشتراك! مرحباً بك!",
        
        # Account related
        "daily_limit_reached": "❌ *تم الوصول إلى الحد اليومي!*\n\nلقد تلقيت *{today_count}* حساباً اليوم.\nالحد الأقصى *حسابان يومياً*.\n\n⏳ يرجى المحاولة غداً.\n📋 استخدم 'حساباتي' لعرض حساباتك.",
        "no_accounts_available": "❌ *لا توجد حسابات متاحة!*\n\nتم توزيع جميع الحسابات.\nيرجى التحقق لاحقاً أو الاتصال بالوكيل.",
        "account_assigned": "✅ *تم تخصيص الحساب!*\n\n{account_display}\n\n💰 *30% كاش باك على جميع الخسائر!*\n\n📊 *الاستخدام اليومي:* {today_usage}/2\n📦 *الحسابات المتبقية:* {remaining}\n\n💡 *اضغط للنسخ!*\n🔒 احفظه بأمان.",
        "no_accounts_found": "📋 *لا توجد حسابات*\n\nاستخدم 'احصل على حساب' للحصول على حسابك الأول!",
        "your_accounts": "📋 *حساباتك*\n\n{accounts_list}\n\n📊 *الاستخدام اليومي:* {today_usage}/2\n📦 *إجمالي الحسابات:* {total_accounts}\n\n💰 *30% كاش باك على جميع الخسائر!*\n💡 *اضغط على أي حساب للنسخ*",
        
        # Agent
        "contact_agent": "💬 *تواصل مع وكيلنا*\n\n📞 تواصل مع *{agent_username}* لـ:\n• مشاكل الحساب\n• الدعم الفني\n• أسئلة عن 1xBet\n• استفسارات الكاش باك",
        "contact_agent_button": "📞 تواصل مع الوكيل",
        
        # Share bot
        "share_bot_title": "📢 *شارك البوت واربح مكافآت!*\n\n🤖 *البوت:* @{bot_username}\n\n📊 *لقد شاركت:* {share_count} مرة\n🎁 *المكافآت:* اسأل وكيلنا عن المكافآت الخاصة!\n\n📤 *رابط المشاركة:*\n`{bot_link}`\n\n💬 تواصل مع الوكيل: {agent_username}",
        "share_bot_button": "📤 مشاركة البوت",
        
        # Stats
        "overall_stats": "📊 *إحصائيات البوت*\n\n📦 *الحسابات المتاحة:* {available_accounts}\n👤 *إجمالي المستخدمين:* {total_users}\n📤 *إجمالي الحسابات المسلمة:* {total_accounts_given}\n📅 *المسلمة اليوم:* {today_given}\n💰 *الكاش باك:* 30% على جميع الخسائر\n\n💳 *إحصائيات الإيداع:*\n   ✅ مقبولة: {deposits_accepted}\n   ❌ مرفوضة: {deposits_rejected}\n   💵 إجمالي المبلغ المقبول: {total_deposit_amount:,.0f} ريال\n\n💸 *إحصائيات السحب:*\n   ✅ مقبولة: {withdrawals_accepted}\n   ❌ مرفوضة: {withdrawals_rejected}\n   💵 إجمالي المبلغ المقبول: {total_withdraw_amount:,.0f} ريال",
        "stats_menu": "📊 *قائمة الإحصائيات*\n\nاختر خياراً أدناه:",
        "overall_stats_button": "📊 الإحصائيات العامة",
        "user_stats_button": "👤 إحصائيات المستخدم",
        "cashback_button": "💰 كاش باك معرف اللاعب",
        
        "user_stats_prompt": "👤 *إحصائيات المستخدم*\n\nيرجى إدخال اسم المستخدم في تلغرام للتحقق من الإحصائيات:\n\n📝 *مثال:* `@username` أو `username`\n\nاكتب /cancel للإلغاء.",
        "user_stats_result": "👤 *إحصائيات المستخدم @{username}*\n\n📤 *إجمالي الحسابات المسلمة:* {total_accounts}\n📅 *المسلمة اليوم:* {given_today}\n\n💳 *إحصائيات الإيداع:*\n   ✅ مقبولة: {deposits_accepted}\n   ❌ مرفوضة: {deposits_rejected}\n   💵 إجمالي المبلغ المقبول: {total_deposit_amount:,.0f} ريال\n\n💸 *إحصائيات السحب:*\n   ✅ مقبولة: {withdrawals_accepted}\n   ❌ مرفوضة: {withdrawals_rejected}\n   💵 إجمالي المبلغ المقبول: {total_withdraw_amount:,.0f} ريال\n\n📢 *عدد مشاركات البوت:* {share_count}",
        "user_not_found": "❌ *المستخدم غير موجود!*\n\nلم يتم العثور على مستخدم باسم `{username}`.",
        
        # Cashback
        "cashback_title": "💰 *حاسبة كاش باك معرف اللاعب*",
        "cashback_step1": "الخطوة 1/3: أدخل معرف اللاعب\n\n📝 *مثال:* `123456789`\n\nاكتب /cancel للإلغاء.",
        "cashback_step2": "✅ معرف اللاعب: `{player_id}`\n\nالخطوة 2/3: أدخل تاريخ البداية\n\n📝 *الصيغة:* `YYYY-MM-DD`\n📌 *مثال:* `2026-07-01`\n\nاكتب /cancel للإلغاء.",
        "cashback_step3": "✅ تاريخ البداية: `{start_date}`\n\nالخطوة 3/3: أدخل تاريخ النهاية\n\n📝 *الصيغة:* `YYYY-MM-DD`\n📌 *مثال:* `2026-07-14`\n\nاكتب /cancel للإلغاء.",
        "invalid_player_id": "❌ *معرف لاعب غير صالح!*\n\nيرجى إدخال معرف لاعب رقمي.",
        "invalid_date": "❌ *صيغة تاريخ غير صالحة!*\n\nيرجى استخدام الصيغة: `YYYY-MM-DD`",
        "cashback_result": "💰 *نتيجة حساب الكاش باك*\n\n🆔 معرف اللاعب: `{player_id}`\n📅 الفترة: {start_date} إلى {end_date}\n\n📊 *الملخص:*\n   💳 الإيداعات المقبولة: {deposits_count} ({total_deposits:,.0f} ريال)\n   💸 السحوبات المقبولة: {withdrawals_count} ({total_withdrawals:,.0f} ريال)\n   📊 صافي المبلغ: {net_amount:,.0f} ريال\n\n🎯 *الكاش باك ({percent}%):* `{cashback:,.2f} ريال`\n\n📌 *المعادلة:* {percent}% × (الإيداعات - السحوبات)",
        
        # Deposit & Withdraw
        "deposit_withdraw_menu": "💳 *الإيداع والسحب*\n\n👇 *اختر خياراً أدناه:*",
        "deposit": "💰 إيداع",
        "withdraw": "💸 سحب",
        
        # Deposit flow
        "deposit_start": "💰 *عملية الإيداع*\n\nالخطوة 1/4: أدخل معرف اللاعب\n\n📝 يرجى إدخال معرف اللاعب في 1xBet:",
        "deposit_player_id": "💰 *عملية الإيداع*\n\n✅ معرف اللاعب: `{player_id}`\n\nالخطوة 2/4: اختر طريقة الدفع\n\nاختر طريقة الدفع:",
        "deposit_method": "💰 *عملية الإيداع*\n\n✅ معرف اللاعب: `{player_id}`\n✅ الطريقة: {method_name}\n\n📋 *أرسل إلى:*\n{details}\n\nالخطوة 3/4: أدخل المبلغ\n\nاختر مبلغاً أدناه أو أدخل مبلغاً مخصصاً:",
        "deposit_amount": "💰 *عملية الإيداع*\n\n✅ معرف اللاعب: `{player_id}`\n✅ الطريقة: {method_name}\n✅ المبلغ: {amount} ريال\n\nالخطوة 4/4: أرسل الإيصال\n\n📸 يرجى إرسال لقطة شاشة أو صورة لإيصال التحويل.\n\n📌 *التعليمات:*\n• التقط لقطة شاشة لتأكيد التحويل\n• أرسلها كصورة في هذه المحادثة\n\n⚠️ *مهم:* يجب أن يظهر في الإيصال:\n• المبلغ المحول\n• تفاصيل المستلم\n• مرجع العملية\n\nاكتب /cancel للإلغاء.",
        "deposit_custom_amount": "📝 *أدخل المبلغ المخصص:*\n\nيرجى إدخال المبلغ بالريال (10-500 ريال):",
        "deposit_invalid_amount": "❌ *يجب أن يكون المبلغ بين 10 و 500 ريال!*",
        "deposit_invalid_number": "❌ *مبلغ غير صالح!*\n\nيرجى إدخال رقم صحيح.",
        "deposit_receipt_received": "✅ *تم استلام الإيصال!*\n\n⏳ يرجى الانتظار حتى يقوم فريقنا بالتحقق من تحويلك.\n\nسيتم إعلامك عند تأكيد إيداعك.\n\n📞 للاستفسارات العاجلة، تواصل مع وكيلنا.",
        "deposit_confirmed": "✅ *تم تأكيد إيداعك!*\n\n💰 المبلغ: {amount} ريال\n🎉 تم إضافة الأموال إلى حسابك في 1xBet!",
        "deposit_rejected": "❌ *تم رفض الإيداع!*\n\n💰 المبلغ: {amount} ريال\n\n📋 *السبب:*\n{reason}",
        
        # Deposit admin notifications
        "new_deposit": "💰 *طلب إيداع جديد*\n\n🆔 المعرف: {deposit_id}\n👤 المستخدم: @{username}\n🆔 معرف اللاعب: {player_id}\n💳 الطريقة: {method_name}\n💵 المبلغ: {amount} ريال\n📅 الوقت: {created_at}\n\nيرجى التحقق من التحويل والرد:",
        "deposit_accept": "✅ قبول",
        "deposit_reject": "❌ رفض",
        "deposit_accept_success": "✅ تم قبول الإيداع!",
        "deposit_reject_prompt": "❌ *رفض الإيداع*\n\nمعرف الطلب: `{request_id}`\n\nيرجى إرسال سبب الرفض:",
        "deposit_not_found": "❌ طلب الإيداع غير موجود!",
        "rejection_sent": "✅ تم إرسال سبب الرفض إلى المستخدم.",
        "rejection_prompt": "❌ *يرجى إرسال نص لسبب الرفض.*",
        "rejection_cancelled": "❌ *تم الإلغاء!*",
        
        # Withdraw flow
        "withdraw_start": "💸 *عملية السحب*\n\nالخطوة 1/4: اختر طريقة السحب\n\nاختر طريقة السحب:",
        "withdraw_player_id": "💸 *عملية السحب*\n\nالخطوة 2/4: أدخل معرف اللاعب\n\n📝 يرجى إدخال معرف اللاعب في 1xBet:",
        "withdraw_details": "💸 *عملية السحب*\n\nالخطوة 3/4: أدخل تفاصيلك\n\n📝 *{field}:*\n\nيرجى إدخال {field_lower}:",
        "withdraw_code": "💸 *عملية السحب*\n\nالخطوة 4/4: أدخل رمز السحب\n\n📋 *كيفية الحصول على رمز السحب:*\n\n1️⃣ افتح تطبيق 1xBet\n2️⃣ اذهب إلى قسم *السحب*\n3️⃣ انتقل للأسفل واختر *1xBet Cash*\n4️⃣ أدخل المبلغ، اختر:\n   - المدينة: *الرياض*\n   - الشارع: *ARVEA*\n5️⃣ أكد عملية السحب\n6️⃣ انتقل للأعلى وابحث عن *طلبات السحب*\n7️⃣ اضغط *احصل على الرمز*\n\n📝 *أدخل الرمز هنا:*\n\nاكتب /cancel للإلغاء.",
        "withdraw_code_entered": "✅ *تم تقديم طلب السحب!*\n\n⏳ يرجى الانتظار حتى يقوم فريقنا بمعالجة طلبك.\n\nسيتم إعلامك عند تأكيد سحبك.\n\n📞 للاستفسارات العاجلة، تواصل مع وكيلنا.",
        "withdraw_confirmed": "✅ *تمت معالجة سحبك!*\n\n💰 المبلغ: {amount:,.0f} ريال\n💸 تم إرسال الأموال إلى الطريقة التي اخترتها.",
        "withdraw_rejected": "❌ *تم رفض السحب!*\n\n📋 *السبب:*\n{reason}",
        "invalid_method": "❌ *طريقة غير صالحة!*",
        "invalid_withdraw_amount": "❌ *مبلغ غير صالح!*\n\nيرجى إدخال رقم موجب صحيح.",
        
        # Withdraw admin notifications
        "new_withdraw": "💸 *طلب سحب جديد*\n\n🆔 المعرف: {withdraw_id}\n👤 المستخدم: @{username}\n🆔 معرف اللاعب: {player_id}\n💳 الطريقة: {method_name}\n📋 تفاصيل المستخدم:\n{details}\n🔑 رمز السحب: {code}\n📅 الوقت: {created_at}\n\nيرجى التحقق والرد:",
        "withdraw_accept": "✅ قبول",
        "withdraw_reject": "❌ رفض",
        "withdraw_accept_prompt": "✅ *قبول السحب*\n\nمعرف الطلب: `{request_id}`\n\nيرجى إدخال مبلغ السحب بالريال:",
        "withdraw_accept_success": "✅ *تم قبول السحب!*\n\nمعرف الطلب: `{withdraw_id}`\nالمبلغ: {amount:,.0f} ريال",
        "withdraw_reject_prompt": "❌ *رفض السحب*\n\nمعرف الطلب: `{request_id}`\n\nيرجى إرسال سبب الرفض:",
        "withdraw_not_found": "❌ طلب السحب غير موجود!",
        "withdraw_already_processed": "⚠️ *تمت معالجة هذا السحب بالفعل!*",
        "withdraw_session_expired": "❌ *انتهت الجلسة!*\n\nيرجى محاولة قبول السحب مرة أخرى.",
        "withdraw_invalid_action": "❌ *إجراء غير صالح!*\n\nيرجى محاولة قبول السحب مرة أخرى.",
        "withdraw_id_not_found": "❌ *معرف السحب غير موجود!*\n\nيرجى محاولة قبول السحب مرة أخرى.",
        
        # Video tutorials
        "video_tutorials_title": "📹 *دروس الفيديو*\n\n{video_list}\n\n👆 اضغط على فيديو للمشاهدة:",
        "video_tutorials_empty": "📹 *لا توجد دروس فيديو*\n\nلا توجد دروس فيديو حالياً.\nيرجى التحقق لاحقاً!",
        "video_admin_panel": "📹 *دروس الفيديو - لوحة المدير*\n\n📊 إجمالي الفيديوهات: {total_videos}\n\n📹 *إضافة فيديو* - إضافة درس فيديو جديد\n🗑️ *حذف فيديو* - إزالة فيديو\n📋 *قائمة الفيديوهات* - عرض جميع الفيديوهات\n\n👆 اختر خياراً أدناه:",
        "add_video": "📹 إضافة فيديو",
        "delete_video": "🗑️ حذف فيديو",
        "list_videos": "📋 قائمة الفيديوهات",
        "add_video_step1": "📹 *إضافة درس فيديو*\n\n📤 *الخطوة 1/2:* أرسل ملف الفيديو\n\nاكتب /cancel للإلغاء.",
        "add_video_step2": "✅ *تم استلام الفيديو!*\n\n📝 *الخطوة 2/2:* أرسل عنوان هذا الفيديو\n\nاكتب /cancel للإلغاء.",
        "add_video_title_short": "❌ *العنوان قصير جداً!*\n\nيرجى إدخال 3 أحرف على الأقل.",
        "add_video_exists": "❌ *يوجد فيديو بالفعل بعنوان '{title}'!*",
        "add_video_success": "✅ *تمت إضافة الفيديو!*\n\n🎬 *العنوان:* {title}\n🆔 *المعرف:* `{vid}`\n📹 *إجمالي الفيديوهات:* {total_videos}",
        "delete_video_prompt": "🗑️ *حذف فيديو*\n\nاختر الفيديو الذي تريد حذفه:",
        "delete_video_success": "✅ *تم حذف الفيديو!*\n\nتمت إزالة: {title}",
        "delete_video_not_found": "❌ *الفيديو '{title}' غير موجود!*",
        "no_videos_to_delete": "📭 *لا توجد فيديوهات لحذفها!*",
        "video_not_found": "❌ *الفيديو غير موجود!*",
        "video_list_title": "📋 *قائمة الفيديوهات*\n\n{video_list}",
        "no_videos": "📭 *لا توجد فيديوهات متاحة.*",
        "error_sending_video": "❌ *خطأ في إرسال الفيديو!*",
        "unknown_video_action": "❌ *إجراء فيديو غير معروف.*",
        "video_not_in_delete_mode": "❌ *أنت لست في وضع الحذف.*",
        "please_send_video": "❌ *يرجى إرسال فيديو!*",
        
        # Payment Methods
        "pm_management": "📋 *إدارة طرق الدفع*\n\nاختر خياراً أدناه:",
        "list_methods": "📋 قائمة الطرق",
        "add_method": "➕ إضافة طريقة",
        "edit_method": "✏️ تعديل طريقة",
        "delete_method": "🗑️ حذف طريقة",
        "no_methods": "📭 *لا توجد طرق دفع متاحة.*",
        "pm_list": "📋 *طرق الدفع*\n\n{methods_list}",
        "add_method_step1": "➕ *إضافة طريقة دفع*\n\nالخطوة 1/6: أدخل معرفاً فريداً\n\n📝 *مثال:* `barq`، `newpay`\n\nاكتب /cancel للإلغاء.",
        "add_method_step2": "✅ المعرف: `{key}`\n\nالخطوة 2/6: أدخل الاسم المعروض\n\n📝 *مثال:* `💳 محفظة بارق`",
        "add_method_step3": "✅ الاسم: {name}\n\nالخطوة 3/6: كم عدد الحقول التي تحتاجها هذه الطريقة؟\n\n📝 *أمثلة:*\n• بارق: حقل واحد (رقم_الهاتف)\n• تحويل بنكي: حقلان (رقم_الهاتف، الآيبان)\n\nاختر رقماً:",
        "add_method_step4": "✅ تم اختيار {count} حقول.\n\nالخطوة 4/6: أدخل الحقل #{index}\n\n📝 *أمثلة:* {examples}\n\nأدخل اسم الحقل:",
        "add_method_step5": "✅ تمت إضافة الحقول: {fields}\n\nالخطوة 5/6: أدخل قيماً لكل حقل\n\n📝 أدخل قيمة *{field}*:",
        "add_method_step6": "📝 أدخل قيمة *{field}*:",
        "add_method_success": "✅ *تمت إضافة طريقة الدفع!*\n\n🔹 الاسم: {name}\n📌 المعرف: `{key}`\n📝 الحقول: {fields}\n📋 القيم:\n{values}",
        "edit_method_prompt": "✏️ *تعديل طريقة الدفع*\n\nاختر الطريقة التي تريد تعديلها:",
        "edit_method_selected": "✏️ *تعديل: {name}*\n\n📌 المعرف: `{key}`\n📝 الحقول: {fields}\n📋 التفاصيل: {details}\n\nاختر الحقل الذي تريد تعديله:",
        "edit_method_field": "✏️ *تعديل: {field}*\n\nالقيمة الحالية: `{current}`\n\nأدخل القيمة الجديدة:",
        "edit_method_success": "✅ *تم تحديث الطريقة!*\n\n📌 المعرف: `{key}`\n📝 {field}: {value}",
        "delete_method_prompt": "🗑️ *حذف طريقة الدفع*\n\nاختر الطريقة التي تريد حذفها:",
        "delete_method_confirm": "🗑️ *حذف الطريقة؟*\n\n🔹 الاسم: {name}\n📌 المعرف: `{key}`\n\n⚠️ *هل أنت متأكد؟*\nلا يمكن التراجع عن هذا الإجراء!",
        "delete_method_yes": "✅ نعم، حذف",
        "delete_method_no": "❌ لا، إلغاء",
        "delete_method_success": "✅ *تم حذف الطريقة `{key}`!*",
        "delete_method_cancelled": "❌ *تم إلغاء الحذف!*",
        "invalid_id": "❌ *معرف غير صالح!*\n\nاستخدم فقط الحروف والأرقام والشرطات السفلية.",
        "id_exists": "❌ *المعرف `{id}` موجود بالفعل!*",
        "invalid_number": "❌ *رقم غير صالح!*\n\nيرجى إدخال رقم بين 1 و 5.",
        "method_not_found": "❌ *الطريقة `{key}` غير موجودة!*",
        "field_not_found": "❌ *الحقل `{field}` غير موجود!*",
        "invalid_fields": "❌ *حقول غير صالحة!*",
        "edit_details_not_allowed": "❌ *لتعديل التفاصيل، قم بتعديل الحقول الفردية.*",
        
        # Admin commands
        "unauthorized": "⛔ *غير مصرح!*",
        "add_account_help": "📝 *كيفية إضافة حساب:*\n\n`/ass اسم_المستخدم: 123456789 كلمة_المرور: abcd1234`\n\n**مثال:**\n`/ass اسم_المستخدم: Ahmed_123 كلمة_المرور: SecurePass456`\n\nيمكنك أيضاً إضافة多个:\n`/ass اسم_المستخدم: user1 كلمة_المرور: pass1, اسم_المستخدم: user2 كلمة_المرور: pass2`",
        "add_account_invalid": "❌ *صيغة غير صالحة!*\n\nاستخدم:\n`/ass اسم_المستخدم: Ahmed كلمة_المرور: 123456`",
        "add_account_no_valid": "❌ *لم يتم العثور على حسابات صالحة!*",
        "add_account_success": "✅ *تمت إضافة {count} حساب!*\n\n{accounts}\n\n📦 *الإجمالي المتاح:* {total}\n💰 *جميع الحسابات تحصل على 30% كاش باك!*",
        "no_accounts_to_list": "📭 *لا توجد حسابات متاحة.*",
        "accounts_list_admin": "📋 *الحسابات المتاحة ({count})*\n\n{accounts}\n\n💰 *30% كاش باك على جميع الخسائر!*",
        "delete_account_help": "📝 `/del اسم_المستخدم: player1`",
        "delete_account_invalid": "❌ *صيغة غير صالحة!*\n\nاستخدم: `/del اسم_المستخدم: player1`",
        "delete_account_not_found": "❌ *لم يتم العثور على حساب باسم `{username}`!*",
        "delete_account_success": "✅ *تم حذف الحساب!*\n\nتمت إزالة: `{account}`\n📦 *الإجمالي المتاح:* {total}",
        "clear_accounts_confirm": "🗑️ *تم مسح {count} حساب!*\n\n📦 *الإجمالي المتاح:* 0",
        "no_accounts_to_clear": "📭 *لا توجد حسابات للمسح!*",
        "reset_user_help": "📝 الاستخدام: `/resetuser معرف_المستخدم`",
        "reset_user_success": "✅ *تم إعادة تعيين المستخدم {user_id}!*",
        "reset_user_not_found": "❌ *المستخدم {user_id} غير موجود.*",
        
        # Common
        "cancel": "/cancel",
        "custom_amount": "✏️ أدخل مبلغاً مخصصاً",
        "unknown_command": "❌ *لا أفهم هذا الأمر.*\n\nيرجى استخدام الأزرار أدناه:",
        "enter_amount": "📝 *أدخل المبلغ المخصص:*\n\nيرجى إدخال المبلغ بالريال (10-500 ريال):",
        "please_send_photo": "❌ *يرجى إرسال صورة!*",
        
        # Admin withdrawal states
        "withdraw_amount_prompt": "يرجى إدخال مبلغ السحب بالريال:",
        "withdraw_amount_invalid": "❌ *مبلغ غير صالح!*\n\nيرجى إدخال رقم موجب صحيح.",
        "withdraw_amount_session_expired": "❌ *انتهت الجلسة!*\n\nيرجى محاولة قبول السحب مرة أخرى.",
        
        # Stats menu options
        "stats_menu_options": "📊 *قائمة الإحصائيات*\n\nاختر خياراً أدناه:",

        # ----- NEW KEYS ADDED -----
        "receipt_caption": "📸 إيصال الإيداع {deposit_id}",
        "video_play_caption": "🎬 *{title}*\n\n📹 فيديو تعليمي\n📅 تاريخ الإضافة: {date}",
        "video_list_item": "🆔 المعرف: `{vid}`\n🎬 العنوان: {title}\n📅 تاريخ الإضافة: {date}",
        "withdraw_video_caption": "🎬 *{title}*\n\n📹 شاهد هذا الفيديو التعليمي للحصول على التعليمات خطوة بخطوة!",
        # --------------------------
        "cashback_video_caption": "🎬 *دروس الكاش باك*\n\n📹 شاهد هذا الفيديو التعليمي لمعرفة كيفية الحصول على 5% كاش باك والمزيد في تطبيق 1xBet!\n\n💰 بعد المشاهدة، اطلب الـ 25% المتبقية من الكاش باك أدناه.",
        "cashback_video_not_found": "📹 *الفيديو غير موجود!*\n\nيرجى الاتصال بالمدير.",
        "cashback_request_message": (
            "💰 *طلب كاش باك 30%*\n\n"
            "📌 *كيف يعمل:*\n"
            "• تحصل بالفعل على 5% كاش باك في التطبيق\n"
            "• اطلب الـ 25% المتبقية هنا\n\n"
            "📝 *الخطوة 1/2:* أدخل معرف اللاعب في 1xBet\n\n"
            "مثال: `123456789`\n\n"
            "اكتب /cancel للإلغاء."
        ),
    }
}

def t(user_id, key, **kwargs):
    """
    Translation helper function.
    Usage: t(user_id, "welcome_text", name="John")
    """
    from user_language import get_user_language
    
    lang = get_user_language(user_id)
    text = LANGUAGES.get(lang, LANGUAGES["en"]).get(key, key)
    
    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError as e:
            print(f"Missing translation key: {e}")
            return text
    return text
