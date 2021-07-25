from django.http.response import HttpResponseRedirect
import markdown2 
from django.urls import reverse

from django.shortcuts import render


from . import util
import secrets


def index(request):
    return render(request, "encyclopedia/index.html", 
    {"entries": util.list_entries()})


def search(request): 
    results = request.GET['q']
    return HttpResponseRedirect(reverse("entry", kwargs={'title': results}))



#função que determina se o resultado digitado é EXATAMENTE igual a algum arquivo .md, caso seja EXATAMENTE igual,
#você é direcionado diretamente para esta pagina
#caso nao seja igual, você será direcionado para uma ERRORPAGE que irá te sugerir nomes que tenham letras iguais

def entry(request, title):
    EntryPage = util.get_entry(title)
    if EntryPage is None:
        sugestoes = util.prefixo(title)
        return render(request,"encyclopedia/errorpage.html", {'title': title , 'listasugestoes':sugestoes})
    else: 
        return render(request, "encyclopedia/entry.html", {"title":title, "entry":markdown2.markdown(EntryPage)})
    
def newEntry(request):
    return render(request, "encyclopedia/newEntry.html")


#para a função random, importei o modulo SECRETS para chamar a função CHOICE que é responsavel por escolher 
#algum elemento de uma nom-empty sequence
def random(request):
    entriesMD = util.list_entries()
    randomEntries = secrets.choice(entriesMD)
    return HttpResponseRedirect(reverse("entry", kwargs={'title':randomEntries}))
