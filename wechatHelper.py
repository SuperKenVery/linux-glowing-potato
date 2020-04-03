import itchat,os,sys,datetime

inFolder='grab'
todayFolder=str(datetime.date.today())
path=os.path.join(sys.path[0],inFolder,todayFolder)

if not os.path.isdir(path):
    os.makedirs(path)
os.chdir(path)

if __name__=='__main__':
    import shell,convert,listen

    itchat.loggedIn=False

    listen.itchat       =itchat
    listen.shell        =shell
    listen.register()
    listen.start()

    convert.notify      =listen.notify
    convert.time        =shell.time

    shell.notify        =listen.notify
    shell.itchat        =itchat
    shell.history       =listen.history
    shell.listen        =listen
    shell.wechatHelper  =listen.wechatHelper
    shell.run()
