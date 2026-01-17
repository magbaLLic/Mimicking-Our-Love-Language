from utility import mask_iban, mask_media

messages = {
    "i": [],
    "ç": []
}


def sanitize_messages(messages, mask_emails=False, mask_phones=False):
    """
    Mesajları temizle ve PII bilgilerini maskele.
    
    Args:
        messages: Temizlenecek mesaj dict'i
        mask_emails: E-postaları maskele
        mask_phones: Telefon numaralarını maskele
        
    Returns:
        dict: Temizlenmiş mesajlar
    """
    from utility import clean_text
    
    sanitized = {}
    for author, msgs in messages.items():
        sanitized_msgs = [clean_text(msg, mask_emails=mask_emails, mask_phones=mask_phones) for msg in msgs]
        sanitized[author] = sanitized_msgs
    return sanitized

def read_data(loc = "C:\\Users\\cagin\\Desktop\\New folder\\data.txt"):
    """
    Veri dosyasını okur ve mesajları parse eder.
    
    Args:
        loc: Veri dosyası yolu
        
    Returns:
        tuple: (messages_dict, author)
    """
    import os
    
    if not os.path.exists(loc):
        raise FileNotFoundError(f"Dosya bulunamadı: {loc}")
      
    with open(loc, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
           
            if not line:
                continue

            # sistem mesajlarını atla
            if " - " not in line or ":" not in line:
                continue

            # tarih/saat kısmını ayır
            try:
                meta, text = line.split(" - ", 1)
                author, message = text.split(":", 1)
            except ValueError:
                continue  # beklenmeyen format varsa geç

            author = author.strip()
            message = message.strip()
            

            # yazarı key'e mapleme
            if author.startswith("İremmm") or author.startswith("İrem"):
                messages["i"].append(message)
            elif author.startswith("Çağın") or author.startswith("Cagin"):
                messages["ç"].append(message)
            else:
                # Bilinmeyen yazarlar için genel bir key kullan
                if "unknown" not in messages:
                    messages["unknown"] = []
                messages["unknown"].append(message)
    
    print(f"İrem mesaj sayısı: {len(messages.get('i', []))}") 
    print(f"Çağın mesaj sayısı: {len(messages.get('ç', []))}")
    if "unknown" in messages:
        print(f"Bilinmeyen yazar mesaj sayısı: {len(messages['unknown'])}")
    
    return messages, author