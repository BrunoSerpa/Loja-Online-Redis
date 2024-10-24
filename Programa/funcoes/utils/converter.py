from bson.objectid import ObjectId
from datetime import datetime

def ObjetoParaJson(objeto):
    if isinstance(objeto, ObjectId): return str(objeto)
    elif isinstance(objeto, datetime): return objeto.isoformat()
    else: raise TypeError(f"Objeto do tipo {type(objeto)} não é serializável.")

def JsonParaObjeto(dicionario):
    for chave, valor in dicionario.items():
        if isinstance(valor, str):
            try: dicionario[chave] = datetime.fromisoformat(valor)
            except ValueError: pass
    return dicionario