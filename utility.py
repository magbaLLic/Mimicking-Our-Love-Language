import re


RE_IBAN = re.compile(r'\b[A-Z]{2}\d{2}(?:\s?\d{4}){4,7}\b')  # IBAN desenini tanımlayan regex
RE_MEDIA = re.compile(r'(?m)^\s<\sMedya\s+Dahil\s+Edilmedi\s>\s\n?')  # medya mesajlarını tanımlayan desen


def mask_iban(text): # IBAN numaralarını maskeler
    iban_pattern = RE_IBAN  
    masked_text = re.sub(iban_pattern, '**** **** **** ****', text)
    return masked_text


def mask_media(text): # medya mesajlarını maskeler
    return (text.replace("<Medya dahil edilmedi>","").strip())


