# coding=utf-8

import os, web, time, hashlib

def toUnicode(text):
    if type(text).__name__ == 'unicode':
        return text
    elif type(text).__name__ == 'str':
        return unicode(text, 'utf-8')
    else:
        return unicode(str(text), 'utf-8')

def toStr(text):
    if type(text).__name__ == 'unicode':
        return text.encode('utf-8')
    else:
        return str(text)
    
class ExistsRecordError(Exception): pass

class XYDB:
    def __init__(self):

        dbfile = os.path.realpath(os.curdir) + '/test.db'
        self.db = web.database(dbn="sqlite", db=dbfile)
        self.db.supports_multiple_insert = True
        
        if not os.path.exists(dbfile):
            """
            category 分类
            parent   第一次发表为空，如果是回复，则这里是原消息的id字段
            user     用户名
            email    用户email
            title    标题
            time     添加时间戳
            message  内容
            id       哈希， md5(category + user + title), 限制: 同一个用户再同一分类下不能发表目录名一致的文章
            """
            self.db.query("create table topic ( category text, parent text, user text, email text, title text, time real, message text, id text )")

            #留言板
            self.addLeavemsg("zhanghua", "airowner@gmail.com", "你好，很高兴认识你丫!")
            self.addLeavemsg("陈怡", "295387148@qq.com", "你好，认识你也很高兴", parent="d4eafca37aa5908a497dfd527a72bb2a", message="d4eafca37aa5908a497dfd527a72bb2a")
            self.addLeavemsg("zhanghua", "airowner@gmail.com", "QQ是多少啊？可以加个好友吗？", parent="d4eafca37aa5908a497dfd527a72bb2a", message="db382e936792b162f0bc429f312456b9")
            self.addLeavemsg("yanyan", "enenqin@gmail.com", "好久不见，最近怎么样啊!")

            #课程
            self.addCase("陈怡", "295387148@qq.com", "语文", message="2012-02-07~2012-02-08 语文语文")
            self.addCase("陈怡", "295387148@qq.com", "数学", message="2012-02-07~2012-02-08 数学数学")
            self.addCase("陈怡", "295387148@qq.com", "英语", message="2012-02-07~2012-02-08 英语英语")
            self.addCase("陈怡", "295387148@qq.com", "自习", message="2012-02-07~2012-02-08 自习自习")
            self.addCase("陈怡", "295387148@qq.com", "地理", message="2012-02-07~2012-02-08 地理地理")

            #相册
            self.addAlbum("陈怡", "295387148@qq.com", "我的风采")
            self.addAlbum("陈怡", "295387148@qq.com", "校园风光")


    def insert(self, category, user, email, title, **keys):
        ret = {}
        ret['category'] = toUnicode(category)
        ret['user'] = toUnicode(user)
        ret['email'] = toUnicode(email)
        ret['title'] = toUnicode(title)
        ret['id'] = XYDB.getID(ret['category'], ret['user'], ret['title'])
        if len(list(self.db.select('topic', where='category='+web.sqlquote(category)+' and id='+web.sqlquote(ret['id'])))):
            raise ExistsRecordError('record is exists')
        ret['time'] = int(time.time())
        ret['parent'] = ''
        ret['message'] = ''
        for k, v in keys.items():
            ret[k] = toUnicode(v)

        self.db.multiple_insert('topic', [ret])

        return ret

    #留言板
    def addLeavemsg(self, user, email, title, **keys):
        return self.insert(u'leavemsg', user, email, title, **keys)
    
    #课程
    def addCase(self, user, email, title, **keys):
        return self.db.multiple_insert('topic', [self.commonParam(u'case', user, email, title, **keys)])

    #相册
    def addAlbum(self, user, email, title, **keys):
        return self.db.multiple_insert('topic', [self.commonParam(u'album', user, email, title, **keys)])

    #个人能力
    def addPower(self, user, email, title, **keys):
        return self.db.multiple_insert('topic', [self.commonParam(u'power', user, email, title, **keys)])

    #个人简介
    def addProfiles(self, user, email, title, **keys):
        return self.db.multiple_insert('topic', [self.commonParam(u'profile', user, email, title, **keys)])

    #求职意向
    def addJob(self, user, email, title, **keys):
        return self.db.multiple_insert('topic', [self.commonParam(u'job', user, email, title, **keys)])


    @staticmethod
    def getID(category, user, title):
        return hashlib.md5(toStr(category) + toStr(user) + toStr(title)).hexdigest()

    def getCommon(self, category, **kws):
        where = "category=" + web.sqlquote(category)
        if kws.has_key("where"):
            where += " and " + kws["where"]
            del kws["where"]
        if kws.has_key("order"):
            order = kws["order"]
            del kws["order"]
        else:
            order = "time desc"
            
        return self.db.select("topic", where=where, order=order, **kws)

    def getLeavemsg(self, **kws):
        return self.getCommon("leavemsg", **kws)
    
    def getRight(self):
        return self.getLeavemsg(limit="5")


if __name__ == "__main__":
    import sys
    os.chdir(sys.path[0])
    print('curpath:' + sys.path[0]+"\n\n")
    if os.path.exists(os.path.realpath(os.curdir) + '/test.db'):
        os.unlink(os.path.realpath(os.curdir) + '/test.db')

    db = XYDB()
    print(list(db.db.select('topic')))

    for i in db.db.select("topic").list():
        print i
    msgs = db.getCommon('leavemsg', where="user="+web.sqlquote('zhanghua') )
    print msgs
    for i in msgs.list():
        print i.user

    print db.addLeavemsg("zhanghua", "airowner@gmail.com", "你好，很高兴认识你丫!")
    print db.addLeavemsg("陈怡", "295387148@qq.com", "你好，认识你也很高兴")
    
