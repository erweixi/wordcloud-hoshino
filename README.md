# wordcloud-hoshino
[原项目链接](https://github.com/erweixi/wordcloud-hoshino)<br> 
不知道为啥老装不好，所以自己改来改去总算勉强能用，仅做一些小小的改动<br> 
没学过python仅靠Java的知识捣鼓，能用已经很好了<br> 
指令 `生成今日词云` `生成昨日词云`<br> 
1.删除查询功能直接生成导出<br> 
2.词云更鲜艳，想搞个蓝色版奈何审美不咋地等我有空再搞<br> 
3.原项目是一天所有群的词云，这里改成本群一天的<br> 
4.对指令，单字，语气词进行剔除，如需增加不需要的词汇请在tyc.txt自己新开一行加<br> 
使用前请先确保你的gocq版本允许保存聊天记录（info)<br> 
并安装wordcloud库和jieba库<br>
## 部署方法<br>
1.新建一个文件夹wordcloud在里面`git clone https://github.com/othinus001/wordcloud-hoshino.git`<br>
2.修改里面路径和QQ号<br>
3.将tyc.txt和ttf字体文件丢进load_path并安装字体<br> 
tyc里是不想要的词，可以自己一行一行加<br> 

