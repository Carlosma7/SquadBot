import telebot

# Markups Bot API to choose a function
def markup_functions():
	# Keyboard
	markup = telebot.types.InlineKeyboardMarkup(row_width = 1)
	# Buttons
	bt1 = (telebot.types.InlineKeyboardButton("Secret Santa \U0001f381", callback_data="secretsanta"))
	markup.add(bt1)

	return markup

# Markups Bot API to work with a Secret Santa
def markup_secret_santa():
	# Keyboard
	markup = telebot.types.InlineKeyboardMarkup(row_width = 1)
	# Buttons
	bt1 = (telebot.types.InlineKeyboardButton("Join", callback_data="ss0"))
	bt2 = (telebot.types.InlineKeyboardButton("Leave", callback_data="ss1"))
	bt3 = (telebot.types.InlineKeyboardButton("Set Limit", callback_data="ss2"))
	bt4 = (telebot.types.InlineKeyboardButton("Set Date", callback_data="ss3"))
	bt5 = (telebot.types.InlineKeyboardButton("Set Message", callback_data="ss4"))
	bt6 = (telebot.types.InlineKeyboardButton("Remove Secret Santa", callback_data="ss5"))
	bt7 = (telebot.types.InlineKeyboardButton("Start Secret Santa \U0001f381", callback_data="ss6"))
	markup.add(bt1, bt2, bt3, bt4, bt5, bt6, bt7)

	return markup