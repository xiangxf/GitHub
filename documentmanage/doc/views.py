from django.shortcuts import render
from doc.models import UserInfo,DepartmentInfo,FileInfo
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from documentmanage.settings import MEDIA_ROOT
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
import os
# Create your views here.

def d_login(request):

    if request.POST.get('username'):
        username1=request.POST['username']
        user=authenticate(username=request.POST['username'],password=request.POST['password'])
        if user:
            login(request,user)
            usersy = User.objects.get(username=username1).id
            useracc=UserInfo.objects.get(user=usersy).accesstype
            request.session['username']=str(username1)
            if str(useracc)=='0':
                return choice(request)
            else:

                request.session['depart']=str(UserInfo.objects.get(user=usersy).departno.id)
                request.session['acctype']=str(useracc)
                return  show_file(request)
            return show_file(request)
    return render_to_response('login.html',context_instance=RequestContext(request))

def d_logout(request):
    logout(request)
    return d_login(request)

def choice(request):
    depart=DepartmentInfo.objects.all()
    user=User.objects.all()
    return  render_to_response('admin/choice.html',locals(),context_instance=RequestContext(request))



def show_file(request):
    acc=request.session.get('acctype')
    if request.session.get('acctype')=='1':
        file=FileInfo.objects.all()
    else:
        depart=request.session.get('depart')
        departde=DepartmentInfo.objects.get(id=depart)
        file=FileInfo.objects.filter(departno=departde)
    return render_to_response('depart/showfile.html',locals(),context_instance=RequestContext(request))

def add_depart(request):
    if request.POST.get('departname'):
        departname1=request.POST['departname']
        departinfo1=request.POST['departinfo']

        d=DepartmentInfo(departname=departname1,departinfo=departinfo1)
        d.save()
        return choice(request)
    return render_to_response('admin/adddepart.html',context_instance=RequestContext(request))


def modify_depart(request,did):
    m = DepartmentInfo.objects.get(id=did)
    if request.method=='POST':
        m.departname=request.POST['newdepartname']
        m.departinfo=request.POST['departinfo']
        m.save()
        return choice(request)
    return render_to_response('admin/modifydepart.html',locals(),context_instance=RequestContext(request))

def reset_pass(request):
    if request.POST.get('userID'):
        usern=request.POST['userID']
        oldpwd=request.POST['oldpwd']
        user=authenticate(username=usern,password=oldpwd)
        print usern,oldpwd,user
        if user:
            print "login"
            newpwd = request.POST.get('pwd')
            print newpwd
            user.set_password(newpwd)
            user.save()
            return choice(request)
    return render_to_response('admin/resetpass.html',context_instance=RequestContext(request))

@csrf_exempt
@csrf_protect
def upload(request):
    if request.method == 'POST':
        print request.FILES['file']
        upfile = request.FILES['file']
        f=handlefile(upfile)
        filename=upfile.name
        filedetail=upfile
        depart = request.session.get('depart')
        print "~~~~~~~~~~~~",depart
        departinfo=DepartmentInfo.objects.get(id=depart)
        ff=FileInfo(filename=upfile.name,file=filedetail,departno=departinfo)
        ff.save()
        return show_file(request)
    return show_file(request)

def handlefile(f):
    f_path = MEDIA_ROOT+f.name
    with open(f_path,'wb+') as info:
        for chunk in f.chunks():
            info.write(chunk)
        return f

def delete(request,fileid):
    f=FileInfo.objects.get(id=fileid)
    f.delete()
    return show_file(request)

def download(request,fid):
    fil=FileInfo.objects.get(id=fid).file
    fname=FileInfo.objects.get(id=fid).filename
    fpath=MEDIA_ROOT+str(fil)
    f=open(fpath)
    data = f.read()
    f.close()
    response = HttpResponse(data,mimetype='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename=%s' % fname
    return response







def modify(request,uid):
    if request.method=='POST':
        f=FileInfo.objects.get(id=uid)
        if request.POST['filename']:
            f.filename=request.POST['filename']
        if request.POST['departid']:
            f.departno_id=request.POST['departid']
        f.save()
        return show_file(request)
    return render_to_response('depart/modify.html',context_instance=RequestContext(request))


