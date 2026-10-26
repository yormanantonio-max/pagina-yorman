with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('src="assets/images/logo_emblema_oficial.png"', 'src="assets/images/logo_emblema_oficial.png?v=20261026"')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Added cache-busting query param to logo in index.html")
