"""
Görselleştirme Modülü
Analiz sonuçlarını görsel olarak sunar.
"""
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List
from collections import Counter

# Türkçe karakter desteği için
plt.rcParams['font.family'] = 'DejaVu Sans'
sns.set_style("whitegrid")

def plot_entity_distribution(messages_with_entities: List[Dict], save_path: str = None):
    """
    Entity dağılımını görselleştirir.
    
    Args:
        messages_with_entities: Entity içeren mesaj listesi
        save_path: Kaydedilecek dosya yolu (None ise gösterir)
    """
    entity_counts = Counter()
    
    for msg in messages_with_entities:
        ents = msg.get('ents', [])
        for ent in ents:
            label = ent.get('entity_group') or ent.get('label') or 'UNKNOWN'
            entity_counts[label] += 1
    
    if not entity_counts:
        print("Görselleştirilecek entity bulunamadı.")
        return
    
    labels = list(entity_counts.keys())
    counts = list(entity_counts.values())
    
    plt.figure(figsize=(10, 6))
    plt.bar(labels, counts, color='skyblue', edgecolor='navy', alpha=0.7)
    plt.xlabel('Entity Tipi', fontsize=12)
    plt.ylabel('Sayı', fontsize=12)
    plt.title('Entity Dağılımı', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Grafik kaydedildi: {save_path}")
    else:
        plt.show()
    
    plt.close()

def plot_sentiment_distribution(messages_with_sentiment: List[Dict], save_path: str = None):
    """
    Duygu dağılımını görselleştirir.
    
    Args:
        messages_with_sentiment: Duygu analizi içeren mesaj listesi
        save_path: Kaydedilecek dosya yolu
    """
    sentiment_counts = Counter()
    
    for msg in messages_with_sentiment:
        sentiment = msg.get('sentiment', {})
        label = sentiment.get('label', 'UNKNOWN')
        sentiment_counts[label] += 1
    
    if not sentiment_counts:
        print("Görselleştirilecek duygu verisi bulunamadı.")
        return
    
    labels = list(sentiment_counts.keys())
    counts = list(sentiment_counts.values())
    colors = ['#4CAF50' if 'POSITIVE' in label.upper() else '#F44336' if 'NEGATIVE' in label.upper() else '#FFC107' 
              for label in labels]
    
    plt.figure(figsize=(8, 6))
    plt.pie(counts, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    plt.title('Duygu Dağılımı', fontsize=14, fontweight='bold')
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Grafik kaydedildi: {save_path}")
    else:
        plt.show()
    
    plt.close()

def plot_message_length_distribution(messages: List[str], save_path: str = None):
    """
    Mesaj uzunluk dağılımını görselleştirir.
    
    Args:
        messages: Mesaj listesi
        save_path: Kaydedilecek dosya yolu
    """
    lengths = [len(msg.split()) for msg in messages]
    
    if not lengths:
        print("Görselleştirilecek mesaj bulunamadı.")
        return
    
    plt.figure(figsize=(10, 6))
    plt.hist(lengths, bins=30, color='steelblue', edgecolor='black', alpha=0.7)
    plt.xlabel('Mesaj Uzunluğu (Kelime Sayısı)', fontsize=12)
    plt.ylabel('Frekans', fontsize=12)
    plt.title('Mesaj Uzunluk Dağılımı', fontsize=14, fontweight='bold')
    plt.axvline(sum(lengths)/len(lengths), color='red', linestyle='--', 
                label=f'Ortalama: {sum(lengths)/len(lengths):.1f}')
    plt.legend()
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Grafik kaydedildi: {save_path}")
    else:
        plt.show()
    
    plt.close()

def plot_author_comparison(comparison_stats: Dict, save_path: str = None):
    """
    Yazarlar arası karşılaştırmayı görselleştirir.
    
    Args:
        comparison_stats: compare_authors() fonksiyonunun çıktısı
        save_path: Kaydedilecek dosya yolu
    """
    if not comparison_stats:
        print("Karşılaştırılacak veri bulunamadı.")
        return
    
    authors = list(comparison_stats.keys())
    metrics = ['total_messages', 'avg_words_per_message', 'avg_characters_per_message']
    
    fig, axes = plt.subplots(1, len(metrics), figsize=(15, 5))
    
    for idx, metric in enumerate(metrics):
        values = [comparison_stats[author].get(metric, 0) for author in authors]
        axes[idx].bar(authors, values, color=['#FF6B6B', '#4ECDC4', '#95E1D3'][:len(authors)], alpha=0.7)
        axes[idx].set_title(metric.replace('_', ' ').title(), fontweight='bold')
        axes[idx].set_ylabel('Değer')
        axes[idx].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Grafik kaydedildi: {save_path}")
    else:
        plt.show()
    
    plt.close()

def plot_word_frequency(word_counts: List[tuple], top_n: int = 20, save_path: str = None):
    """
    En sık kullanılan kelimeleri görselleştirir.
    
    Args:
        word_counts: (kelime, sayı) formatında tuple listesi
        top_n: Gösterilecek kelime sayısı
        save_path: Kaydedilecek dosya yolu
    """
    if not word_counts:
        print("Görselleştirilecek kelime bulunamadı.")
        return
    
    top_words = word_counts[:top_n]
    words = [w[0] for w in top_words]
    counts = [w[1] for w in top_words]
    
    plt.figure(figsize=(12, 8))
    plt.barh(words, counts, color='coral', edgecolor='darkred', alpha=0.7)
    plt.xlabel('Kullanım Sayısı', fontsize=12)
    plt.ylabel('Kelimeler', fontsize=12)
    plt.title(f'En Sık Kullanılan {top_n} Kelime', fontsize=14, fontweight='bold')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Grafik kaydedildi: {save_path}")
    else:
        plt.show()
    
    plt.close()
