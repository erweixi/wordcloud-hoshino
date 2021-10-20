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

sv = Service('wordcloud', enable_on_default=True)

loadpath = ''#此处填gocq的logs路径
self_id = ''#此处填机器人的QQ号
load_in_path = ''#此处填词云图片保存的路径


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
        
@sv.on_rex(f'^查询(.*)月(\d+)日词云$')
async def ciyun(bot, ev: CQEvent):
    match = ev['match']
    month = int(match.group(1))
    day = int(match.group(2))
    await bot.send(ev,MessageSegment.image(f'file:///{load_in_path}//2021-{month:02}-{day:02}.png'))

@sv.on_fullmatch('生成今日词云')
async def getciyun(bot, ev: CQEvent):
    if not hoshino.priv.check_priv(ev, hoshino.priv.OWNER):
        await bot.send(ev,message = '仅限群主可用',at_sender = True)
        return
    await bot.send(ev,message = '正在生成本群今日词云，请耐心等待',at_sender = True)
    gid = ev.group_id
    makeclouds(gid)
    today = datetime.date.today().__format__('%Y-%m-%d')
    await bot.send(ev,MessageSegment.image(f'file:///{load_in_path}//{today}-{gid}.png'))


@sv.on_fullmatch('生成昨日词云')
async def getciyunb(bot, ev: CQEvent):
    if not hoshino.priv.check_priv(ev, hoshino.priv.OWNER):
        await bot.send(ev,message = '仅限群主可用',at_sender = True)
        return
    await bot.send(ev,message = '正在生成本群昨日词云，请耐心等待',at_sender = True)
    gid = ev.group_id
    makecloudsb(gid)
    yesterday = (datetime.date.today() + datetime.timedelta(-1)).__format__('%Y-%m-%d')
    await bot.send(ev,MessageSegment.image(f'file:///{load_in_path}//{yesterday}-{gid}.png'))
    
def random_color_func(word=None, font_size=None, position=None,
                      orientation=None, font_path=None, random_state=None):
  
    if random_state is None:
        random_state = Random()
    return "hsl(%d, 75%%, 62%%)" % random_state.randint(0, 225)#值，饱和度，色相
    
def makeclouds(gid):
    global loadpath
    bot = nonebot.get_bot()
    today = datetime.date.today().__format__('%Y-%m-%d')
    f = open(loadpath + f"\\{today}.log", "r", encoding="utf-8")
    f.seek(0)
    gida = str(gid)
    msg=''
    for line in f.readlines():          #删除前缀和自己的发言
        if self_id in line or gida not in line:
            continue
        try:                         
            o = line.split("的消息: ")[1]
            msg += o  
        except:
            pass
    msg = re.sub('''[a-zA-Z0-9'!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘'！[\\]^_`{|}~\s]+''', "", msg)
    msg = re.sub('[\001\002\003\004\005\006\007\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a]+', '', msg)
    banword = []#此处为不显示的删除禁词
    ls = jieba.lcut(msg,cut_all=True)#制作分词
    stopwords = set()
    content = [line.strip() for line in open(load_in_path+f"\\tyc.txt",\
               encoding='utf-8').readlines()]
    stopwords.update(content)
    txt = " ".join(ls)
    w = wordcloud.WordCloud(font_path=load_in_path+f"\\SimHei.ttf",\
                            max_words=10000, width=1000, height=700,\
                            background_color='white',stopwords=stopwords,\
                            relative_scaling=0.5,min_word_length=2,\
                            color_func=random_color_func#调色
        )
    w.generate(txt)
    w.to_file(f"{today}-{gid}.png")
    if gid:
        try:
            shutil.move(f"{today}-{gid}.png",load_in_path)
        except:
            os.remove(load_in_path+f"\\{today}-{gid}.png")
            shutil.move(f"{today}-{gid}.png",load_in_path)
    else:
        try:
            shutil.move(f"{today}.png",load_in_path)
        except:
            os.remove(load_in_path+f"\\{today}.png")
            shutil.move(f"{today}.png",load_in_path)
        
        
def makecloudsb(gid):
    global loadpath
    bot = nonebot.get_bot()
    today = datetime.date.today().__format__('%Y-%m-%d')
    yesterday = (datetime.date.today() + datetime.timedelta(-1)).__format__('%Y-%m-%d')
    gida = str(gid)
    f = open(loadpath + f"\\{yesterday}.log", "r", encoding="utf-8")
    f.seek(0)
    msg=''
    for line in f.readlines():          #删除前缀和自己的发言
        if self_id in line or gida not in line:
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
    stopwords = set()
    content = [line.strip() for line in open(load_in_path+f"\\tyc.txt",encoding='utf-8').readlines()]
    stopwords.update(content)
    txt = " ".join(ls)
    w = wordcloud.WordCloud(font_path=load_in_path+f"\\SimHei.ttf",\
                            max_words=10000, width=1000, height=700,\
                            background_color='white',stopwords=stopwords,\
                            relative_scaling=0.5,min_word_length=2,\
                            color_func=random_color_func#词汇上限，宽，高,背景颜色去除停用词(tyc.txt),频次与大小相关度，最小词长,调色
        )
    w.generate(txt)
    w.to_file(f"{yesterday}-{gid}.png")
    if gid:
        try:
            shutil.move(f"{yesterday}-{gid}.png",load_in_path)
        except:
            os.remove(load_in_path+f"\\{yesterday}-{gid}.png")
            shutil.move(f"{yesterday}-{gid}.png",load_in_path)
    else:
        try:
            shutil.move(f"{yesterday}.png",load_in_path)
        except:
            os.remove(load_in_path+f"\\{yesterday}.png")
            shutil.move(f"{yesterday}.png",load_in_path)
