import pdb,threading,time,os,convert,datetime,termcolor
loggingout=False
def printLines(l):
    x=''
    for i in l:
        x+=i+'\n'
    x=x[:-1]
    print(x)
def _stopNotify(t=None):
    listen.mute=True
    if t:
        def start(st=t):
            time.sleep(int(st)*60)#in minutes
            _startNotify()
        p=threading.Thread(target=start)
        p.start()
def _startNotify():
    listen.mute=False
def _idlecls():
    print('\n'*40)
def _exit():
    global loggingout
    loggingout=True
    itchat.logout()
    exit()
def _reconnect():
    itchat.logout()
def _history(history,every):
    if every==False:
        print(history)
    elif every=='all':
        print(history.printall)
    else:
        print("Unknown operation "+str(every))
mo,c,m,e,p,ch,b,h,po,g,s,cl,mu,a,ps,it,pe="早读 语文 数学 英语 物理 化学 生物 历史 政治 地理 自习 班会 音乐 美术 心理 信息 体育".split(' ')
t=datetime.time
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
    now=datetime.datetime.now()
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
        if os.path.isdir(filename):
            _process(*[os.path.join(filename,i) for i in os.listdir(filename)])
        else:
            path,name=parseFilename(filename)
            convert.processFile(filename,path)
def _send(*filenames):
    for filename in filenames:
        if os.path.isdir(filename):
            _send(*[os.path.join(filename,i) for i in os.listdir(filename)])
        elif os.path.isfile(filename):
            itchat.send_file(filename,toUserName='filehelper')
        else:
            itchat.send(filename,toUserName='filehelper')
def _folder(every=None):
    if every==None:
        os.popen('nautilus '+wechatHelper.path)
    elif every=='all':
        for i in listen.allFolders:
            if os.listdir(i)!=[]:
                os.popen('nautilus '+os.path.join(wechatHelper.path,i))
    else:
        print("Unknown operation "+str(every))
def _allhomework(*argv):
    '''
        argv:
        edit    edit all chat.txt using gedit
        gui     show homework in gui, otherwise in cli
        no-sr   no subject representative 
    '''
    path=wechatHelper.path
    homework=''
    if 'edit' in argv:
        for i in listen.allFolders:
            name=os.path.join(path,i,'chat.txt')
            os.system("gedit %s >> /dev/null &"%name)
    else:
        for i in listen.allFolders:
            recname=os.path.join(path,i,'chat.txt')
            if os.path.isfile(recname):
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
            print(homework)
        else:
            with open("homework.txt",'w') as f:
                f.write(homework)
            os.system('xdg-open "homework.txt"')

commands={
    'help': lambda:printLines(commands.keys()),
    'send':_send,
    'folder':_folder,
    'history':lambda every=False:_history(history,every),
    'cls':lambda:os.system("clear"),
    'clear':lambda:os.system("clear"),
    'mute':_stopNotify,
    'dnd':_stopNotify,#do not disturb
    'ring':_startNotify,
    'unmute':_startNotify,
    'dndoff':_startNotify,
    'idlecls':_idlecls,
    'lastGroup':lambda:print(lastGroup),
    'exit':_exit,
    'reconnect':_reconnect,
    'reboot':_reconnect,
    'debug':pdb.set_trace,
    'process':_process,
    'table':_timeTable,
    'lessons':_timeTable,
    'time':_timeTable,
    'homework':_allhomework,
    '':nothing
    }
def parse(cmd):
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
        
def run(debug=False):            
    if not debug:
        while itchat.loggedIn==False: time.sleep(0.01)
    time.sleep(0.01)
    os.popen("clear")
    while True:
        try:
            x=termcolor.colored('>>>','green',attrs=['bold','blink'])
            c=parse(input(x).strip())
            commands[c[0]](*c[1:])
        except KeyboardInterrupt:
            print('Type "exit" to quit. (Doesn\'t work all the time)')
        except TypeError as e:
            print("Argument Error. %s"%str(e))
        except KeyError:
            print("Command not found: %s"%c[0])
        except SystemExit:
            exit()
        except BaseException as e:
            print("Unknown Error. ",str(e))


if __name__=='__main__':
    print("Please run wechatHelper.py")
    import wechatHelper,listen
    _allhomework('gui','no-sr')
