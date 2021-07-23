from django.http.response import HttpResponseRedirect
import markdown2 
from django.urls import reverse

from django.shortcuts import render


from . import util


def index(request):
    return render(request, "encyclopedia/index.html", 
    {"entries": util.list_entries() })


def search(request): 
    value = request.GET['q']
    if(util.get_entry(value) is not None):
        return HttpResponseRedirect(reverse("entry", kwargs={'title': value}))
    else:
        sugestoes = util.prefixo(value)
        return render(request,"encyclopedia/errorpage.html", {'title': value , 'listasugestoes':sugestoes})



def entry(request, title):
    EntryPage = util.get_entry(title)
    if EntryPage is None:
        return render(request, "encyclopedia/errorpage.html",{"title":title}) 
    else: 
        return render(request, "encyclopedia/entry.html", {"title":title, "entry":markdown2.markdown(EntryPage)})
    
def newEntry(request):
    return render(request, "encyclopedia/newEntry.html")


        
#passo1, pegar titulo
#passo2, pesquisar a entry pelo title
   