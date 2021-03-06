loggingout=False
def lessshow(msg):
    if isinstance(msg,list):
        x=''
        for i in msg:
            x+=i+'\n'
        x=x[:-1]
        lessshow(x)
    else:
        msg=str(msg)
        cmd='echo "%s" | less'%msg.replace('"','\\"')
        core.os.system(cmd)
def _stopNotify(t=None):
    core.listen.mute=True
    if t:
        def start(st=t):
            core.time.sleep(int(st)*60)#in minutes
            _startNotify()
        p=core.threading.Thread(target=start)
        p.start()
def _startNotify():
    core.listen.mute=False
def _idlecls():
    print('\n'*40)
def _exit():
    global loggingout
    loggingout=True
    core.itchat.logout()
    exit()
def _reconnect():
    core.itchat.logout()
def _history(history,every):
    if every==False:
        lessshow(str(history))
    elif every=='--all':
        lessshow(history.printall)
    else:
        print("Unknown operation "+str(every))
def init_lessons():
    global lessons,times
    mo,c,m,e,p,ch,b,h,po,g,s,cl,mu,a,ps,it,pe="早读 语文 数学 英语 物理 化学 生物 历史 政治 地理 自习 班会 音乐 美术 心理 信息 体育".split(' ')
    t=core.datetime.time
    times=[(t(7,30),t(7,50)),(t(8,0),t(8,40)),(t(9,00),t(9,40)),(t(10,0),t(10,40)),(t(11,00),t(11,40)),(t(14,00),t(14,40)),(t(15,00),t(15,40)),(t(16,00),t(16,40)),(t(17,00),t(17,40))]
    lessons=[
        [mo,e,ch,b,m,p,c,po,cl],
        [mo,c,m,e,p,g,h,s,mu],
        [mo,po,m,e,c,pe,ch,s,h],
        [mo,g,c,e,p,b,m,a,ps],
        [mo,e,m,ch,p,it,c,b,s]
        ]
def which():
    '''
        tells you which lesson is it
        returns (status, class index, weekday)

        status: 0=weekend
                1=weekday,after school
                2=weekday, having class
                3=weekday,during break

        if not in class, then now it's the class' break.
    '''
    now=core.datetime.datetime.now()
    time,weekday=now.time(),now.weekday()
    if not weekday in [0,1,2,3,4]:#weekend
        return (0,-1,weekday)
    for index,lesson in enumerate(times):
        if lesson[0]<time<lesson[1]:
            return (2,index,weekday)
        elif time<lesson[0]:
            return (3,index-1,weekday)
    else:
        return (1,-1,weekday)
def _timeTable():
    status,index,weekday=which()
    if status>=2:
        print(*lessons[weekday],sep='  ')
        msg='      '*index + ('^~~~' if status==2 else '    ^~')
    else:
        msg='今天周末！' if status==0 else '课都上完啦！~'
    print(msg)
def nothing(*argv):
    pass
def parseFilename(filename):
    folders=filename.split('/')
    path=''
    for i in folders[:-1]:
        path+=i+'/'
    name=folders[-1]
    return path,name
def _process(*filenames):
    for filename in filenames:
        if core.os.path.isdir(filename):
            _process(*[core.os.path.join(filename,i) for i in core.os.listdir(filename)])
        else:
            path,name=parseFilename(filename)
            core.convert.processFile(filename,path)
def _send(*filenames):
    for filename in filenames:
        if core.os.path.isdir(filename):
            _send(*[core.os.path.join(filename,i) for i in core.os.listdir(filename)])
        elif core.os.path.isfile(filename):
            core.itchat.send_file(filename,toUserName='filehelper')
        else:
            core.itchat.send(filename,toUserName='filehelper')
def _folder(*argv):
    if '--gui' in argv:
        if not '--all' in argv:
            core.subprocess.Popen(['nautilus',core.path],stdout=core.subprocess.DEVNULL,stderr=core.subprocess.DEVNULL)
        else:
            for i in core.listen.allFolders:
                if core.os.listdir(i)!=[]:
                    core.subprocess.Popen(['nautilus',core.os.path.join(core.path,i)],stdout=core.subprocess.DEVNULL,stderr=core.subprocess.DEVNULL)
    else:
        core.os.system("ranger")
