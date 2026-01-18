import re
import hashlib
from typing import Dict, List
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

MODEL_NAME = "akdeniz27/bert-base-turkish-cased-ner"

_tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME) #tokenizer yükleme
_model = AutoModelForTokenClassification.from_pretrained(MODEL_NAME) #model yükleme

_ner = pipeline("ner", model=_model, tokenizer=_tokenizer, aggregation_strategy="simple")

TR_SUFFIX_RE = re.compile(r"^'[\wçğıöşüÇĞİÖŞÜ]+") # Türkçe ekleri ayırmak için regex

def apply_ner(text: str) -> List[Dict]: # metin üzerinde NER uygulama
    return _ner(text)

def norm_ent(e): # normalize entity dictionary -> Dict: 
    label = e.get('entity_group', e.get('entity')) or e.get('label')
    value = e['word'] or e.get('value') or e.get('text') or ""
    score = e.get('score', 1.0)
    start = e.get('start', -1)
    end = e.get('end', -1)
    return {
        'label': label,
        'value': value,
        'score': score,
        'start': start,
        'end': end
    }

def filter_messages(messages, label=None, query=None, min_score=0.6): # filtreleme fonksiyonu
    """
    label: "PER", "LOC", "ORG" gibi
    query: value içinde geçen substring ("ankara", "ahmet")
    """
    out = []
    q = query.lower() if isinstance(query, str) else None

    for m in messages: # her mesaj için
        ents = m.get("ents") or []
        ok = False
        for e in ents: # her entity için
            ne = norm_ent(e)
            if ne["label"] is None or ne["score"] < min_score:
                continue
            if label and ne["label"] != label:
                continue
            if q and q not in (ne["value"] or "").lower():
                continue
            ok = True
            break
        if ok:
            out.append(m)

    return out
    
