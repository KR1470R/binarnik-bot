import telebot
from telebot import types, util
import re
from datetime import datetime


#TOKEN = '************************************************' # My bot
TOKEN = '************************************************'	# Deploy bot
bot = telebot.TeleBot(TOKEN)
text_field = ''
mode = ''

welcome_text = """
> Gimme binary or text and i convert it.
"""

def text_to_bits(text, encoding='utf-8', errors='ignore'):
  try:
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))
  except Exception as e:
    return '> Error 0x1. Something went wrong.'

def text_from_bits(bits, encoding='utf-8', errors='ignore'):
  try:
    if len(bits) == 1:
    	if bits == '1' or '0':
    		n = int(bits, 1)
    else:
    	n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors)
  except Exception as e:
    print('> Error 0x1. Something went wrong. Try text_to_bits func.')
    mode = 'ttb'
    return text_to_bits(bits)


@bot.inline_handler(lambda query: len(query.query) > 0)
def query_text(inline_query):
    global r
    text_field = inline_query.query
    pattern = re.compile(r"[a-zA-Z0-9А-Яа-я<!\[.*?\]>+-=]+")
    pattern_binar = re.compile("[0-1]+")
    split_message = []
    mode = ''
    count_spaces = 0
    get_regex_binar = []
    try:
        if text_field == 'Beer' or text_field == 'beer' or text_field == 'пиво' or text_field == 'Пиво' or text_field == 'Пивас' or text_field == 'пивас' or text_field == 'Пивасик' or text_field == 'пивасик' or text_field == 'Пивусик' or text_field == 'пивусик':
            r = types.InlineQueryResultArticle(id = '1', title = 'Output:', description = text_to_bits(inline_query.query), input_message_content=types.InputTextMessageContent(message_text = "> Take your beer, Sir!🍻🍺"))
            return
        for i in str(text_field):
            if (i.isspace())==True:
                count_spaces+=1
            if pattern.fullmatch(text_field) is not None or count_spaces>=1:
                if re.search(r'([0-1])',text_field):
                    mode = 'btt'
                    text_field = text_field.split()
                    splitted_text = util.split_string(''.join(text_field), 3000)
                    for text in splitted_text:
                        r = types.InlineQueryResultArticle(id = '1', title = 'Output:', description = text_from_bits(''.join(text)), input_message_content=types.InputTextMessageContent(message_text = text_from_bits(''.join(text))))
                    text_field = ''.join(text_field)
                    break
                else:
                    mode = 'ttb'
                    splitted_text = util.split_string(text_field, 200)
                    for text in splitted_text:
                        r = types.InlineQueryResultArticle(id = '1', title = 'Output:', description = text_to_bits(''.join(text)), input_message_content=types.InputTextMessageContent(message_text = text_to_bits(''.join(text))))
                    break
    except Exception as e:
        print(e)
        print(" All: \n" + str(inline_query))
    bot.answer_inline_query(inline_query.id, [r])



@bot.message_handler(commands=['start'])
def welcome(message):
		bot.send_message(message.chat.id, welcome_text)

@bot.message_handler(content_types=['text'])
def enter_text(message):
	text_field = message.text
	#pattern = re.compile(r"[a-zA-Z0-9А-Яа-я<!\[.*?\]>+-]+")
	pattern = re.compile(r"[a-zA-Z0-9А-Яа-я<!\[.*?\]>+-=]+")
	pattern_binar = re.compile("[0-1]+")
	split_message = []
	mode = ''
	count_spaces = 0
	get_regex_binar = []
	if message.chat.type == 'private':
		if text_field == 'Beer' or text_field == 'beer' or text_field == 'пиво' or text_field == 'Пиво' or text_field == 'Пивас' or text_field == 'пивас' or text_field == 'Пивасик' or text_field == 'пивасик' or text_field == 'Пивусик' or text_field == 'пивусик':
			bot.send_message(message.chat.id, '> Take your beer, Sir!🍻🍺')
			return
		for i in str(text_field):
			if (i.isspace())==True:
				count_spaces+=1
			if pattern.fullmatch(text_field) is not None or count_spaces>=1:
				if re.search(r'([0-1])',text_field):
					mode = 'btt'
					text_field = text_field.split()
					splitted_text = util.split_string(''.join(text_field), 3000)
					for text in splitted_text:
						bot.send_message(message.chat.id,text_from_bits(''.join(text)))
					text_field = ''.join(text_field)
					break
				else:
					mode = 'ttb'
					splitted_text = util.split_string(text_field, 200)
					for text in splitted_text:
						bot.send_message(message.chat.id,text_to_bits(''.join(text)))
					break
		now = datetime.now()
		current_time = now.strftime("%Y/%m/%d;%H:%M:%S") #на 3 часа позднит по моему времени.
		get_first_name = str(message.from_user.first_name)
		get_last_name = str(message.from_user.last_name)
		get_username = str(message.from_user.username)
		if get_first_name == 'None':
			get_first_name = 'No first name'
		if get_last_name == 'None':
			get_last_name = 'No last name'
		print('LOG ->>'+current_time+' , '+'User data - '+str(get_first_name)+':'+str(get_last_name)+':'+str(get_username)+' , '+'message_text: '+"* "+text_field+" *"+' , mode - '+mode)
		mode = ''
		count=0
	else:
		bot.send_message(message.chat.id, '> Error! Please try again!')
# RUN
bot.polling(none_stop=True)