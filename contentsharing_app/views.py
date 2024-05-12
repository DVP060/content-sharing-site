from django.shortcuts import render,redirect
from django.contrib import messages
import contentsharing_app.models as model
import bcrypt

# Create your views here.

def index(request):
    if request.session.get('username'):
        return redirect(home)
    return render(request,'index.html')

def home(request):
    return render(request,'homepage.html')

def dashboard(request):
    return render(request,'dashboard.html')

def signup(request):
    return render(request,'signup.html')

def password_to_hash(password):
    salt = bcrypt.gensalt()
    hpassword = bcrypt.hashpw(password.encode('utf-8'),salt)
    return hpassword.decode('utf-8'),salt

def saveSignup(request):
    if request.method == 'POST':
        print("in request")
        firstname = request.POST.get('first-name')
        lastname = request.POST.get('last-name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        zipcode = request.POST.get('postal-code')

        hash_password,salt = password_to_hash(password)

        print(firstname+lastname+email+str(hash_password)+str(zipcode))

        if model.reader.objects.filter(email=email).exists():
            messages.error(request,'please enter unique email and password')
        else:
            newObj = model.reader(name=firstname+"_"+lastname,email=email,password=hash_password,zip=int(zipcode))
            newObj.save()
            messages.success(request,'You are successfully registered')
            return redirect(index)
    return redirect(signup)

def saveSignin(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        print(email+password)
        print(type(password))

        if model.reader.objects.filter(email=email).exists():
            print("in condition")
            getReader = model.reader.objects.get(email=email)
            print(getReader.password)
            print(type(getReader.password))
            if bcrypt.checkpw(password.encode('utf-8'),getReader.password.encode('utf-8')):
                request.session['username'] = getReader.name
                request.session['userid'] = getReader.id
                request.session.save()
                return redirect(home)
            else:
                messages.error(request,'Password is wrong')
        else:
            messages.error(request,'email is wrong')
    return redirect(index)

def logout(request):
    del request.session['username']
    return redirect(index)

def gettingStarted(request):
    return render(request,'gettingstarted.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def sendContact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
    return redirect(contact)

def resource(request):
    resourceObjs = model.resource.objects.filter(isPublished=True)
    context = {
        "resources": resourceObjs
    }
    return render(request,'resource.html',context)

def singleResource(request,id):
    resourceObj = model.resource.objects.get(id=id)
    context = {
        "resource" : resourceObj
    }
    return render(request,'single-resource.html',context)

def createResource(request):
    return render(request,'create-resource.html')

def saveResource(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        img = None
        if request.FILES.get('res-img'):
            img = request.FILES['res-img']
        else:
            img = "resource-img/resource-default-image.png"
        link = None
        if request.POST.get('res-link'):
            link = request.POST.get('res-link')
        file = None
        if request.FILES.get('res-file'):
            file = request.FILES['res-file']
        isPublished = 0

        try:
            if model.resource.objects.filter(title=title).exists():
                messages.error(request,'Please enter unique title because it will already taken')
            else:
                if link == None:
                    print("in file")
                    resourceObj = model.resource(title=title, description=description, img=img, resfile=file,
                                                 isPublished=isPublished,
                                                 readerName=model.reader.objects.get(id=request.session['userid']))
                    resourceObj.save()
                    if resourceObj:
                        messages.success(request,'Resource created successfully')
                        return redirect(user_resources)
                elif file == None:
                    print("in link")
                    resourceObj = model.resource(title=title, description=description, img=img,
                                                 isPublished=isPublished, link=link,
                                                 readerName=model.reader.objects.get(id=request.session['userid']))
                    resourceObj.save()
                    if resourceObj:
                        messages.success(request, 'Resource created successfully')
                        return redirect(user_resources)
                elif file != None and link != None:
                    print("in file and link")
                    resourceObj = model.resource(title=title, description=description, img=img, resfile=file,
                                                 isPublished=isPublished, link=link,
                                                 readerName=model.reader.objects.get(id=request.session['userid']))
                    resourceObj.save()
                    if resourceObj:
                        messages.success(request, 'Resource created successfully')
                        return redirect(user_resources)
                else:
                    messages.error(request,'Please enter link or file')
        except Exception as e:
            print(e)
            messages.error(request,'Something went wrong')
    return redirect(createResource)

def editResource(request,id):
    resourceObj = model.resource.objects.get(id=id)
    print(resourceObj.resfile)
    context = {
        "resource" : resourceObj
    }
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        img = None
        if request.FILES.get('res-img'):
            img = request.FILES['res-img']
        else:
            img =  resourceObj.img
        link = None
        if request.POST.get('res-link'):
            link = request.POST.get('res-link')
        else:
            if resourceObj.link:
                link = resourceObj.link
        file = None
        if request.FILES.get('res-file'):
            file = request.FILES['res-file']
        else:
            if resourceObj.resfile:
                file = resourceObj.resfile

        try:
            if link == None:
                print("in file")
                resourceObj2 = model.resource.objects.filter(id=id).update(title=title, description=description, img=img, resfile=file,readerName=model.reader.objects.get(id=request.session['userid']))
                if resourceObj2:
                    return redirect(resource)
            elif file == None:
                print("in link")
                resourceObj2 = model.resource.objects.filter(id=id).update(title=title, description=description, img=img, link=link,
                                             readerName=model.reader.objects.get(id=request.session['userid']))
                if resourceObj2:
                    return redirect(resource)
            elif file != None and link != None:
                print("in file and link")
                resourceObj2 = model.resource.objects.filter(id=id).update(title=title, description=description, img=img, resfile=file,link=link,
                                             readerName=model.reader.objects.get(id=request.session['userid']))
                if resourceObj2:
                    return redirect(resource)
            else:
                messages.error(request,'Please enter link or file')
        except Exception as e:
            print(e)
            messages.error(request,'Something went wrong')
    return render(request,'edit-resource.html',context)


def user_resources(request):
    resourceObjs = model.resource.objects.filter(readerName=model.reader.objects.get(id=request.session.get('userid')))
    context = {
        "user_resources" : resourceObjs
    }
    return render(request,'user-resource-setting.html',context)

def user_resource_delete(request,id):
    resourceObj = model.resource.objects.filter(readerName=model.reader.objects.get(id=request.session.get('userid')),id=id)
    deleteObj = resourceObj.delete()
    if deleteObj:
        messages.info(request,'Resource Deleted Successfully')
    else:
        messages.error(request,'Something went wrong!')
    return render(request,'user-resource-setting.html')

import datetime

def user_resource_publish_request(request,id):
    resourceObj = model.resource.objects.filter(readerName=model.reader.objects.get(id=request.session.get('userid')),id=id).update(isPublished = True)
    if resourceObj:
        messages.info(request,'Resource is published at '+str(datetime.datetime.now()))
        return redirect(user_resources)
    messages.error(request,'Something went wrong')
    return redirect(user_resources)

def user_resource_unpublish_request(request,id):
    resourceObj = model.resource.objects.filter(readerName=model.reader.objects.get(id=request.session.get('userid')),
                                                id=id).update(isPublished=False)
    if resourceObj:
        messages.info(request, 'Resource is unpublished at ' + str(datetime.datetime.now()))
        return redirect(user_resources)
    messages.error(request, 'Something went wrong')
    return redirect(user_resources)