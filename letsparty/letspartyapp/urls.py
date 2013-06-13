"""
Urls per la gestione di tutti gli indirizzamenti delle richieste di letspartyapp

questo fale conterra tutte le informazioni necessarie per rendere i
template molto dinamici in modo che pochi template riescano a coprire
tutta l'applicazione.
Per la gestione della specializzazione dei nomi dei campi verra passato un oggetto
ctx che sara' mandato al template per creare il contesto di renderizzazione.
l'oggetto ctx sara' diviso in varie sezioni, le principali sono 
--header: contenenti le informazioni dell'header html
--body: contente informazioni relative al body html
questi sono 2 dict che cercano di simulare il dom html per rendere
l'accesso alle variabili in modo piu' naturale.

"""

from django.conf.urls.defaults import *
from letspartyapp.views import *

urlpatterns = patterns('',
	# url per il test
# 	url(r'^test/$', inventario_test, {
# 									'template_path': "test/test.djhtml",
# 									'table': "partecipazioni"
# 									}),
	
	# radice di lets party app, indirizza verso la homepage
	url(r'^$', go_home, { 
						"template_path": "structure/main.djhtml",
						"ctx": { 
							'header': { 
									"title": "modifica della tabella" },
								    "body": {
										"mainTitle": "titolo principale",
										"form": { 
												"button_value": "next >>>" 
												} 
											} 
							     } 
						} 
	),
					
	# 
	url(r'^formset/(?P<table>\w+)/$', manage_table, {
												'template_path': 'forms/generic-formset.djhtml',
												"ctx": {
													'header': {
															"title": "modifica della tabella"
															},
													"body": {
															"mainTitle": "titolo principale",
															"form": {
																"button_value": "next >>>"
																}
															}
														}
													}
		),
	
	# indirizzamento per il log in
	url(r'^login/$', login, {
							'template_path': 'forms/generic-create.djhtml',
							"ctx": {
								'header': {
										"title": "login"
										},
								"body": {
										"mainTitle": "simulazione di login",
										"form": {
												"button_value": "login"
												}
										}
									}
							}
	),
	
	# test per i login durante la fase di progettazione
	url(r'^logintest/$', login),
	
	# creazione di un nuovo amministratore per gli eventi
	url(r'^admin/$', create, {
								'template_path': 'forms/generic-create.djhtml',
								'table': "amministratore",
								"ctx": {
									'header': {
											"title": "crea amministratore"
											},
									"body": {
											"mainTitle": "Creazione di un utente amministratore",
											"form": {
												"button_value": "salva"
												}
										}
									}
								}
	),
					
	# creazione di nuovo evento
	url(r'^event/create/$', create, {
							"template_path": 'forms/generic-create.djhtml',
							'table': 'festa',
							"ctx": {
								"header": {
										'title': 'creazione evento'
										},
								'body': {
										'mainTitle': "Creazione di un evento",
										'form': {
												'action': "/letsparty/fill-inventario/",
												'button_value': "avanti"
												}
										}
								}
							}
	),
					
	url(r'^fill-inventario/$', bind_m2m, {
									'template_path': "test/test.djhtml",
									'table': "inventario",
									'ctx': {
										'header': {},
										'body': {}
										}
									}
	),
					
	url(r'^fill-partecipazioni/$', bind_m2m, {
									'template_path': "test/test.djhtml",
									'table': "partecipazioni",
									'ctx': {
										'header': {},
										'body': {}
										}
									}
	),
)