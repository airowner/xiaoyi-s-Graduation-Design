# _*_ coding: utf-8 _*_
import web

urls = (
    '/', 'index', # 首页
    '/', 'myphoto', # 我的相薄
    '/', 'message', # 给我留言
    '/', 'case', #所学课程
    '/', 'mypower', #个人能力
    '/', 'myprofile', #个人简介
    '/', 'jobtarget', #求职意向
    )

app = web.application(urls, globals())
render = web.template.render('template', base='layout.html')


class index:
    def GET(self):
        return render.index()



if __name__ == '__main__':
    app.run()
