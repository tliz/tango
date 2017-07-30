import os 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')


import django
django.setup()

from rango.models import Category, Page

def populate():

    # create lists of dictionaries containing pages we want to add into each Category
    # then create dictionary of dictionary for categories
    # this allows us to iterate through each data structure, and add data to our models

    python_pages = [
        {"title": "Official Python Tutorial", "url":"http://docs.python.org/2/tutorial/", "views":20},
        {"title":"How to Think like a Computer Scientist", "url":"http://www.greenteapress.com/thinkpython/", "views":76},
        {"title":"Learn Python in 10 Minutes", "url":"http://www.korokithakis.net/tutorials/python/", "views":58} 
    ]

    django_pages = [
        {"title":"Official Django Tutorial", "url":"https://docs.djangoproject.com/en/1.9/intro/tutorial01/", "views":90},
        {"title":"Django Rocks", "url":"http://www.djangorocks.com/", "views":40},
        {"title":"How to Tango with Django", "url":"http://www.tangowithdjango.com/", "views":46} 
    ]

    other_pages = [
        {"title":"Bottle", "url":"http://bottlepy.org/docs/dev/", "views":30},
        {"title":"Flask",  "url":"http://flask.pocoo.org", "views":50},
        {"title": "Facebook", "url":"http:facebook.com", "views":60},
        {"title": "Team Treehouse Winnie", "url": "http://teamtreehouse/winnietibingana", "views":20}
    ]

    cats = { "Python": {"pages": python_pages, "views": 128, "likes": 64}
    , "Django": {"pages": django_pages, "views": 64, "likes": 32}
    , "Other Frameworks": {"pages": other_pages, "views": 32, "likes": 16}
    }

    # go through cats dictionary, adds each category and adds all associates pages for it
    
    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data["views"], cat_data["likes"])
        for p in cat_data["pages"]:
            add_page(c, p["title"], p["url"], p['views'])

    # Print out the categories we have added.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))

def add_page(cat, title, url, views):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name)[0]
    c.views=views
    c.likes=likes
    c.save()
    return c

# Start execution here!
if __name__ == '__main__':
    print("Starting Rango population script...") 
    populate()