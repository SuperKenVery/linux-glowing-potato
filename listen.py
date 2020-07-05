import re
class classroom:
    c,m,e,p,ch,h,b,g,po,pe='语文 数学 英语 物理 化学 历史 生物 地理 政治 体育'.split(' ')
    teachers={'乔战胜':b,
              '终結者':ch,
              '张简':g,
              '王文悦':c,
              '曹建民':po,
              'zoe':e,
              '陈坤':p,
              '梁宏':h,
              '方善泽':m,
              '孟祥标':pe
              }
    sr={#subject representatives
        '王语桐':c,
        '林飞':m,'张涛':m,
        '张善':e,'洪锦奕':e,
        '李欣慰':'大合集',
        '欣慰':'大合集'
        }

blacklist=['刘瑞珏','腾讯课堂六星教育python十一群']

class chatHistory:
    def __init__(self,history=[],file=r'..\history.data'):
        self.histories=history
        self.print=''
        self.printall=''
    def append(self,argv):
        self.histories.append(argv)
        self.print+=argv+'\n'
    def __str__(self): 
        self.printall+=self.print
        r=self.print[:]
        self.print=''
        return r
 
def notify(title,body=''):
    core.os.system('notify-send -a "WeChat Helper" "%s" "%s"'%(title,body))

def initmodule():
    global history,mute,allFolders,emojiFilter,listenThread
    listenThread=core.threading.Thread(target=listen)
    listenThread.daemon=True
    history=chatHistory()
    mute=False
    allFolders=set(classroom.teachers.values())|set(classroom.sr.values())
    for i in allFolders:
        if not core.os.path.isdir(i): core.os.mkdir(i)
    emojiFilter=re.compile(u'[\U00010000-\U0010ffff]')


def connectionError(e,*argv):
    core.itchat.logout()

def register():
    try:    core.itchat.error_register(True)(connectionError)
    except: pass
    
    @core.itchat.msg_register(core.itchat.content.ATTACHMENT,isGroupChat=True)
    def gotGroupAttachment(msg):
        sender=emojiFilter.sub('',msg['ActualNickName'])
        group=emojiFilter.sub('',msg['User']['NickName'])
        path=core.path
        if not mute and (sender not in blacklist) and (group not in blacklist):
            notify('收到%s'%msg['FileName'],'来自%s'%sender)
        if sender in classroom.teachers.keys():
            path=core.os.path.join(path,classroom.teachers[sender])
        elif sender in classroom.sr.keys():
            path=core.os.path.join(path,classroom.sr[sender])
        core.convert.processFile(filename=msg['FileName'],path=path,getter=msg['Text'])
        return None

    @core.itchat.msg_register(core.itchat.content.PICTURE,isGroupChat=True)
    def gotGroupPicture(msg):
        path=core.path
        sender=emojiFilter.sub('',msg['ActualNickName'])
        group=emojiFilter.sub('',msg['User']['NickName'])
        if sender in classroom.teachers.keys():
            path=core.os.path.join(path,classroom.teachers[sender])
        elif sender in classroom.sr.keys():
            path=core.os.path.join(path,classroom.sr[sender])
        else:
            return
        n=core.os.path.join(path,msg['FileName'])
        
        with open(n,'wb') as f:
            f.write(core.convert.download(msg['Text']))
        if not mute and (group not in blacklist) and (sender not in blacklist):
            core.subprocess.Popen(['xdg-open',n],stdout=core.subprocess.DEVNULL,stderr=core.subprocess.DEVNULL)
        history.append(group[:3]+'\t'+sender+' 发了一张图片\t存储在'+n)

    @core.itchat.msg_register(core.itchat.content.TEXT,isGroupChat=True)
    def gotGroupText(msg):
        global lastGroup
        path=core.path
        sender=emojiFilter.sub('',msg['ActualNickName'])
        group=emojiFilter.sub('',msg['User']['NickName'])
        msg['Text']=emojiFilter.sub('',msg['Text'])
        if not mute and (sender not in blacklist) and (group not in blacklist):
            notify(sender+'\t('+group+')',msg['Text'])
        history.append(group[:3]+'\t'+sender+':'+msg['Text'])
        if sender in classroom.teachers.keys():
            path=core.os.path.join(path,classroom.teachers[sender])
            with open(core.os.path.join(path,'chat.txt'),'ab') as f:
                f.write(('老师:'+'\t'+msg['Text']+'\n').encode('utf-8'))
        elif sender in classroom.sr.keys():
            path=core.os.path.join(path,classroom.sr[sender])
            with open(core.os.path.join(path,'chat.txt'),'ab') as f:
                f.write(('科代表:'+'\t'+msg['Text']+'\n').encode('utf-8'))
        lastGroup=msg['User']['NickName']

    @core.itchat.msg_register(core.itchat.content.TEXT,isFriendChat=True)
    def gotFriendText(msg):
        sender=emojiFilter.sub('',msg['User']['NickName']) if 'NickName' in msg['User'].keys() else '我'
        msg['Text']=emojiFilter.sub('',msg['Text'])
        if not notify and (sender not in blacklist): notify(sender,msg['Text'])
        history.append(sender+':'+msg['Text'])

    @core.itchat.msg_register([core.itchat.content.ATTACHMENT,core.itchat.content.PICTURE],isFriendChat=True)
    def gotSelfAttachment(msg):
        if not 'NickName' in msg['User'].keys():
            notify('Got SELF File',msg['FileName'])
            core.convert.processFile(msg['FileName'],core.path,msg['Text'],always=True)
            return None

def listen():
    def setLoggedIn():
        p=core.shell.inputprompt
        p.status=core.termcolor.colored('listening','green',attrs=['bold'])
        p.updatePrompt()
    def exitcallback():
        if not core.shell.loggingout:
            core.itchat.logout()
            p=core.shell.inputprompt
            p.status=core.termcolor.colored('re-logging in','magenta',attrs=['dark','bold'])
            p.updatePrompt()
    while not core.shell.loggingout:
        core.itchat.auto_login(hotReload=True,
                        enableCmdQR=False,
                        statusStorageDir='../itchat.pkl',
                        loginCallback=setLoggedIn,
                        exitCallback=exitcallback
                        )
        import logging 
        itchatlogger=logging.getLogger('itchat')
        itchatlogger.setLevel(50)
        core.itchat.run()

    
def start():
    listenThread.start()

if __name__=='__main__':
    print("Please run ocHelper.py")
