"""
Definizione delle classi models per la rappresentazione delle tabelle,
e dei modelForm per la gestione del front-end
"""

from django.db import models
from django import forms

# Lista di tutti i model presenti nel modulo
MODELS_LIST = [ 'Indirizzo',
                'Tipologia',
                'Materiale', 
                'Amministratore', 
                'Partecipante', 
                'Festa', 
                'Partecipazione', 
                'Inventario',
                'Partecipazioni' ]


# i modelli per la gestione del database di letsparty app
class Indirizzo(models.Model):
    """E
    ntita' per la gestione degli indirizzi che saranno utili per il recapito
    dell'utente e la location delle feste
    """
    nome = models.CharField(max_length=150)
    civico = models.CharField(max_length=45)
    cap = models.CharField(max_length=5)
    citta = models.CharField(max_length=45)
    def __unicode__(self):
        """
        toString per la rappresentazioine dell'indirizzo nel formato esempio:
        via Roma 15, Mestre 30174, non verrano rappresentati l'interno e la scala
        """
        return u"%s %s, %s %s" %(self.nome, self.civico, self.cap, self.citta)
    class Meta:
        verbose_name_plural = "Indirizzi"
        unique_together = (('nome', 'civico', 'cap', 'citta'))

class Tipologia(models.Model):
    """
    Entita' per la gestione di tutte le tipologie possibili di una festa
    che identifica una determinata categoria di feste che abbiamo elementi
    in comune tra di loro
    """
    nome = models.CharField(max_length=45, unique=True)
    privata = models.BooleanField(default=True)
    descrizione = models.TextField(max_length=500, null=True, blank=True)
    def __unicode__(self):
        """
        toString per la rappresentazione delle tipologie di festa
        verra visualizzato esclusivamente il nome della tipologia
        """
#        tmp_string = " ".join(self.descrizione.split()[:10])  #splita negli spazi e recupera le prine 50 parole che verrano reincollate
#        if len(self.descrizione.split())>10:
#            tmp_string += " ..."
        return u"%s" %(self.nome)
    class Meta:
        verbose_name_plural = "Tipologie"
        unique_together = (('nome', 'privata', 'descrizione'))
        
class Materiale(models.Model):
    """Entita' per la gestione dei materiali che sono utili per una festa
    la voce quantitaProCapite indica quanto una persona potrebbe consumare
    nel caso di materiali consumabili"""
    nome = models.CharField(max_length=45, unique=True)
    descrizione = models.TextField(max_length=150, null=True)
    quantita_pro_capite= models.DecimalField(max_digits=5, decimal_places=2, null=True)
    def __unicode__(self):
        """toString per la rappresentazione dei materiali necessari per l'organizzazione di 
        una festa rappresentato nel formato
        nome materiale, e se presente descrizione e quantita' pro capite"""
        return u"%s" %(self.nome)
    class Meta:
        verbose_name_plural = "Materiali"
        unique_together = (('nome', 'descrizione', 'quantita_pro_capite'))

class Amministratore(models.Model):
    """Entita' per la gestione dei Partecipanti"""
    nome = models.CharField(max_length=45)
    cognome  = models.CharField(max_length=45)
    email = models.EmailField(max_length=75, unique=True)
    telefono = models.CharField(max_length=10, null=True, blank=True)
    def __unicode__(self):
        """toString"""
        return u"%s %s" %(self.nome, self.cognome)
    class Meta:
        verbose_name_plural = "Amministratori"
        unique_together = (('nome', 'cognome', 'email', 'telefono'))

class Partecipante(models.Model):
    """Entita' per la gestione degli utenti, sia organizzatori che partecipati delle feste"""
    nome = models.CharField(max_length=45)
    cognome  = models.CharField(max_length=45)
    email = models.EmailField(max_length=75)
    def __unicode__(self):
        """toString per la rappresentazione di utente nel formato
        nome, cognome, e-mail"""
        return u"%s %s" %(self.nome, self.cognome)
    class Meta:
        verbose_name_plural = "Partecipanti"
        unique_together = (('nome', 'cognome', 'email'))

class Festa(models.Model):
    """Entita' per la gestione della festa comprensiva di ora inizio, ora fine e se a pagamento
    esempio: 21:00 - 3:00 , a pagamento"""
    nome = models.CharField(max_length=45, default="Party!")
    data = models.DateField()
    ora_inizio = models.TimeField()
    ora_fine = models.TimeField()
    costo = models.DecimalField(max_digits=5, decimal_places=2)
    tipologia = models.ForeignKey(Tipologia)
    location = models.ForeignKey(Indirizzo)
    amministratore = models.ForeignKey(Amministratore)
    inventario = models.ManyToManyField(Materiale, db_table="Inventario")
    partecipazioni = models.ManyToManyField(Partecipante, through="Partecipazione" )
    
    def __unicode__(self):
        """toString"""
        pagamento = ""
        if(self.costo>0):
            pagamento = "A pagamento"
        else:
            pagamento = "Gratis"

        return u"%s (%s: %s - %s, %s)" %(self.nome, self.data, self.ora_inizio, self.ora_fine, pagamento)
    class Meta:
        verbose_name_plural = "Feste"
        unique_together = (('nome', 'data', 'ora_inizio', 'ora_fine', 'costo', 'tipologia', 'location', 'amministratore'))

class Partecipazione(models.Model):
    festa = models.ForeignKey(Festa)
    partecipante = models.ForeignKey(Partecipante)
    partecipa = models.BooleanField(default=False)
    def __unicode__(self):
        """toString per la rappresentazione del legame tra 
        Partecipante e Festa"""
        return u"%s@%s" %(self.partecipante, self.festa)
    class Meta:
        verbose_name_plural = "Partecipazioni"
        unique_together = (('festa', 'partecipante'))
    
class Login(models.Model):
    """Simulazione del sistema di login che verra' migliorato in futuro"""
    from datetime import datetime
    data_accesso = models.DateTimeField(default=datetime.now())
    amministratore = models.ForeignKey(Amministratore)
    
    def __unicode__(self):
        """toString per la rappresentazione del login"""
        return u"%s:%s" %(self.amministratore, self.data_accesso)
    

# ModelForm classi moldto utili per la creazione di form automatici
class IndirizzoForm(forms.ModelForm):
    class Meta:
        model = Indirizzo
        
class TipologiaForm(forms.ModelForm):
    class Meta:
        model = Tipologia
        
class MaterialeForm(forms.ModelForm):
    class Meta:
        model = Materiale
        
class AmministratoreForm(forms.ModelForm):
    class Meta:
        model = Amministratore
        
class PartecipanteForm(forms.ModelForm):
    class Meta:
        model = Partecipante
        
class FestaForm(forms.ModelForm):
    class Meta:
        model = Festa
        exclude = ('inventario', 'partecipazioni')
class PartecipazioneForm(forms.ModelForm):
    class Meta:
        model = Partecipazione

class LoginForm(forms.ModelForm):
    class Meta:
        model = Login
        fields = ('amministratore',)       
class InventarioForm(forms.ModelForm):
    class Meta:
        model = Festa
        fields = ('inventario',)
        widgets = {
                   'inventario': forms.CheckboxSelectMultiple()
                   }
        
class PartecipazioniForm(forms.ModelForm):
    class Meta:
        model = Festa
        fields = ('partecipazioni',)
        widgets = {
                   'partecipazioni': forms.CheckboxSelectMultiple()
                   }
        
# Metodi personalizzati

# verifica se la stringa passata puo essere il nome di un model
def is_model(name):
    name = name.lower().capitalize()
    return name in MODELS_LIST and name or ''
