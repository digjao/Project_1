from django.forms.widgets import Textarea
from django.http.response import HttpResponseRedirect
import markdown2 
from django.urls import reverse
from django import forms
from django.shortcuts import render
from . import util
import secrets

class NewEntryForm(forms.Form):
    title = forms.CharField(
        label="New Entry",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control col-md-8 col-lg-8', 
                'placeholder': 'Type your entry here'}))
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class' : 'form-control col-md-8 col-lg-8',
                'rows': 10, 'placeholder':'Remember to use markdown sintax'}))
    edit = forms.BooleanField( initial=False, widget=forms.HiddenInput(), required=False)

def index(request):
    return render(request, "encyclopedia/index.html", 
    {"entries": util.list_entries()})


def search(request): 
    results = request.GET['q']
    return HttpResponseRedirect(reverse("entry", kwargs={'entry': results}))



#função que determina se o resultado digitado é EXATAMENTE igual a algum arquivo .md, caso seja EXATAMENTE igual,
#você é direcionado diretamente para esta pagina
#caso nao seja igual, você será direcionado para uma ERRORPAGE que irá te sugerir nomes que tenham letras iguais

def entry(request, entry):
    EntryPage = util.get_entry(entry)
    if EntryPage is None:
        sugestoes = util.prefixo(entry)
        return render(request,"encyclopedia/errorpage.html", {'entry': entry , 'listasugestoes':sugestoes})
    else: 
        return render(request, "encyclopedia/entry.html", {"title":entry, "entry":markdown2.markdown(EntryPage)})
    
def renderNewEntryPage(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if (util.get_entry(title) is None or form.cleaned_data["edit"] is True):
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry", kwargs={'entry': title}))
            else:
                return render(request, "encyclopedia/newEntry.html", {
                    "form":form,
                    "existing":True,
                    "entry":title
                })
        else:
            return render(request, "encyclopedia/newEntry.html", {
                "form":form,
                "existing":False
            })
    else:
        return render(request, "encyclopedia/newEntry.html", {
        "form": NewEntryForm(),
        "existing": False
        })

def edit(request, entry):
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return render(request, "encyclopedia/errorpage.html",{
            "entryTitle": entry
        })
    else:
        form = NewEntryForm()
        form.fields["title"].initial = entry
        form.fields["title"].widget = forms.HiddenInput()
        form.fields["content"].initial = entryPage
        form.fields["edit"].initial = True
        return render(request, "encyclopedia/newEntry.html", {
            "form": form,
            "edit": form.fields["edit"].initial,
            "entryTitle": form.fields["title"].initial
        })
#form.fields filled the fields with the informations that i alredy have 

def random(request):
    entriesMD = util.list_entries()
    randomEntries = secrets.choice(entriesMD)
    return HttpResponseRedirect(reverse("entry", kwargs={'entry':randomEntries}))
#para a função random, importei o modulo SECRETS para chamar a função CHOICE que é responsavel por escolher 
#algum elemento de uma nom-empty sequence

#def saveNewPage(request):
    # TO DO!
    # fi request.POST[]
    #textarea = request.POST['md']
    #title = request.POST['newEntryTitle']
    #util.save_entry(title,textarea)
    #return HttpResponseRedirect(reverse("entry", kwargs={'title':(title)}))

#def editPage(request,):
    #if request.method == "POST":

