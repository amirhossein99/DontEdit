#-*- coding: utf-8 -*-
import telebot
import logging
import json
import os
from telebot import util
import re
from random import randint
import random
import requests as req
import requests
import commands
import urllib2
import urllib
import telebot
import ConfigParser
import redis as r
import redis as redis
from telebot import types
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
token = 'Token' #توکن بات
bot = telebot.TeleBot(token)
redis = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
is_sudo = '192593495' #ایدی شما
bot_id = '123639273' #ایدی بات شما

print "Bot Now Is on"

markupstart = types.InlineKeyboardMarkup()
markupstart.add(types.InlineKeyboardButton('🌀اد کردن به گروه🌀', url='https://telegram.me/DontEdit_API_Bot?startgroup=new'))
markupstart.add(types.InlineKeyboardButton('👤توسعه دهنده👤', url='https://telegram.me/ApiCli'), types.InlineKeyboardButton('📢کانال📢', url='https://telegram.me/Special_Programing'))

@bot.message_handler(commands=['toall'])
def toall(m):
    if str(m.from_user.id) == is_sudo:
        text = m.text.replace('/toall','')
        rd = redis.smembers('startmebot')
        for id in rd:
            try:
                bot.send_message(id, "{}".format(text), parse_mode="Markdown")
            except Exception as e:
                print(e)

@bot.message_handler(commands=['togroups'])
def toall(m):
    if str(m.from_user.id) == is_sudo:
        text = m.text.replace('/togroups','')
        rd = redis.smembers('ourgroups')
        for id in rd:
            try:
                bot.send_message(id, "{}".format(text), parse_mode="Markdown")
            except Exception as e:
                print(e)

@bot.message_handler(commands=['stats'])
def stats(m):
    if str(m.from_user.id) == is_sudo:
        stats = redis.scard('startthebot')
        bot.send_message(m.chat.id, "`تعداد کاربران`👇\n*{}*".format(stats), parse_mode="Markdown")

@bot.message_handler(commands=['groups'])
def stats(m):
    if str(m.from_user.id) == is_sudo:
        stats = redis.scard('ourgroups')
        bot.send_message(m.chat.id, "`تعداد گروه ها`👇\n*{}*".format(stats), parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def start(m):
    if not m.chat.type == "supergroup" or m.chat.type == "group":
        id = m.chat.id
        redis.sadd('startthebot',id)
        bot.send_message(m.chat.id, """
سلام {} 😊
من ربات ادیت نکن هستم😍
یعنی میتونم توی گروه وقتی کسی پیام خودشو ادیت کرد بفهمم که قبل ادیت کردن پیامش چی گفت و مچشو بگیرم😎
لطفا منو به گروهت اد کن تا مچ دوستاتو بگیرم😈
""".format(m.from_user.first_name), reply_markup=markupstart)

@bot.message_handler(content_types=['new_chat_member'])
def hi(m):
    if m.new_chat_member.id == bot_id and m.chat.type == "supergroup" or m.chat.type == "group":
        redis.sadd("ourgroups",m.chat.id)
        title = m.chat.title
        name = m.from_user.first_name
        bot.send_message(m.chat.id, """
مرسی که منو اد کردی {} 😃
سلام به اعضای گروه {} 😊
من ربات ادیت نکن هستم😎
هر کی که ادیت کنه پیام خودشو من میفهمم که قبلش چی گفت و توی گروه ارسال میکنم تا مچشو بگیرم😃
شما هم میتونین بیاین پی ویم استارت بدین و منو به گروهاتون اد کنید🙂👋
""".format(name,title))

@bot.edited_message_handler(func=lambda message: True)
def plain_text(m):
    if m.chat.type == "supergroup" or m.chat.type == "group":
        text = redis.hget("messages:{}".format(m.from_user.id),"{}".format(m.message_id))
        name = m.from_user.first_name
        bot.reply_to(m, """

{}
من میدونم قبل ادیت کردن چی گفتی😜
بازم ادیت کنی میفهمم🙄
🗣گفتی:
{}
""".format(name,text))
        redis.hdel("messages:{}".format(m.from_user.id),"{}".format(m.message_id))
        redis.hset("messages:{}".format(m.from_user.id),"{}".format(m.message_id),"{}".format(m.text))

@bot.message_handler(content_types=['text'])
def plain_text(m):
    if m.chat.type == "supergroup" or m.chat.type == "group":
        redis.hset("messages:{}".format(m.from_user.id),"{}".format(m.message_id),"{}".format(m.text))
bot.polling(True)

#Writen by @ApiCli
