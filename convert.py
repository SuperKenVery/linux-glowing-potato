import zipfile,os
#def notify   injected from listen
def parseFileName(filename):
    splitted=filename.split('.')
    name=''
    for i in splitted[:-1]:
        name+=i+'.'
    name=name[:-1]
    end=splitted[-1]
    return name,end

def download(downfunc,tryTimes=10,fail=lambda *argv,**argvs:notify("Download Failed")):
    for i in range(tryTimes):
        try:
            data=downfunc()
        except BaseException as e:
            fail(e)
        else:
            return data

def rename(path,name,end):
    fullname=os.path.join(path,name+'.'+end)
    filename=name+'.'+end
    guess=os.popen('file --extension "%s"'%fullname).read().split(': ')[1].split('/')[0]
    if (not '???' in guess) and (end is not guess):
        os.rename(fullname,os.path.join(path,name+'.'+guess))
        filename=name+'.'+guess
        end=guess
    return filename,end
def processFile(filename,path,getter=None,always=False):
    if type(filename)==list:
        for f,g in zip(filename,getter):
            processFile(f,path,g,always)
        return
    if filename=='': return
    name,end=parseFileName(filename)
    if always==True or (end in ['doc','docx','pdf','zip','ppt','pptx','xls','xlsx','mp3','png','jpg','jpeg','rar']):
        if hasattr(getter,'__call__'):
            data=download(getter)
            with open(os.path.join(path,filename),'wb') as f:
                f.write(data)
        filename,end=rename(path,name,end)
        if end=='doc' or end=='docx':
            fullname=os.path.join(path,filename)
            os.popen('libreoffice --convert-to odt "%s" --outdir "%s" >> /dev/null'%(fullname,path))
            odtname=os.path.join(path,parseFileName(filename)[0]+'.odt')
            while not os.path.isfile(odtname): time.sleep(0.01)
            os.remove(fullname)
            os.popen('libreoffice --convert-to pdf "%s" --outdir "%s" >> /dev/null'%(odtname,path))
            pdfname=os.path.join(path,parseFileName(filename)[0]+'.pdf')
            while not os.path.isfile(pdfname): time.sleep(0.01)
        elif end=='zip':
            manager=zipfile.ZipFile(os.path.join(path,filename))
            fullnames=manager.namelist()
            filenames=[i.split('/')[-1] for i in fullnames]
            getters=[lambda f=i:manager.read(f) for i in fullnames]
            processFile(filenames,path,getters,always)
        else:
            pass

if __name__=='__main__':
    from listen import notify
    import time
    print("Please run wechatHelper.py")
    path='/home/ken/Desktop/grab/2020-04-20/'
    name='英语/200420-110013'
    end='png'
    fullname=os.path.join(path,name+'.'+end)
    print(fullname)
    guess=os.popen('file --extension "%s"'%fullname).read().split(': ')[1].split('/')[0]
    print(guess)
    if (not '???' in guess) and (end is not guess):
        print("rename %s to %s"%(fullname,os.path.join(path,name+'.'+guess)))
        os.rename(fullname,os.path.join(path,name+'.'+guess))
        filename=name+'.'+guess
        end=guess