# _*_ coding: utf-8 _*_
import web

urls = (
    '/', 'index', # 首页
    '/myphoto', 'myphoto', # 我的相薄
    '/message', 'message', # 给我留言
    '/case', 'case', #所学课程
    '/mypower', 'mypower', #个人能力
    '/myprofile', 'myprofile', #个人简介
    '/jobtarget', 'jobtarget', #求职意向
    )

app = web.application(urls, globals())

t_globals = {
        '_SERVER': web.ctx,
        'nav': [ '/', '/myphoto', '/message', '/case', '/mypower', '/myprofile', '/jobtarget' ],
        'nav_name': [ '首页', '我的相薄', '给我留言', '所学课程', '个人能力', '个人简介', '求职意向' ],
        }
render = web.template.render('template', globals=t_globals)


class index:
    def GET(self):
        info = {}
        info['title'] = '首页'
        left = render.style_main()
        right = render.style_right()
        return render.layout(info, left, right)

class myphoto:
    def GET(self):
        info = {}
        info['title'] = '我的相薄'
        left = render.index() 
        right = ''
        return render.layout(info, left, right)

class message:
    def GET(self):
        info = {}
        info['title'] = '给我留言'
        left = ''
        right = ''
        return render.layout(info, left, right)

class case:
    def GET(self):
        info = {}
        info['title'] = '所学课程'
        left = ''
        right = ''
        return render.layout(info, left, right)

class mypower:
    def GET(self):
        info = {}
        info['title'] = '个人能力'
        left = ''
        right = ''
        return render.layout(info, left, right)

class myprofile:
    def GET(self):
        info = {}
        info['title'] = '个人简介'
        left = ''
        right = ''
        return render.layout(info, left, right)

class jobtarget:
    def GET(self):
        info = {}
        info['title'] = '求职意向'
        left = ''
        right = ''
        return render.layout(info, left, right)

if __name__ == '__main__':
    web.application.internalerror = web.debugerror
    app.run()
