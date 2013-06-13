"""Raccolta di utilita' e strumenti per la gestone del sito e delle applicazioni"""


def as_dict(rec):
        """Restituisce il recordo preso come se fosse un dict"""
        temp = {}
        for field in rec._meta.fields:
            temp[field.name] = field.value_from_object(rec)
        return temp
    
def queryset_to_dictset(qs):
        """trasforma una queryset in un lista di record in forma dizionario"""
        return [ as_dict(rec) for rec in qs ]
    
