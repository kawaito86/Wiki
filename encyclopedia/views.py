from django.shortcuts import render
import markdown
import random
from . import util
from django.http import HttpResponse

def md_to_html(markdown_text):
    content = util.get_entry(markdown_text)
    markdowner = markdown.Markdown()
    if content is None:
         return None
    else:
        return markdowner.convert(content)


def index(request):
    return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
    })

def entry(request, title):
    html_content = md_to_html(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "This content does not exist"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })

def search(request):
    if request.method == "POST":
        query = request.POST['q']
        html_content = md_to_html(query)
        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": query,
                "content": html_content
            })
        else:
            all_entries = util.list_entries()
            list_of_entries = []
            for entry in all_entries:
                if query.lower() in entry.lower():
                    list_of_entries.append(entry)
            return render(request, "encyclopedia/search.html", {
                "list_of_entries": list_of_entries
            })

def new_entry(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        check = util.get_entry(title)
        if check is not None:
            return render(request, "encyclopedia/error.html", {
                "message": "This title already exists"
            })
        else:
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": content
            })
    else:
        return render(request, "encyclopedia/new.html")

def edit(request):
    if request.method == "POST":
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })

        
def save_edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        html_content = md_to_html(title)
        return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": html_content
            }) 

def random_page(request):
    all_entries = util.list_entries()
    random_entry = random.choice(all_entries) 
    html_content = md_to_html(random_entry)
    return render(request, "encyclopedia/entry.html", {
        "title": random_entry,
        "content": html_content
    })