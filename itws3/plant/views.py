from __future__ import unicode_literals
from .models import Plant
from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
# Create your views here.
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .forms import UserForm


def dashboard(request):
	plantid=1
	if not request.user.is_authenticated():
		return render(request, 'plant/login.html', {'error_message': 'Login Required'})
	else:
		humSet=[]
		temSet=[]
		plant=Plant.objects.get(pk=int(plantid))
		mstate=plant.motorstate
		mode=plant.automode
		if (mode=='True'):
			ircondition='auto mode'
		else:
			if(mstate=='True'):
				ircondition='manual and motor on'
			else:
				ircondition='manual and motor off'
		datastring=str(plant.sensors_set.all()[len(plant.sensors_set.all())-1])
		d=datastring.split(",")
		all_plants=Plant.objects.all()
		for i in range(1,12):
			temp = str(plant.sensors_set.all()[len(plant.sensors_set.all())-i])
			temp = temp.split(',')
			temSet.append(int(temp[0]))
			humSet.append(int(temp[1]))
		context={'tem':d[0],'hum':d[1],'soil':d[2],'water':d[3],'time':d[4],'rain':d[5],'id':plantid,'all_plants':all_plants,'temValues':temSet,'humValues':humSet,'ms':ircondition}
		return render(request,'plant/dashboard.html',context)


def newdashboard(request,plantid):
	if not request.user.is_authenticated():
		return render(request, 'plant/login.html', {'error_message': 'Login Required'})
	else:
		plant=Plant.objects.get(pk=int(plantid))
		plant1=Plant.objects.get(pk=int(1))
		mstate=plant1.motorstate
		mode=plant1.automode
		if (bool(mode)):
			ircondition='auto mode'
		else:
			if(bool(mstate)):
				ircondition='manual and motor on'
			else:
				ircondition='manual and motor off'
		try:
			datastring=str(plant.sensors_set.all()[len(plant.sensors_set.all())-1])
			d=datastring.split(",")
			all_plants=Plant.objects.all()
			humSet=[]
			temSet=[]
			for i in range(1,12):
				temp = str(plant.sensors_set.all()[len(plant.sensors_set.all())-i])
				temp = temp.split(',')
				temSet.append(int(temp[0]))
				humSet.append(int(temp[1]))
			context={'tem':d[0],'hum':d[1],'soil':d[2],'water':d[3],'time':d[4],'rain':d[5],'id':plantid,'all_plants':all_plants,'temValues':temSet,'humValues':humSet,'ms':ircondition}
			return render(request,'plant/dashboard.html',context)
		except:
			all_plants=Plant.objects.all()
			context={'tem':'no data','hum':'no data','soil':'no data','water':'no data','time':'no data','rain':'no data','id':plantid,'all_plants':all_plants,'ms':ircondition}
			return render(request,'plant/dashboard.html',context)

def home(request):
	if not request.user.is_authenticated():
		return render(request, 'plant/home.html', {'error_message': 'Login Required'})
	else:
		return dashboard(request)
	
def getdata(request):
	if request.method=='GET' :
		pid=request.GET['pid']
		tem=request.GET['plant']
		hum = request.GET['humidity']
		time = request.GET['time']
		soilm = request.GET['soil']
		wlvl = request.GET['water']
		rn  = request.GET['rain']
		plant=Plant.objects.get(pk=int(pid))
		plant.sensors_set.create(tem_value=str(tem),hum_value=str(hum),soil_mois=str(soilm),wat_lvl=str(wlvl),time=str(time),rain=str(rn))
		plant=Plant.objects.get(pk=int(1))
	        string=plant.motorstate + "," + plant.automode
	        return HttpResponse(string)
def actuatorcontrol(request):
	if request.method=='GET' :
		ms=request.GET['motorstate']
		ms=str(ms)
		am=request.GET['automode']
		am=str(am)
		plant=Plant.objects.get(pk=1)
		plant.automode=am
		plant.motorstate=ms
		plant.save()
		return redirect('/dashboard/')
def motorstatecheckbypi(request):
	plant=Plant.objects.get(pk=int(1))
	string=plant.motorstate + "," + plant.automode
	return HttpResponse(string)
def add(request):
	return render(request,'plant/addPlant.html');
def addPlant(request):
	#pass;
	if(request.method=="POST"):
		x = len(Plant.objects.all());
		lat = request.POST['lat'];
		lon = request.POST['long'];
		plant = Plant(plantid=str(x+1),longitude = str(lon) , latitude = str(lat));
		plant.save();
		return redirect('/dashboard/')

	
def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'plant/login.html',  {'error_message': 'User logged out sucessfully'})

def login_user(request):
	if not request.user.is_authenticated():
	    if request.method == "POST":
	        username = request.POST['username']
	        password = request.POST['password']
	        user = authenticate(username=username, password=password)
	        if user is not None:
	            if user.is_active:
	                login(request, user)
	                #albums = Album.objects.filter(user=request.user)
	                return dashboard(request)#render(request, 'plant/dashboard.html', {'albums': 1})
			#return HttpResponse('finally success is waiting foryou')
	            else:
	                return render(request, 'plant/login.html', {'error_message': 'Your account has been disabled'})
	        else:
	            return render(request, 'plant/login.html', {'error_message': 'Invalid login'})
	    return render(request, 'plant/login.html')
	else:
	    return dashboard(request)
def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
		
                return dashboard(request)#1
    context = {
        "form": form,
    }
    return render(request, 'plant/register.html', context)

def map(request):
	plantid=1
	if not request.user.is_authenticated():
		return render(request, 'plant/login.html', {'error_message': 'Login Required'})
	else:
		plant=Plant.objects.get(pk=int(plantid))
		datastring=str(plant.sensors_set.all()[len(plant.sensors_set.all())-1])
		d=datastring.split(",")
		lat=plant.latitude
		lon=plant.longitude
		context={'tem':d[0],'hum':d[1],'soil':d[2],'water':d[3],'time':d[4],'rain':d[5],'lat':lat,'lon':lon}
		return render(request,'plant/map.html',context)

def newmap(request,plantid):
	if not request.user.is_authenticated():
		return render(request, 'plant/login.html', {'error_message': 'Login Required'})
	else:
		plant=Plant.objects.get(pk=int(plantid))
		lat=plant.latitude
		lon=plant.longitude
		try:
			datastring=str(plant.sensors_set.all()[len(plant.sensors_set.all())-1])
			d=datastring.split(",")
			context={'tem':d[0],'hum':d[1],'soil':d[2],'water':d[3],'time':d[4],'rain':d[5],'lat':lat,'lon':lon}
		except:
			context={'tem':10,'hum':10,'soil':10,'water':10,'rain':1,'lat':lat,'lon':lon}
		return render(request,'plant/map.html',context)

