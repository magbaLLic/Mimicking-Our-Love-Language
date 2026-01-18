"""
İstatistik ve Analiz Modülü
Mesajlar hakkında detaylı istatistikler ve analizler sağlar.
"""
from typing import Dict, List, Counter
from collections import Counter
import re

def count_words(text: str) -> int:
    """Metindeki kelime sayısını hesaplar"""
    return len(text.split())

def count_characters(text: str) -> int:
    """Metindeki karakter sayısını hesaplar"""
    return len(text)

def count_emojis(text: str) -> int:
    """Metindeki emoji sayısını hesaplar"""
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    return len(emoji_pattern.findall(text))

def get_message_statistics(messages: List[str]) -> Dict:
    """
    Mesaj listesi için genel istatistikler hesaplar.
    
    Args:
        messages: Mesaj metinlerinin listesi
        
    Returns:
        Dict: İstatistikler
    """
    if not messages:
        return {}
    
    total_messages = len(messages)
    total_words = sum(count_words(msg) for msg in messages)
    total_chars = sum(count_characters(msg) for msg in messages)
    total_emojis = sum(count_emojis(msg) for msg in messages)
    
    avg_words_per_message = total_words / total_messages if total_messages > 0 else 0
    avg_chars_per_message = total_chars / total_messages if total_messages > 0 else 0
    
    # En uzun ve en kısa mesajlar
    if messages:
        longest_msg = max(messages, key=len)
        shortest_msg = min(messages, key=len)
    else:
        longest_msg = ""
        shortest_msg = ""
    
    return {
        'total_messages': total_messages,
        'total_words': total_words,
        'total_characters': total_chars,
        'total_emojis': total_emojis,
        'avg_words_per_message': round(avg_words_per_message, 2),
        'avg_characters_per_message': round(avg_chars_per_message, 2),
        'longest_message': longest_msg[:100] + "..." if len(longest_msg) > 100 else longest_msg,
        'longest_message_length': len(longest_msg),
        'shortest_message': shortest_msg,
        'shortest_message_length': len(shortest_msg)
    }

def get_most_common_words(messages: List[str], top_n: int = 10, min_length: int = 3) -> List[tuple]:
    """
    En sık kullanılan kelimeleri bulur.
    
    Args:
        messages: Mesaj listesi
        top_n: Kaç kelime döndürülecek
        min_length: Minimum kelime uzunluğu
        
    Returns:
        List[tuple]: (kelime, sayı) formatında liste
    """
    # Türkçe stop words (basit bir liste)
    stop_words = {
        'bir', 'bu', 'şu', 'o', 've', 'ile', 'için', 'gibi', 'kadar',
        'de', 'da', 'ki', 'mi', 'mı', 'mu', 'mü', 'var', 'yok',
        'ben', 'sen', 'biz', 'siz', 'onlar', 'benim', 'senin'
    }
    
    all_words = []
    for msg in messages:
        # Kelimeleri ayır ve temizle
        words = re.findall(r'\b\w+\b', msg.lower())
        words = [w for w in words if len(w) >= min_length and w not in stop_words]
        all_words.extend(words)
    
    word_counts = Counter(all_words)
    return word_counts.most_common(top_n)

def get_entity_statistics(messages_with_entities: List[Dict]) -> Dict:
    """
    NER sonuçları için istatistikler hesaplar.
    
    Args:
        messages_with_entities: {'text': str, 'ents': List[Dict]} formatında liste
        
    Returns:
        Dict: Entity istatistikleri
    """
    entity_counts = Counter()
    entity_by_label = {}
    
    for msg in messages_with_entities:
        ents = msg.get('ents', [])
        for ent in ents:
            label = ent.get('entity_group') or ent.get('label') or 'UNKNOWN'
            entity_counts[label] += 1
            
            if label not in entity_by_label:
                entity_by_label[label] = []
            entity_by_label[label].append(ent.get('word', ''))
    
    return {
        'total_entities': sum(entity_counts.values()),
        'entity_counts': dict(entity_counts),
        'entities_by_label': {k: len(v) for k, v in entity_by_label.items()},
        'unique_entities': {k: list(set(v))[:10] for k, v in entity_by_label.items()}  # Her label'dan ilk 10
    }

def compare_authors(messages_dict: Dict[str, List[str]]) -> Dict:
    """
    Farklı yazarların mesajlarını karşılaştırır.
    
    Args:
        messages_dict: {'author_key': [messages]} formatında dict
        
    Returns:
        Dict: Karşılaştırma istatistikleri
    """
    comparison = {}
    
    for author, msgs in messages_dict.items():
        comparison[author] = get_message_statistics(msgs)
    
    return comparison
