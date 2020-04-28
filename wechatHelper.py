#!/usr/bin/python3
try:
    import itchat,os,sys,datetime,subprocess
except ModuleNotFoundError as e:
    print("Some required modules arn't installed. ")
    print("Use 'pip3 install <module name>' to install it. ")
    print(str(e))
    exit()

inFolder=os.path.expanduser('~/School/Materials/')
today=datetime.date.today()
toweek=today.weekday()
if toweek in [5,6]:#Saturday, Sunday. Weekday is 0-based. 
    y,m,d=today.year,today.month,today.day
    d-=toweek-4 #Calculate how many days from Friday. Again, 0-based. 
    if d<=0:
        last_month_days=(datetime.date(y,m,1)-datetime.date(y,m-1,1)).days
        m-=1
        d+=last_month_days
        if m<=0:
            m+=12
    today=datetime.date(y,m,d)
todayFolder=str(today)
path=os.path.join(sys.path[0],inFolder,todayFolder)

if not os.path.isdir(path):
    os.makedirs(path)
os.chdir(path)


if __name__=='__main__':
    import shell,convert,listen

    itchat.loggedIn=False

    listen.itchat       =itchat
    listen.shell        =shell
    listen.subprocess   =subprocess
    listen.register()
    listen.start()

    convert.notify      =listen.notify
    convert.time        =shell.time
    convert.subprocess  =subprocess

    shell.notify        =listen.notify
    shell.itchat        =itchat
    shell.history       =listen.history
    shell.listen        =listen
    shell.wechatHelper  =listen.wechatHelper
    shell.subprocess    =subprocess
    shell.run()
