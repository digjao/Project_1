import re
import os
import chardet
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


#funcao 
def prefixo(title):
    lista = []    
    _, filenames = default_storage.listdir("entries")
    for filename in filenames:
        if filename.endswith(".md"):
            match = re.search(title, filename,re.IGNORECASE) 
            if match: 
                lista.append(re.sub(r"\.md$", "", filename))
    return lista

def get_entry(title):
    try:
        with open(f"entries/{title}.md", "rb") as f:  # Abra em modo binário
            content = f.read()
            # Detecta a codificação
            encoding = chardet.detect(content)['encoding']
            # Decodifica o conteúdo com a codificação detectada
            return content.decode(encoding)
    except FileNotFoundError:
        return None
    except UnicodeDecodeError:
        return "Erro ao decodificar o arquivo. Verifique a codificação."


def delete_entry(title):
    filepath = f"entries/{title}.md"
    if os.path.exists(filepath):  # Verifica se o arquivo existe
        os.remove(filepath)  # Remove o arquivo       