codecs = ["cp1252", "cp437", 'Latin-1', 'ISO-8859-1', 'Windows-1251',
          'KOI8-R', 'CP437']
for codec in codecs:
    try:
        with open("simple_text.txt", "r", encoding=codec) as file:
            text = file.read()
        print(codec.rjust(12), "|", text)
    except:
        pass

for i in codecs:
    try:
        print(text.encode(i).decode('UTF-8'))
        break
    except:
        pass
