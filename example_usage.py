"""
Kullanım Örnekleri
Projenin farklı özelliklerini gösteren örnekler.
"""
from parser import read_data, sanitize_messages
from NER import apply_ner, filter_messages
from sentiment import analyze_sentiment, get_sentiment_statistics
from analysis_statistics import get_message_statistics, get_most_common_words, get_entity_statistics
from export import export_to_json, export_to_csv
from visualization import plot_entity_distribution, plot_sentiment_distribution
from utility import clean_text

def example_ner_analysis():
    """NER analizi örneği"""
    print("=== NER Analizi Örneği ===")
    
    # Örnek metinler
    texts = [
        "Ankara'da güzel bir gün geçirdim.",
        "Ahmet ile İstanbul'da buluştuk.",
        "Türk Telekom'da çalışıyorum."
    ]
    
    for text in texts:
        entities = apply_ner(text)
        print(f"\nMetin: {text}")
        print(f"Bulunan Entity'ler:")
        for ent in entities:
            print(f"  - {ent.get('word')}: {ent.get('entity_group')} (score: {ent.get('score', 0):.2f})")

def example_sentiment_analysis():
    """Duygu analizi örneği"""
    print("\n=== Duygu Analizi Örneği ===")
    
    texts = [
        "Bu harika bir gün!",
        "Çok üzgünüm.",
        "Her şey yolunda gidiyor."
    ]
    
    for text in texts:
        result = analyze_sentiment(text)
        print(f"\nMetin: {text}")
        print(f"Duygu: {result['label']} (score: {result['score']:.2f})")

def example_statistics():
    """İstatistik örneği"""
    print("\n=== İstatistik Örneği ===")
    
    messages = [
        "Merhaba! Nasılsın?",
        "Bugün çok güzel bir gün geçirdim.",
        "Yarın Ankara'ya gidiyorum.",
        "Seni çok seviyorum ❤️"
    ]
    
    stats = get_message_statistics(messages)
    print(f"Toplam mesaj: {stats['total_messages']}")
    print(f"Toplam kelime: {stats['total_words']}")
    print(f"Ortalama kelime/mesaj: {stats['avg_words_per_message']:.1f}")
    print(f"Toplam emoji: {stats['total_emojis']}")
    
    common_words = get_most_common_words(messages, top_n=5)
    print(f"\nEn sık kullanılan kelimeler:")
    for word, count in common_words:
        print(f"  {word}: {count}")

def example_pii_masking():
    """PII maskeleme örneği"""
    print("\n=== PII Maskeleme Örneği ===")
    
    text = "IBAN: TR330006100519786457841326, Email: test@example.com, Tel: 555-123-4567"
    print(f"Orijinal: {text}")
    
    cleaned = clean_text(text, mask_emails=True, mask_phones=True)
    print(f"Temizlenmiş: {cleaned}")

def example_filtering():
    """Filtreleme örneği"""
    print("\n=== Filtreleme Örneği ===")
    
    # Örnek mesajlar ve entity'leri
    messages = [
        {"text": "Ankara'da güzel bir gün.", "ents": apply_ner("Ankara'da güzel bir gün.")},
        {"text": "İstanbul çok güzel.", "ents": apply_ner("İstanbul çok güzel.")},
        {"text": "Bugün hava güzel.", "ents": apply_ner("Bugün hava güzel.")}
    ]
    
    # Sadece LOC entity'lerini filtrele
    location_messages = filter_messages(messages, label="LOC", min_score=0.6)
    print(f"Lokasyon içeren mesaj sayısı: {len(location_messages)}")
    for msg in location_messages:
        print(f"  - {msg['text']}")

if __name__ == "__main__":
    print("Mimicking Our Love Language - Kullanım Örnekleri\n")
    
    try:
        example_ner_analysis()
        example_sentiment_analysis()
        example_statistics()
        example_pii_masking()
        example_filtering()
        
        print("\n✅ Tüm örnekler başarıyla çalıştırıldı!")
    except Exception as e:
        print(f"\n❌ Hata: {e}")
        import traceback
        traceback.print_exc()
