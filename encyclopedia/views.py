from django.shortcuts import render
from markdown2 import Markdown
from . import util
import random

# Helper function that converts Markdown content to HTML using the Markdown2 library.
def md_to_html(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content == None:
        return None
    else:
        html = markdowner.convert(content)
        return html
    
# Renders the index.html template with a list of all encyclopedia entries as its 
# context variable.
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Takes a title parameter and renders the entry.html template with the HTML content 
# of the encyclopedia entry with that title as its context variable. 
# If no entry exists with that title, it renders the error.html template with an 
# error message.
def entry(request, title):
    requested_content = md_to_html(title)
    if requested_content == None:
        return render(request, "encyclopedia/error.html", {
            "msg_title":"How Interesting!",
            "msg_body": "You are looking for something that does NOT exist!!!"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title":title,
            "body":requested_content,
        })

# Takes a search query from a POST request and performs a search for encyclopedia entries 
# that match the query. If an exact match is found, it renders the entry.html template 
# with the HTML content of the matching entry. If no exact match is found, 
# it renders the search.html template with a list of suggested entries.
def search(request):
    if request.method == "POST":
        search = request.POST.get("q")
        content = md_to_html(search)
        if content is not None:
            return render(request, "encyclopedia/entry.html", {
                "title":search,
                "body":content,
            })
        else:
            suggestions=[]
            entries = util.list_entries() 
            for entry in entries:
                if search.lower() in entry.lower():
                    suggestions.append(entry)
            return render(request, "encyclopedia/search.html", {
                        "suggestions":suggestions,
                })


#  Renders the new.html template for creating a new encyclopedia entry. 
# If a POST request is received, it saves the new entry to the encyclopedia using 
# the util.save_entry function and redirects the user to the newly created entry.
def new(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST.get("title")
        body = request.POST.get("body")
        exist = util.get_entry(title)
        if exist is not None:
            return render(request, "encyclopedia/error.html", {
            "msg_title":"Insertion Failed",
            "msg_body": f"{title} exist!!!"            
            })
        else:
            util.save_entry(title, body)
            heading = f"<h1>{title}</h1>"
            body = md_to_html(title)
            return render(request, "encyclopedia/entry.html", {
                "title":title,
                "body":heading + body,
            })

# Takes a title parameter and renders the edit.html template with 
# the existing body of the encyclopedia entry with that title as its context variable.
def edit(request):
    if request.method == "POST":
        title = request.POST.get("edit_title")
        body = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "body": body,
        })
    
# Receives a POST request with updated title and body fields for an encyclopedia entry 
# and saves the updates to the encyclopedia using the util.save_entry function. 
# It then redirects the user to the updated entry.
def save_edit(request):
    if request.method =="POST":
        title=request.POST.get("title")
        body=request.POST.get("body")
        util.save_entry(title, body)
        body_text=md_to_html(title)
        return render(request, "encyclopedia/entry.html", {
            "title":title,
            "body":body_text,
        })
    
# randomly selects an encyclopedia entry and renders the entry.html template with 
# its title and content as its context variables.
def random_choice(request):
    entries = util.list_entries()
    chance=random.choice(entries)
    chosen=md_to_html(chance)
    return render(request, "encyclopedia/entry.html", {
        "title":chance,
        "body":chosen,
    })

# receives a POST request with the title of an encyclopedia entry to delete, 
# deletes the entry using the util.delete_entry function, 
# and redirects the user to the index page.
def delete(request):
   if request.method == "POST":
        title = request.POST.get("delete_title")
        util.delete_entry(title)
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })