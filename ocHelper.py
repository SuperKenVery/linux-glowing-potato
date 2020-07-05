#!/usr/bin/python3
import sys
class Core:
    '''An object to transfer data between py files'''
    def __init__(self,argv=[]): #argv:sys.argv[1:]
        try:
            import itchat,os,sys,datetime,subprocess,termcolor,time,threading
        except ModuleNotFoundError:
            print('''In order to run this, you'll need to have some module installed.
Required modules:
    itchat,termcolor''')
        self.itchat     =itchat
        self.os         =os
        self.sys        =sys
        self.datetime   =datetime
        self.subprocess =subprocess
        self.termcolor  =termcolor
        self.time       =time
        self.threading  =threading
        inFolder=os.path.expanduser('~/School/Materials/')
        today=datetime.date.today()
        if '--clean' in argv:
            argv.remove('--clean')
            pkl=os.path.join(inFolder,'itchat.pkl')
            if os.path.isfile(pkl):
                os.remove(pkl)
        if len(argv)==0:
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
        else:
            year,month,day=today.year,today.month,today.day
            day=int(argv[-1])
            if len(argv)>=2: month=int(argv[-2])
            if len(argv)>=3: year=int(argv[-3])
            today=datetime.date(year,month,day)
        todayFolder=str(today)
        self.path=os.path.join(sys.path[0],inFolder,todayFolder)



if __name__=='__main__':
    import shell,convert,listen,sys,os


    core=Core(sys.argv[1:])
    if not core.os.path.isdir(core.path):
        core.os.makedirs(core.path)
    core.os.chdir(core.path)

    core.shell          =shell
    core.convert        =convert
    core.listen         =listen

    core.itchat.loggedIn=False

    listen.core         =core
    listen.initmodule()
    listen.register()
    listen.start()

    convert.core        =core
    
    shell.core          =core
    shell.init_lessons()
    shell.run()
