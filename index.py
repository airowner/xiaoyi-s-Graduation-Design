# _*_ coding: utf-8 _*_
import os, sys
import web, xy_db

import datetime, urllib, glob 


urls = (
    '/', 'index', # 首页
    '/myphoto', 'myphoto', # 我的相薄
    '/message(/.*)?', 'message', # 给我留言
    '/case', 'case', #所学课程
    '/mypower', 'mypower', #个人能力
    '/myprofile', 'myprofile', #个人简介
    '/jobtarget', 'jobtarget', #求职意向
    '/images', 'images', #图像
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
        left = render.myphoto() 
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
        return render.layout(info, left, self.sidebar())

    def POST(self, tid=None):
        data = {}
        for k, v in web.input().iteritems():
            data[k] = v.strip()

        for k, v in web.ctx.iteritems():
            if k == 'environ':
                refer = v['HTTP_REFERER']
                break
        if not refer:
            refer = '/'
            
        if not data['name'] or not data['email'] or not data['message']:
            return web.seeother(refer + '?msg=' + urllib.quote('评论失败'))

        parent = data.get('id', '')

        ret = _db.addLeavemsg(data['name'], data['email'], data['message'], parent=parent, message=data['rows'])
        if not ret['parent']:
            web.seeother('/message/' + ret['id'] + '?msg=' + urllib.quote('评论成功'))
        else:
            web.seeother('/message/' + ret['parent'] + '?msg=' + urllib.quote('评论成功'))

class case(base):
    def GET(self):
        info = {}
        info['title'] = '所学课程'
        left = render.case()
        return render.layout(info, left, self.sidebar())

class mypower(base):
    def GET(self):
        info = {}
        info['title'] = '个人能力'
        left = render.mypower()
        return render.layout(info, left, self.sidebar())

class myprofile(base):
    def GET(self):
        info = {}
        info['title'] = '个人简介'
        left = render.myprofile()
        return render.layout(info, left, self.sidebar())

class jobtarget(base):
    def GET(self):
        info = {}
        info['title'] = '求职意向'
        left = render.archives_main()
        return render.layout(info, left, self.sidebar())

class images:
    def GET(self):
        imgroot = os.path.abspath(os.path.curdir) + '/static/img'
        httproot = web.ctx.homedomain + '/static/img/'
        xml = '<?xml version="1.0" encoding="utf-8"?>\n<pics>\n'
        for pic in glob.glob(imgroot + '/*'):
            if os.path.isfile(pic) and os.path.splitext(pic)[1] in [ '.jpg', '.png' ]:
                xml += '<pic src="' + httproot + os.path.basename(pic) + '" title="'+os.path.basename(pic)+'" />\n'
        xml += '</pics>\n'
        return xml

if __name__ == '__main__':
    os.chdir(sys.path[0])
    
    #web.application.internalerror = web.debugerror
    app.run()
