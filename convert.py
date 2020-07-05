import zipfile
#def notify   injected from listen
def parseFileName(filename):
    splitted=filename.split('.')
    name=''
    for i in splitted[:-1]:
        name+=i+'.'
    name=name[:-1]
    end=splitted[-1]
    return name,end

def download(downfunc,tryTimes=10,fail=lambda *argv,**argvs:core.listen.notify("Download Failed")):
    for i in range(tryTimes):
        try:
            data=downfunc()
        except BaseException as e:
            fail(e)
        else:
            return data

def rename(path,name,end):
    fullname=core.os.path.join(path,name+'.'+end)
    filename=name+'.'+end
    filecmd=core.subprocess.Popen(['file','--extension',fullname],stdout=core.subprocess.PIPE,stderr=core.subprocess.PIPE)
    guess=filecmd.stdout.read().decode().split(': ')[1].split('/')[0]
    if (not '???' in guess) and (end is not guess):
        core.os.rename(fullname,core.os.path.join(path,name+'.'+guess))
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
            with open(core.os.path.join(path,filename),'wb') as f:
                f.write(data)
        filename,end=rename(path,name,end)
        if end=='doc' or end=='docx':
            fullname=core.os.path.join(path,filename)
            core.subprocess.Popen(['libreoffice','--convert-to','odt',fullname,'--outdir','%s'%path],stdout=core.subprocess.DEVNULL,stderr=core.subprocess.DEVNULL).wait()
            odtname=core.os.path.join(path,parseFileName(filename)[0]+'.odt')
            core.os.remove(fullname)
            core.subprocess.Popen(['libreoffice','--convert-to','pdf',odtname,'--outdir','%s'%path],stdout=core.subprocess.DEVNULL,stderr=core.subprocess.DEVNULL).wait()
        elif end=='zip':
            manager=zipfile.ZipFile(core.os.path.join(path,filename))
            fullnames=manager.namelist()
            filenames=[i.split('/')[-1] for i in fullnames]
            getters=[lambda f=i:manager.read(f) for i in fullnames]
            processFile(filenames,path,getters,always)
        else:
            pass

if __name__=='__main__':
    from listen import notify
    import time
    import subprocess
    print("Please run ocHelper.py")
    path="/home/xu/School/Materials/2020-04-30/大合集/"
    name="4月30日.zip"
    processFile(name,path)
