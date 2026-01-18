import re

def extract_numbers(text):
    return re.findall(r'\d+', text)
def extract_emails(text):
    return re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
def extract_urls(text):
    return re.findall(r'http[s]?://\S+', text)
def extract_dates(text):
    return re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', text)
def extract_times(text):
    return re.findall(r'\b\d{1,2}:\d{2}(?:\s?[APMapm]{2})?\b', text)
def extract_phone_numbers(text):
    return re.findall(r'\b(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}\b', text)
def extract_addresses(text):
    return re.findall(r'\d+\s+[A-Za-z]+\s+(Street|St|Avenue|Ave|Boulevard|Blvd|Road|Rd|Lane|Ln|Drive|Dr)\b', text)
def extract_credit_card_numbers(text):
    return re.findall(r'\b(?:\d[ -]*?){13,16}\b', text)
def extract_ip_addresses(text):
    return re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', text)
def extract_social_security_numbers(text):
    return re.findall(r'\b\d{3}-\d{2}-\d{4}\b', text)
def extract_license_plates(text):
    return re.findall(r'\b[A-Z0-9]{1,7}\b', text)

def extract_all_pii(text):
    pii_data = {
        "numbers": extract_numbers(text),
        "emails": extract_emails(text),
        "urls": extract_urls(text),
        "dates": extract_dates(text),
        "times": extract_times(text),
        "phone_numbers": extract_phone_numbers(text),
        "addresses": extract_addresses(text),
        "credit_card_numbers": extract_credit_card_numbers(text),
        "ip_addresses": extract_ip_addresses(text),
        "social_security_numbers": extract_social_security_numbers(text),
        "license_plates": extract_license_plates(text)
    }
    return pii_data
