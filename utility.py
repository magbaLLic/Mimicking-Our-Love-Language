"""
Utility Modülü
Metin temizleme ve PII maskeleme fonksiyonları.
"""
import re
from pii import extract_emails, extract_phone_numbers

RE_IBAN = re.compile(r'\b[A-Z]{2}\d{2}(?:\s?\d{4}){4,7}\b')  # IBAN desenini tanımlayan regex
RE_MEDIA = re.compile(r'(?m)^\s<\sMedya\s+Dahil\s+Edilmedi\s>\s\n?')  # medya mesajlarını tanımlayan desen
RE_EMAIL = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
RE_PHONE = re.compile(r'\b(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}\b')


def mask_iban(text: str) -> str:
    """
    IBAN numaralarını maskele.
    
    Args:
        text: Masklenecek metin
        
    Returns:
        str: Maskelenmiş metin
    """
    iban_pattern = RE_IBAN  
    masked_text = re.sub(iban_pattern, '**** **** **** ****', text)
    return masked_text


def mask_media(text: str) -> str:
    """
    Medya mesajlarını temizle.
    
    Args:
        text: Temizlenecek metin
        
    Returns:
        str: Temizlenmiş metin
    """
    return text.replace("<Medya dahil edilmedi>", "").strip()


def mask_email(text: str, replacement: str = "***@***.***") -> str:
    """
    E-posta adreslerini maskele.
    
    Args:
        text: Masklenecek metin
        replacement: Yerine konulacak metin
        
    Returns:
        str: Maskelenmiş metin
    """
    return re.sub(RE_EMAIL, replacement, text)


def mask_phone(text: str, replacement: str = "***-***-****") -> str:
    """
    Telefon numaralarını maskele.
    
    Args:
        text: Masklenecek metin
        replacement: Yerine konulacak metin
        
    Returns:
        str: Maskelenmiş metin
    """
    return re.sub(RE_PHONE, replacement, text)


def clean_text(text: str, mask_emails: bool = False, mask_phones: bool = False) -> str:
    """
    Metni temizle ve PII bilgilerini maskele.
    
    Args:
        text: Temizlenecek metin
        mask_emails: E-postaları maskele
        mask_phones: Telefon numaralarını maskele
        
    Returns:
        str: Temizlenmiş metin
    """
    text = mask_iban(text)
    text = mask_media(text)
    
    if mask_emails:
        text = mask_email(text)
    
    if mask_phones:
        text = mask_phone(text)
    
    return text

