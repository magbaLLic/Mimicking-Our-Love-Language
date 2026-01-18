"""
Mimicking Our Love Language - Ana Program
Mesaj analizi, NER, duygu analizi ve istatistikler için kapsamlı bir araç.
"""
import os
import sys
from parser import read_data, sanitize_messages
from NER import apply_ner, filter_messages
from sentiment import analyze_sentiment, analyze_sentiments, get_sentiment_statistics
from statistics import get_message_statistics, get_entity_statistics, get_most_common_words, compare_authors
from export import export_to_json, export_to_csv, export_to_excel, export_statistics_to_json
from visualization import plot_entity_distribution, plot_sentiment_distribution, plot_message_length_distribution
from config import load_config

def main():
    """Ana program fonksiyonu"""
    try:
        # Yapılandırmayı yükle
        config = load_config()
        
        # Veri dosyası yolunu al
        default_path = "C:\\Users\\cagin\\Desktop\\New folder\\data.txt"
        dir = input(f"Lütfen veri dosyasının konumunu giriniz (varsayılan: {default_path}): ").strip()
        if not dir:
            dir = default_path
        
        # Dosya kontrolü
        if not os.path.exists(dir):
            print(f"Hata: Dosya bulunamadı: {dir}")
            return
        
        print("Veri okunuyor...")
        messages, author = read_data(loc=dir)
        
        if not messages or not any(messages.values()):
            print("Hata: Mesaj bulunamadı!")
            return
        
        print("Mesajlar temizleniyor...")
        sanitized_messages = sanitize_messages(messages)
        
        # Analiz seçenekleri
        print("\n=== Analiz Seçenekleri ===")
        print("1. NER Analizi")
        print("2. Duygu Analizi")
        print("3. İstatistikler")
        print("4. Tüm Analizler")
        print("5. Sadece NER (Eski versiyon)")
        
        choice = input("\nSeçiminiz (1-5): ").strip()
        
        if choice == "1" or choice == "4":
            print("\nNER analizi yapılıyor...")
            analyze_ner(sanitized_messages, config)
        
        if choice == "2" or choice == "4":
            print("\nDuygu analizi yapılıyor...")
            analyze_sentiments_module(sanitized_messages)
        
        if choice == "3" or choice == "4":
            print("\nİstatistikler hesaplanıyor...")
            show_statistics(sanitized_messages)
        
        if choice == "5":
            # Eski versiyon
            filter_message = []
            for text in sanitized_messages.get("i", []):
                ents = apply_ner(text)
                filter_message.append({"text": text, "ents": ents})
            
            ankara = filter_messages(filter_message, label="LOC", query="ankara", min_score=0.7)
            print(f"\nAnkara ile ilgili mesajlar: {len(ankara)}")
            for msg in ankara[:5]:  # İlk 5 mesajı göster
                print(f"- {msg['text'][:100]}...")
    
    except KeyboardInterrupt:
        print("\n\nProgram kullanıcı tarafından durduruldu.")
    except Exception as e:
        print(f"\nHata oluştu: {e}")
        import traceback
        traceback.print_exc()

def analyze_ner(messages_dict, config):
    """NER analizi yapar"""
    ner_config = config.get("ner", {})
    min_score = ner_config.get("min_score", 0.6)
    
    all_messages_with_entities = []
    
    for author_key, msgs in messages_dict.items():
        print(f"  {author_key} için NER uygulanıyor...")
        author_messages = []
        for text in msgs:
            try:
                ents = apply_ner(text)
                author_messages.append({"text": text, "ents": ents, "author": author_key})
            except Exception as e:
                print(f"    Uyarı: Mesaj işlenirken hata: {e}")
        
        all_messages_with_entities.extend(author_messages)
        
        # Entity istatistikleri
        entity_stats = get_entity_statistics(author_messages)
        print(f"  {author_key} için bulunan entity'ler:")
        for label, count in entity_stats.get("entity_counts", {}).items():
            print(f"    {label}: {count}")
    
    # Görselleştirme
    if all_messages_with_entities:
        try:
            plot_entity_distribution(all_messages_with_entities, "entity_distribution.png")
        except Exception as e:
            print(f"  Görselleştirme hatası: {e}")
    
    # Filtreleme örneği
    print("\n  Örnek filtreleme (LOC, min_score=0.7):")
    filtered = filter_messages(all_messages_with_entities, label="LOC", min_score=min_score)
    print(f"  Bulunan mesaj sayısı: {len(filtered)}")
    
    return all_messages_with_entities