def _allhomework(*argv):
    '''
        argv:
        edit    edit all chat.txt using gedit
        gui     show homework in gui, otherwise in cli
        no-sr   no subject representative 
    '''
    path=core.path
    homework=''
    if '--edit' in argv:
        for i in core.listen.allFolders:
            name=core.os.path.join(path,i,'chat.txt')
            core.os.system("gedit %s >> /dev/null &"%name)
    else:
        for i in core.listen.allFolders:
            recname=core.os.path.join(path,i,'chat.txt')
            if core.os.path.isfile(recname):
                with open(recname) as f:
                    homework+=i+':\n'+f.read()+'\n'
        if '--no-sr' in argv:
            lines=homework.split('\n')
            diff=0
            status=''
            for i in range(len(lines)):
                if lines[i+diff][0:3]=='科代表':
                    status=1
                elif lines[i+diff][0:2]=='老师':
                    status=0
                if status==1:
                    del lines[i+diff]
                    diff-=1
            homework='\n'.join(lines)
        if not '--gui' in argv:
            lessshow(homework)
        else:
            with open("homework.txt",'w') as f:
                f.write(homework)
            core.os.system('xdg-open "homework.txt" >> /dev/null &')

commands={
    'help': lambda:lessshow([str(i) for i in commands.keys()]),
    'send':_send,
    'folder':_folder,
    'history':lambda every=False:_history(core.listen.history,every),
    'cls':lambda:core.os.system("clear"),
    'clear':lambda:core.os.system("clear"),
    'mute':_stopNotify,
    'dnd':_stopNotify,#do not disturb
    'ring':_startNotify,
    'unmute':_startNotify,
    'dndoff':_startNotify,
    'idlecls':_idlecls,
    'exit':_exit,
    'reconnect':_reconnect,
    'reboot':_reconnect,
    'process':_process,
    'table':_timeTable,
    'lessons':_timeTable,
    'time':_timeTable,
    'homework':_allhomework,
    '':nothing
    }
class prompt:
    def __init__(self,start=None,name=None,status=None):
        self.start=start or core.termcolor.colored('➜','green',attrs=['bold'])
        self.name=name or core.termcolor.colored('(OC Helper)','cyan',attrs=['bold'])
        self.status=status or core.termcolor.colored('listening','green',attrs=['bold'])
        self.generateMsg()
        self.y=self.x=0
    def generateMsg(self):
        self.msg=self.start+' '+self.name+' '+self.status+' '
    def updatePrompt(self):
        print('\b'*len(self.msg),end='',flush=True)
        oriLength=len(self.msg)
        self.generateMsg()
        print(self.msg,end='',flush=True)
        lendiff=len(self.msg)-oriLength
        if lendiff<0: 
            lendiff=-lendiff
            print(' '*lendiff,flush=True,end='')
            print('\b'*lendiff,flush=True,end='')
    def run(self,os,subprocess):
        while True:
            print(self.msg,end='',flush=True)
            try: 
                user_input=input()
                self.execute(user_input)
            except KeyboardInterrupt: print("Type exit to exit. ")
    def execute(self,user_input):
        try:
            parsed=self.parse(user_input.strip())
            commands[parsed[0]](*parsed[1:])
        except KeyboardInterrupt:
            print('Cancled by user. ')
        except TypeError as e:
            print("Argument Error. \n%s"%str(e))
        except KeyError:
            ret=core.os.popen(user_input)
            print(ret.read())
        except SystemExit:
            exit()
        except BaseException as e:
            print("Unknown Error. ",str(e))
    def parse(self,cmd):
        x=['']
        inPara=False
        direct=False
        for i in cmd:
            if direct:
                x[-1]+=i
                direct=not direct
                continue
            if i=='\\':
                direct=True
                continue
            if i in ['"',"'"]:
                inPara=not inPara
                continue
            if inPara:
                x[-1]+=i
            else:
                if i==' ':
                    x.append('')
                else:
                    x[-1]+=i
        return x

def run():
    global inputprompt
    inputprompt=prompt(status=core.termcolor.colored('waiting for login','magenta',attrs=['dark','bold']))
    inputprompt.run(core.os,core.subprocess)
if __name__=='__main__':
    print("Please run ocHelper.py")
    lessshow('''
        A long text ' to " test less\\ show
    ''')
