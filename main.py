from parser import read_data, sanitize_messages
from NER import apply_ner, filter_messages

if __name__ == "__main__":    
    dir = input("Lütfen veri dosyasının konumunu giriniz (varsayılan: C:\\Users\\cagin\\Desktop\\New folder\\data.txt): ")

    messages , author = read_data(loc = dir)

    sanitized_messages = sanitize_messages(messages)
    
    ents = apply_ner(sanitized_messages["i"])
    ents_list = ents
    text = sanitized_messages["i"][0]

    filter_message = [{"text": t, "ents": e} for t, e in zip(text, ents_list)]

    ankara = filter_messages(filter_message, label="LOC", query="ankara", min_score=0.7)

    print(ankara)