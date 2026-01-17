"""
Yapılandırma Modülü
Proje ayarlarını yönetir.
"""
import json
import os
from typing import Dict, Any

DEFAULT_CONFIG = {
    "ner": {
        "model_name": "akdeniz27/bert-base-turkish-cased-ner",
        "min_score": 0.6,
        "aggregation_strategy": "simple"
    },
    "sentiment": {
        "model_name": "savasy/bert-base-turkish-sentiment-cased"
    },
    "pii": {
        "mask_iban": True,
        "mask_media": True,
        "mask_emails": False,
        "mask_phone_numbers": False
    },
    "export": {
        "default_format": "json",
        "output_directory": "exports"
    },
    "visualization": {
        "figure_size": [10, 6],
        "dpi": 300,
        "style": "whitegrid"
    }
}

_config = None

def load_config(config_path: str = "config.json") -> Dict[str, Any]:
    """
    Yapılandırma dosyasını yükler.
    
    Args:
        config_path: Yapılandırma dosyası yolu
        
    Returns:
        Dict: Yapılandırma verisi
    """
    global _config
    
    if _config is not None:
        return _config
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                _config = json.load(f)
            # Varsayılan değerlerle birleştir
            _config = merge_config(DEFAULT_CONFIG, _config)
        except Exception as e:
            print(f"Yapılandırma dosyası yüklenirken hata: {e}")
            _config = DEFAULT_CONFIG.copy()
    else:
        _config = DEFAULT_CONFIG.copy()
        # Varsayılan yapılandırmayı kaydet
        save_config(_config, config_path)
    
    return _config

def save_config(config: Dict[str, Any], config_path: str = "config.json"):
    """
    Yapılandırmayı dosyaya kaydeder.
    
    Args:
        config: Kaydedilecek yapılandırma
        config_path: Yapılandırma dosyası yolu
    """
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Yapılandırma kaydedilirken hata: {e}")

def merge_config(default: Dict, user: Dict) -> Dict:
    """
    Varsayılan ve kullanıcı yapılandırmasını birleştirir.
    
    Args:
        default: Varsayılan yapılandırma
        user: Kullanıcı yapılandırması
        
    Returns:
        Dict: Birleştirilmiş yapılandırma
    """
    result = default.copy()
    for key, value in user.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_config(result[key], value)
        else:
            result[key] = value
    return result

def get_config() -> Dict[str, Any]:
    """Mevcut yapılandırmayı döndürür"""
    return load_config()

def get_ner_config() -> Dict:
    """NER yapılandırmasını döndürür"""
    return get_config().get("ner", {})

def get_sentiment_config() -> Dict:
    """Sentiment yapılandırmasını döndürür"""
    return get_config().get("sentiment", {})

def get_pii_config() -> Dict:
    """PII yapılandırmasını döndürür"""
    return get_config().get("pii", {})

def get_export_config() -> Dict:
    """Export yapılandırmasını döndürür"""
    return get_config().get("export", {})
