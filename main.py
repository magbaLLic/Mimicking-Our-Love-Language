messages = {
    "i": [],
    "ç": []
}

with open("C:\\Users\\ceren\\Desktop\\proje\\Mimicking-Our-Love-Language\\data\\data.txt", "r", encoding="utf-8") as f:
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