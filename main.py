messages = {
    "i": [],
    "ç": []
}

def mask_iban(text):
    import re
    iban_pattern = r'\b[A-Z]{2}\d{2}(?:\s?\d{4}){4,7}\b'
    masked_text = re.sub(iban_pattern, '**** **** **** ****', text)
    return masked_text


def read_data(loc = "C:\\Users\\ceren\\Desktop\\proje\\Mimicking-Our-Love-Language\\data\\data.txt"):
    
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
            if author.startswith("İremmm"):
                messages["i"].append(message)
            elif author.startswith("Çağın"):
                messages["ç"].append(message)
    print(f"İrem mesaj sayısı: {len(messages['i'])}") 
    print(f"Çağın mesaj sayısı: {len(messages['ç'])}")
    return messages, author
def sanitize_messages(messages):
    sanitized = {}
    for author, msgs in messages.items():
        sanitized_msgs = [mask_iban(msg) for msg in msgs]
        sanitized[author] = sanitized_msgs
    return sanitized
if __name__ == "__main__":    
    dir = input("Lütfen veri dosyasının konumunu giriniz (varsayılan: C:\\Users\\cagin\\Desktop\\New folder\\data.txt): ")
    messages , author = read_data(loc = dir)
    sanitized_messages = sanitize_messages(messages)
    