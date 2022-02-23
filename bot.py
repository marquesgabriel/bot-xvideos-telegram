import os
from telegram import Update, ParseMode
from telegram.ext import CommandHandler, CallbackContext, Updater
from bs4 import BeautifulSoup
import emoji

from xvideos import choose_random_porn_comment, choose_random_video

BOT_TOKEN = os.getenv('BOT_TOKEN')

updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

def formatMessage(message):
  soup = BeautifulSoup(message)
  workedMessage= soup.getText()
  return emoji.emojize(workedMessage)

def meajuda(update: Update, ctx: CallbackContext):
  print("called help")
  ctx.bot.send_message(chat_id=update.effective_chat.id, text='*Olá, Aqui estão os comandos:*\n \- `/mensagem` \- Procura um comentario aleatório no Xvideos em Portugês\n \- `/busca *termo*` \- Procura um video pelo termo passado, se não passado nenhum, é retornado um video aleatório\n \- `!meajuda` \- Mostra esta mensagem\.\n\n Encontrou algum problema ou tem alguma sugestão para o bot? Sinta\-se livre para nos enviar uma mensagem por este [link](https://github.com/marquesgabriel/bot-xvideos-telegram/issues)', parse_mode=ParseMode.MARKDOWN_V2)

  # update.effective_message

  ctx.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)

def mensagem(update: Update, ctx: CallbackContext):
    print("called mensagem")
    sentMessage = ctx.bot.send_message(chat_id=update.effective_chat.id, text='**Buscando\.\.\.\n**', parse_mode=ParseMode.MARKDOWN_V2)
    try:
        author, comment, title, url = choose_random_porn_comment()
        author = '**O '+author+'  comentou o seguinte:**\n'
        title = '**vi isso no [video](https://xvideos.com'+url+'):**\n`'+title+'`'
        ctx.bot.send_message(chat_id=update.effective_chat.id, text=author, parse_mode=ParseMode.MARKDOWN_V2)
        ctx.bot.send_message(chat_id=update.effective_chat.id, text=formatMessage(comment))
        ctx.bot.send_message(chat_id=update.effective_chat.id, text=title, parse_mode=ParseMode.MARKDOWN_V2)
    except Exception :
        ctx.bot.send_message(chat_id=update.effective_chat.id, text='Houve uma falha na busca. Tente novamente.')
    ctx.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
    ctx.bot.delete_message(chat_id=update.effective_chat.id, message_id=sentMessage.message_id)


def busca(update: Update, ctx: CallbackContext):
  print("called busca")
  # update.message.from.id
  try:
      term = '+'.join(update.message.text.replace("/busca ", ""))
      link = choose_random_video(term)
      ctx.bot.send_message(chat_id=update.effective_chat.id, text='Segura esse [link]('+link+') aí meu parceiro', parse_mode=ParseMode.MARKDOWN_V2)
  except Exception:
      ctx.bot.send_message(chat_id=update.effective_chat.id, text='Houve uma falha na busca. Tente novamente.')
  ctx.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)

start_handler = CommandHandler('start', meajuda)
help_handler = CommandHandler('meajuda', meajuda)
message_handler = CommandHandler('mensagem', mensagem)
search_handler = CommandHandler('busca', busca)


dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(message_handler)
dispatcher.add_handler(search_handler)

updater.start_polling()
print("Bot Online!")