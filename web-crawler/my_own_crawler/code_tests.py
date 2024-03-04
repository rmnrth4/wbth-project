import re

pattern = re.compile(r"^\s*$")

# Beispiel Verwendung:
strings = ["", "    ", "\t", "  abc ", "123", "\n", "\n\t  ", "\n\n\n\n\n"]

chained_text = ""
for s in strings:
    if not pattern.match(s):
        chained_text += s
print(chained_text)

# for item in list_of_text_elements.extract():
#     if not pattern.match(s):

# return chained_text
