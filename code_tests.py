def get_joined_text(list_of_text_elements):
    import re

    pattern = re.compile(r"^\s*$")
    joined_text = ""

    for item in list_of_text_elements.extract():
        if not pattern.match(item):
            joined_text += item.strip() + " "

    # Entfernen Sie das letzte Leerzeichen vor der Rückgabe
    return joined_text.rstrip()


def get_joined_text(list_of_text_elements):
    import re

    pattern = re.compile(r"^\s*$")
    joined_text = ""
    joined_text.join(
        [
            item.strip() + " "
            for item in list_of_text_elements
            if not pattern.match(item)
        ]
    )
    return joined_text.rstrip()


# Beispielaufruf:
text_elements = ["   Hello   ", "World", "   ", "   Python   "]
result = get_joined_text(text_elements)
print(result)