def analyze_sentiments_module(messages_dict):
    """Duygu analizi yapar"""
    all_messages_with_sentiment = []
    
    for author_key, msgs in messages_dict.items():
        print(f"  {author_key} için duygu analizi yapılıyor...")
        author_messages = []
        
        # Batch processing için
        batch_size = 10
        for i in range(0, len(msgs), batch_size):
            batch = msgs[i:i+batch_size]
            try:
                sentiments = analyze_sentiments(batch)
                for text, sentiment in zip(batch, sentiments):
                    author_messages.append({
                        "text": text,
                        "sentiment": sentiment,
                        "author": author_key
                    })
            except Exception as e:
                print(f"    Uyarı: Duygu analizi hatası: {e}")
                # Fallback: tek tek analiz
                for text in batch:
                    try:
                        sentiment = analyze_sentiment(text)
                        author_messages.append({
                            "text": text,
                            "sentiment": sentiment,
                            "author": author_key
                        })
                    except:
                        pass
        
        all_messages_with_sentiment.extend(author_messages)
        
        # İstatistikler
        stats = get_sentiment_statistics(author_messages)
        print(f"  {author_key} duygu istatistikleri:")
        print(f"    Pozitif: {stats.get('positive_count', 0)} ({stats.get('positive_percentage', 0):.1f}%)")
        print(f"    Negatif: {stats.get('negative_count', 0)} ({stats.get('negative_percentage', 0):.1f}%)")
    
    # Görselleştirme
    if all_messages_with_sentiment:
        try:
            plot_sentiment_distribution(all_messages_with_sentiment, "sentiment_distribution.png")
        except Exception as e:
            print(f"  Görselleştirme hatası: {e}")
    
    return all_messages_with_sentiment

def show_statistics(messages_dict):
    """İstatistikleri gösterir"""
    print("\n=== Genel İstatistikler ===")
    
    for author_key, msgs in messages_dict.items():
        print(f"\n{author_key}:")
        stats = get_message_statistics(msgs)
        print(f"  Toplam mesaj: {stats.get('total_messages', 0)}")
        print(f"  Toplam kelime: {stats.get('total_words', 0)}")
        print(f"  Ortalama kelime/mesaj: {stats.get('avg_words_per_message', 0):.1f}")
        print(f"  Toplam emoji: {stats.get('total_emojis', 0)}")
        
        # En sık kullanılan kelimeler
        common_words = get_most_common_words(msgs, top_n=5)
        if common_words:
            print(f"  En sık kullanılan kelimeler:")
            for word, count in common_words:
                print(f"    {word}: {count}")
    
    # Karşılaştırma
    comparison = compare_authors(messages_dict)
    print("\n=== Yazarlar Arası Karşılaştırma ===")
    for author, stats in comparison.items():
        print(f"{author}: {stats.get('total_messages', 0)} mesaj, "
              f"ortalama {stats.get('avg_words_per_message', 0):.1f} kelime/mesaj")
    
    # Görselleştirme
    try:
        plot_message_length_distribution(
            messages_dict.get("i", []) + messages_dict.get("ç", []),
            "message_length_distribution.png"
        )
    except Exception as e:
        print(f"  Görselleştirme hatası: {e}")

if __name__ == "__main__":
    main()