"""
Duygu Analizi (Sentiment Analysis) Modülü
Türkçe metinler için duygu analizi yapar.
"""
from transformers import pipeline
from typing import Dict, List, Optional

# Türkçe sentiment analysis modeli
_sentiment_analyzer = None

def get_sentiment_analyzer():
    """Sentiment analyzer'ı lazy load et"""
    global _sentiment_analyzer
    if _sentiment_analyzer is None:
        # Türkçe için uygun bir model kullanılabilir
        # Alternatif: "savasy/bert-base-turkish-sentiment-cased"
        try:
            _sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model="savasy/bert-base-turkish-sentiment-cased"
            )
        except:
            # Fallback: Genel bir model
            _sentiment_analyzer = pipeline("sentiment-analysis")
    return _sentiment_analyzer

def analyze_sentiment(text: str) -> Dict:
    """
    Tek bir metin için duygu analizi yapar.
    
    Args:
        text: Analiz edilecek metin
        
    Returns:
        Dict: {'label': 'POSITIVE'/'NEGATIVE', 'score': float}
    """
    analyzer = get_sentiment_analyzer()
    result = analyzer(text)[0]
    return {
        'label': result['label'],
        'score': result['score']
    }

def analyze_sentiments(texts: List[str]) -> List[Dict]:
    """
    Birden fazla metin için duygu analizi yapar.
    
    Args:
        texts: Analiz edilecek metin listesi
        
    Returns:
        List[Dict]: Her metin için duygu analizi sonucu
    """
    analyzer = get_sentiment_analyzer()
    results = analyzer(texts)
    return [
        {'label': r['label'], 'score': r['score']}
        for r in results
    ]

def get_sentiment_statistics(messages: List[Dict]) -> Dict:
    """
    Mesajlar için duygu istatistikleri hesaplar.
    
    Args:
        messages: {'text': str, 'sentiment': Dict} formatında mesaj listesi
        
    Returns:
        Dict: Duygu istatistikleri
    """
    if not messages:
        return {}
    
    positive_count = sum(1 for m in messages 
                        if m.get('sentiment', {}).get('label') == 'POSITIVE')
    negative_count = sum(1 for m in messages 
                        if m.get('sentiment', {}).get('label') == 'NEGATIVE')
    
    total = len(messages)
    avg_positive_score = sum(m.get('sentiment', {}).get('score', 0) 
                            for m in messages 
                            if m.get('sentiment', {}).get('label') == 'POSITIVE') / max(positive_count, 1)
    avg_negative_score = sum(m.get('sentiment', {}).get('score', 0) 
                            for m in messages 
                            if m.get('sentiment', {}).get('label') == 'NEGATIVE') / max(negative_count, 1)
    
    return {
        'total_messages': total,
        'positive_count': positive_count,
        'negative_count': negative_count,
        'positive_percentage': (positive_count / total * 100) if total > 0 else 0,
        'negative_percentage': (negative_count / total * 100) if total > 0 else 0,
        'avg_positive_score': avg_positive_score,
        'avg_negative_score': avg_negative_score
    }
