"""
Views per la gestione dei dati di letspartyapp

Per evitare la manipolazione di informazioni di renderizzazione
viene passato dagli url un path del template da visualizzare
oppure un indirisso per il reindirizzamento
mentre per informazioni relative ad eventuali specializzazioni dei template
si usa un oggetto context passato dall'url in modo che 
la parte dedicata alla visualizzazione sia piu' isolata possibile
dalla manipolazione dei dati.
"""

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from letspartyapp import models
from django.forms.models import modelformset_factory, modelform_factory
from django.forms.formsets import formset_factory
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from LPTools.model_tools import queryset_to_dictset
from django import forms
#from django.forms.formsets import formset_factory
#from LPTools.model_tools import queryset_to_dictset
import datetime

def logged_user():
	adm = models.Login.objects.latest('data_accesso')
	return adm.amministratore

# Contesto per la renderizzazione
@csrf_protect
def login(request, template_path="", ctx={}):
	"""
	simulazione del login, se il metodo viene chiamato direttamente dal link
	vuol dire che e' stato passato post con l'amministratore
	"""
	if request.method == 'POST':
#		adm = models.Login.objects.get(id=request.POST['amministratore'])
		adm = models.Amministratore.objects.get(id=request.POST['amministratore'])
		log = models.Login(amministratore=adm, data_accesso=datetime.datetime.now())
		log.save()
		return redirect('/letsparty/')
	else:
		context = {}
		context['user'] = 'anonym'
		context.update(ctx)
		adm = models.Login.objects.latest('data_accesso')
		context['form'] = models.LoginForm(instance=adm)
		return render(request, template_path, context)

def go_home(request, template_path='letsparty/', ctx={}):
	"""
	Crea il contenuto per la home page
	"""
	context = {}
	context.update(ctx)
	context['user'] = logged_user()
	log = models.Login.objects.latest('data_accesso')
	qset = models.Amministratore.objects.get(id=log.amministratore.id).festa_set.select_related()
	context['formset'] = modelformset_factory(models.Festa, exclude=('inventario', 'partecipazioni'), extra=0)(queryset=qset)
	return render(request, template_path, context )
	
def displayTable(request, table, template_path='letsparty/', ctx={}):
	"""
	Visualizza la tabella richiesta sotto forma di formset
	"""
	# Contesto per la renderizzazione
	context = {}
	context.update(ctx)
	context['user'] = logged_user()
	tname = models.is_model(table)
	if not tname:
		return HttpResponse('errore tabella non trovata')
	tb = getattr(models, tname)
	mf = getattr(models, tname + 'Form')
	formset = formset_factory( mf, extra=0 )
	context['form'] = formset( initial=queryset_to_dictset(tb.objects.all()))
	context.update(csrf(request))
	return render(request, template_path, context)

@csrf_protect
def manage_table(request, table, template_path='letsparty/', ctx={}):
	"""
	Gestione di una tabella sia la visualizzazione che la modifica
	"""
	context = {}
	context['user'] = logged_user()
	tname = models.is_model(table)
	if not tname:
		return HttpResponse('<h1>errore</h1>')
	tb = getattr(models, tname)
	formset = modelformset_factory(tb)
#	return HttpResponse(request.POST)
	if request.method == 'POST':
		filled_formset = formset(request.POST, prefix=tname)
		if filled_formset.is_valid():
			filled_formset.save()
	context.update(ctx)
	context['extra'] = {
					'tname': tname
					}
	context['formset'] = formset(prefix=tname)
	return render(request, template_path, context)

#al momento questo metodo non e' piu necessario in quanto gestito con un sistema
#di reindirizzamenti e gestione delle variabili	
#@csrf_protect
#def manage_admin(request, template_path="", ctx={}):	
#	"""
#	View per la creazione di un nuovo amministratore
#	"""
#	context = {}
#	context.update(ctx)
#	if request.method == 'POST':
#		post = request.POST
#		a = [ [k, v] for k, v in post.items() if k in ['nome', 'cognome', 'telefono', 'email']]
#		a = dict(a)
#		adm = models.Amministratore(**a)
#		adm.save()
#       models.Login(amministratore=adm, data_accesso=datetime.datetime.now()).save()
#		return redirect('/letsparty/')
#	else:
#		context['form'] = models.AmministratoreForm()
##		return HttpResponse(context["form"].as_p())
#		return render(request, 'forms/login.djhtml', context)
@csrf_protect
def create(request, table, template_path='letsparty/', ctx={}):
	"""
	Gestione di una tabella sia la visualizzazione che la modifica
	"""
	context = {}
	context.update(ctx)
	tname = models.is_model(table)
	if not tname:
		return HttpResponse('<h1>errore</h1>')
	model_form = getattr(models, tname+'Form')
#	return HttpResponse(request.POST)
	if request.method == 'POST':
		filled_form = model_form(request.POST)
		if filled_form.is_valid():
			adm = filled_form.save()
			models.Login(amministratore=adm, data_accesso=datetime.datetime.now()).save()
			return redirect('/letsparty/')
	context.update(ctx)
	context['user'] = table == 'amministratore' and 'anonym' or logged_user()
	context['extra'] = {
					'tname': tname
					}
	context['form'] = model_form()
#	return HttpResponse(context['form'])
	return render(request, template_path, context)

@csrf_protect
def link(request, template_path='letsparty/', ctx={}):
	"""
	Gestione per la la visualizzazione e link dei partecipanti e materiali di una festa
	"""
	context = {}
	context.update(ctx)
	context['user'] = logged_user()
	qset = {
		'amministratore': models.Amministratore.objects.all()
		}
	if request.method == 'GET':
		qset['festa'] = models.Amministratore.objects.get(id=request.GET['amministratore']).festa_set.select_related()
		if request.GET.get('festa'):
#			p = models.Partecipante.objects.all().filter(partecipazione_set_select_related_festa_id=request.GET['festa'])
			p = set(models.Festa.objects.get(id=request.GET['festa']).partecipazione_set.select_related())
			qset['partecipazioneOut'] = models.Partecipante.objects.all()
			qset['partecipazioneIn'] = p
	context['querysets'] = qset
	return HttpResponse(context['querysets']['partecipazioneOut'])
	return render(request, template_path, context)
	
	
def bind_m2m(request, table, template_path="", ctx={}):
	context = {}
	context.update(ctx)
	name = models.is_model(table)
	if name:
		model_form = getattr(models, name + "Form")
	else:
		return HttpResponse('error')
	formset = modelformset_factory(models.Festa, form=model_form, extra=0 )
	return render(request, template_path, {'form': formset(queryset=models.Festa.objects.filter(id=1))})

def partecipazioni_test(request):
	rec = models.Festa.objects.get(id=1)
	
#	formset = modelformset_factory(models.Partecipazione, form=models.CheckPartecipazioneForm)
#	return HttpResponse(formset(queryset=models.Festa.objects.get(id=1).partecipazione_set.select_related()).as_p())
	
	