# _*_ coding: utf-8 _*_
import web, xy_db

import datetime


urls = (
    '/', 'index', # 首页
    '/myphoto', 'myphoto', # 我的相薄
    '/message(/.*)?', 'message', # 给我留言
    '/case', 'case', #所学课程
    '/mypower', 'mypower', #个人能力
    '/myprofile', 'myprofile', #个人简介
    '/jobtarget', 'jobtarget', #求职意向
    )

app = web.application(urls, globals())
now = datetime.datetime.utcnow()

def Timestringify(timestamp):
    return web.datestr(datetime.datetime.utcfromtimestamp(timestamp), now=now)

t_globals = {
        '_SERVER': web.ctx,
        'nav': [ '/', '/myphoto', '/message', '/case', '/mypower', '/myprofile', '/jobtarget' ],
        'nav_name': [ '首页', '我的相薄', '给我留言', '所学课程', '个人能力', '个人简介', '求职意向' ],
        'timestringify': Timestringify,
        'now': now,
        }

render = web.template.render('template', globals=t_globals)
_db = xy_db.XYDB()

class base:
    def __init__(self):
        self.msg = web.input(msg='')
        
    def sidebar(self):
        return unicode(render.right(_db.getRight()))

class index(base):
    def GET(self):
        info = {}
        info['title'] = '首页'
        left = render.style_main()
        return render.layout(info, left, self.sidebar())

class myphoto(base):
    def GET(self):
        info = {}
        info['title'] = '我的相薄'
        left = render.style_main() 
        return render.layout(info, left, self.sidebar())

class message(base):
    def GET(self, tid=None):
        info = {}
        info['title'] = '给我留言'
        msgs = {}
        reply = []
        if tid:
            tid = tid[1:]
            msgs = list(_db.getLeavemsg(where='id='+web.sqlquote(tid)))[0]
            reply = _db.getLeavemsg(where='parent='+web.sqlquote(tid), order='time asc')
        left = unicode(render.message(msgs, list(reply)))
        return render.layout(info, left, self.sidebar(), self.msg)

    def POST(self, tid=None):
        data = web.input()
        for k, v in web.ctx.iteritems():
            if k == 'environ':
                refer = v['HTTP_REFERER']
                break
        if not refer:
            refer = '/'
            
        if not data.name or not data.email or not data.message:      
            return web.seeother(refer + '?msg=评论失败')
        parent = data.get('id', '')
        _db.addLeavemsg(data.name, data.email, data.message, parent=parent, message=data.rows)
        return web.seeother(refer + '?msg=评论成功')

class case(base):
    def GET(self):
        info = {}
        info['title'] = '所学课程'
        left = render.archives_main()
        return render.layout(info, left, self.sidebar())

class mypower(base):
    def GET(self):
        info = {}
        info['title'] = '个人能力'
        left = ''
        return render.layout(info, left, self.sidebar())

class myprofile(base):
    def GET(self):
        info = {}
        info['title'] = '个人简介'
        left = ''
        return render.layout(info, left, self.sidebar())

class jobtarget:
    def GET(self):
        info = {}
        info['title'] = '求职意向'
        left = ''
        return render.layout(info, left, self.sidebar())

if __name__ == '__main__':
    import os, sys
    os.chdir(sys.path[0])
    
    #web.application.internalerror = web.debugerror
    app.run()
