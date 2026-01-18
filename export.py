"""
Veri Dışa Aktarma Modülü
Analiz sonuçlarını farklı formatlarda dışa aktarır.
"""
import json
import csv
from typing import Dict, List, Any
from datetime import datetime

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

def export_to_json(data: Any, filename: str = None) -> str:
    """
    Veriyi JSON formatında dışa aktarır.
    
    Args:
        data: Dışa aktarılacak veri
        filename: Dosya adı (None ise otomatik oluşturulur)
        
    Returns:
        str: Kaydedilen dosya yolu
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"export_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return filename

def export_to_csv(messages: List[Dict], filename: str = None) -> str:
    """
    Mesajları CSV formatında dışa aktarır.
    
    Args:
        messages: Dışa aktarılacak mesaj listesi
        filename: Dosya adı (None ise otomatik oluşturulur)
        
    Returns:
        str: Kaydedilen dosya yolu
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"export_{timestamp}.csv"
    
    if not messages:
        return filename
    
    # CSV için uygun format
    fieldnames = set()
    for msg in messages:
        fieldnames.update(msg.keys())
    fieldnames = list(fieldnames)
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for msg in messages:
            # Nested dict'leri string'e çevir
            row = {}
            for key, value in msg.items():
                if isinstance(value, (dict, list)):
                    row[key] = json.dumps(value, ensure_ascii=False)
                else:
                    row[key] = value
            writer.writerow(row)
    
    return filename

def export_to_excel(messages: List[Dict], filename: str = None, sheet_name: str = "Messages") -> str:
    """
    Mesajları Excel formatında dışa aktarır.
    
    Args:
        messages: Dışa aktarılacak mesaj listesi
        filename: Dosya adı (None ise otomatik oluşturulur)
        sheet_name: Excel sheet adı
        
    Returns:
        str: Kaydedilen dosya yolu
    """
    if not PANDAS_AVAILABLE:
        raise ImportError("pandas ve openpyxl paketleri gerekli. pip install pandas openpyxl")
    
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"export_{timestamp}.xlsx"
    
    # DataFrame oluştur
    df = pd.DataFrame(messages)
    
    # Nested dict/list kolonlarını string'e çevir
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].apply(
                lambda x: json.dumps(x, ensure_ascii=False) if isinstance(x, (dict, list)) else x
            )
    
    df.to_excel(filename, index=False, sheet_name=sheet_name, engine='openpyxl')
    return filename

def export_statistics_to_json(stats: Dict, filename: str = None) -> str:
    """
    İstatistikleri JSON formatında dışa aktarır.
    
    Args:
        stats: İstatistik verisi
        filename: Dosya adı
        
    Returns:
        str: Kaydedilen dosya yolu
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"statistics_{timestamp}.json"
    
    return export_to_json(stats, filename)

def export_entities_to_csv(messages_with_entities: List[Dict], filename: str = None) -> str:
    """
    Entity'leri CSV formatında dışa aktarır.
    
    Args:
        messages_with_entities: Entity içeren mesaj listesi
        filename: Dosya adı
        
    Returns:
        str: Kaydedilen dosya yolu
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"entities_{timestamp}.csv"
    
    # Entity'leri düzleştir
    flattened = []
    for msg in messages_with_entities:
        text = msg.get('text', '')
        ents = msg.get('ents', [])
        
        if not ents:
            flattened.append({
                'text': text,
                'entity': '',
                'label': '',
                'score': ''
            })
        else:
            for ent in ents:
                flattened.append({
                    'text': text,
                    'entity': ent.get('word', ''),
                    'label': ent.get('entity_group', ent.get('label', '')),
                    'score': ent.get('score', '')
                })
    
    return export_to_csv(flattened, filename)
