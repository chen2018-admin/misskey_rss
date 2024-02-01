# RSS 订阅，发布到misskey上面
在他的基础上做了一部分调整，非常感谢，我想合并的，但是我玩github不是很熟悉，非常抱歉

## 安装

在开始之前，请先按照此说明操作一次：

### 在 Misskey 上创建一个帐户并获取您的机器人的 APIKEY。

- 进入你的实例
- 创建一个新的用户
- Remember to set `isBot = True`
- 访问以下页面，创建一个apikey `https://your.misskey.instance/settings/api`
- 至少需要笔记的编辑权限 `notes:write`

### 准备一个python的虚拟环境
推荐使用python3

1. `git clone`克隆这个仓库或者下载源代码
2. `python -m venv .venv` 创建你的虚拟环境，或者使用virtualen创建，具体可以自己搜索相关教程
3. `. .venv/bin/activate` 激活你的虚拟环境
4. `pip install -r requirements.txt` 安装需要的库
5. `python -m spacy download en_core_web_lg` 下载`en_core_web_lg`在解析的时候用到

## 配置

安装好了之后需要进行少量的配置

### 用 RSS feed 填充机器人

首先，新建一个sources.yaml文件，将 RSS Feed 源放到其中中。多个的话就写多个的
```yaml
- title: 别名
  url: 订阅的rss源地址
  channelId: 频道的id 实例：a5bxs2kfut
- title: 别名
  url: 订阅的rss源地址
  channelId: 频道的id 实例：a5bxs2kfut
```

### 环境变量

复制.env-example到.env以填写您的个人配置：

- **HOST** 你misskey的地址，比如misskey.example.com
- **APIKEY** 上面创建的apikey
- **VISIBILITY** 选择发布在哪个 [时间轴](https://misskey-hub.net/en/docs/features/timeline.html).
- **LOCAL** 是否本地
- **EVERY_MINUTES** 发帖的频率
- **HOW_MANY** 一次发几个

## 运行

进入到你的虚拟环境中运行这个

`(env) $ python feed_bot.py`

如果需要，它将进行设置。然后将启动三个预定作业。

### 服务守护进程配置

您可能希望通过使用nohup或运行screen命令来与控制台分离地运行它。这样就可以不停地关闭ssh shell。

该软件能够避免多个并发运行。

## 停止

控制台使用`CTRL+C`.

## 升级

只需停止！然后git pull检查更新。然后pip-review -a更新库。需要重新启动才能完成任务。

