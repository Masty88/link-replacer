import re

def text_to_html(text):
    # Cerca gli URL nel testo
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    urls = re.findall(url_pattern, text)

    # Sostituisci ogni URL con un tag 'a'
    for url in urls:
        text = text.replace(url, f'<a href="{url}">{url}</a>')

    return text

# Testa la funzione
text = "https://www.sib.swiss/about/news/10978-deciphering-the-rhythmicity-of-metabolism-in-the-kidney#:~:text=Wigger%20from%20SIB%E2%80%99s-,Vital%2DIT%20Group%2C,-the%20researchers%20aimed"
html = text_to_html(text)
print(html)