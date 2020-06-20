import re

def remove_special_character(file): 
    cleaned_file = ""
    for k in file.split("\n"):
        cleaned_file += re.sub(r"[^a-zA-Z0-9]+", ' ', k) + "\n"
        
    return cleaned_file.lower()
    
def main():
    f = open(r'D:\\Desktop\\sent_news\\causality_connector\\data\\combine.txt',encoding="utf8")
    # f = open(r'D:\\Desktop\\sent_news\\causality_connector\\selected_causality_news.txt',encoding="utf8")

    file = f.read()

    cleaned = remove_special_character(file)

    # print(cleaned)
    f_c = open(r'D:\\Desktop\\sent_news\\causality_connector\\data\\cleaned_combine.txt', "w")

    f_c.write(cleaned)
    f_c.close()


main()