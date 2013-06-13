from django.forms import *
from django.forms.widgets import *
from letspartyapp.models import *
from LPTools.model_tools import *


def showattr(obj):
    """Visualizza la lista degli oggetti"""
    for attr in dir(obj):
        if not attr.startswith('__'):
            print attr

def printMF(mf):
    """Stampa il model forma passato"""
    from django.forms import ModelForm
    if isinstance( mf, ModelForm):
        print mf.as_p()
    else:
        print mf().as_p()
    return

def new_drec(m, i = 1):
    """Metodo per la creazione di un dict per il riempimento di un model"""
    from django.db.models import Model
    if not isinstance( m, Model):
        m = m()
    from copy import copy
    name = m._meta.module_name
    tmp = as_dict(m())
    del tmp['id']
    new = []
    for n in range(i):
        print "inserimento", name, n
        r = copy(tmp)
        for f in tmp.keys():
            r[f] = raw_input('inserisci un valore per %s il << %s >>: ' %(name, f))
        new.append(r)
    return new