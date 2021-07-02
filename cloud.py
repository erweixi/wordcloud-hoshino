import jieba
import re
import nonebot
import wordcloud
import hoshino
from hoshino.typing import CQEvent
from hoshino import Service,R
from nonebot import MessageSegment,NoticeSession
import base64
from PIL import Image
import numpy as np
import datetime
import shutil
import os

sv = Service('wordcloud', enable_on_default=False)

loadpath = ''#此处填gocq的data路径
self_id = ''#此处填机器人的QQ号
load_in_path = ''#此处填词云图片保存的路径


@sv.on_rex(f'^查询(.*)月(\d+)日词云$')
async def ciyun(bot, ev: CQEvent):
    match = ev['match']
    month = int(match.group(1))
    day = int(match.group(2))
    await bot.send(ev,MessageSegment.image(f'file:///{load_in_path}//2021-{month:02}-{day:02}.png'))

@nonebot.scheduler.scheduled_job(
    'cron',
    day='*',
    hour='23',
    minute='55'
)
async def makecloud():
    bot=nonebot.get_bot()
    try:
        makeclouds()
    except Exception as e:
        today = datetime.date.today().__format__('%Y-%m-%d')
        await bot.send_private_msg(user_id=hoshino.config.SUPERUSERS[2], message=f'{today}词云生成失败,失败原因:{e}')

@sv.on_fullmatch('生成今日词云')
async def getciyun(bot,ev):
    if not hoshino.priv.check_priv(ev, hoshino.priv.SUPERUSER):
        return
    await bot.send(ev,message = 'execute',at_sender = True)
    makeclouds()



def makeclouds():
    global loadpath
    bot = nonebot.get_bot()
    today = datetime.date.today().__format__('%Y-%m-%d')
    f = open(loadpath + f"\\gocq\\logs\\{today}.log", "r", encoding="utf-8")
    f.seek(0)
    msg=''
    for line in f.readlines():          #删除前缀和自己的发言
        if self_id in line:
            continue
        try:                         
            o = line.split("的消息: ")[1]
            msg += o  
        except:
            pass
    msg = re.sub('''[a-zA-Z0-9'!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘'！[\\]^_`{|}~\s]+''', "", msg)
    msg = re.sub('[\001\002\003\004\005\006\007\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a]+', '', msg)
    banword = []#此处为不显示的删除禁词
    ls = jieba.lcut(msg)#制作分词
    txt = " ".join(ls)
    w = wordcloud.WordCloud( \
        width = 1000, height = 618,\
        max_words = 114514,\
        background_color = "white",regexp="\d*"
        )
    w.generate(msg)
    w.to_file(f"{today}.png")
    try:
        shutil.move(f"{today}.png",load_in_path)
    except:
        os.remove(load_in_path+f"\\{today}.png")
        shutil.move(f"{today}.png",load_in_path)
