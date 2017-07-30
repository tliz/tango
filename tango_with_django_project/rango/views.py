from django.shortcuts import render

from rango.models import Category, Page

from rango.forms import CategoryForm, PageForm

from django.contrib.auth.decorators import login_required
# from rango.forms import UserForm, UserProfileForm

# from django.http import HttpResponse

# def index(request):
# 	return HttpResponse("Rango says hey there partner!" + "<a href='about/'>About</a>")

# def about(request):
# 	return HttpResponse("Rango says here is the about page." + "<a href='/rango/'>Home</a>")

def index(request):
# Construct a dictionary to pass to the template engine as its context.
# Note the key boldmessage is the same as {{ boldmessage }} in the template! 
	# context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}

# Return a rendered response to send to the client.
# We make use of the shortcut function to make our lives easier. # Note that the first parameter is the template we wish to use. 
	# return render(request, 'rango/index.html', context=context_dict)

	category_list = Category.objects.order_by('-likes')[:5]

	page_list = Page.objects.order_by('-views')[:5]


	context_dict = {'categories': category_list, 'pages': page_list}
	# Render the response and send it back!
	return render(request, 'rango/index.html', context_dict)


def about(request):
	print(request.method)
	print(request.user)
	return render(request, 'rango/about.html', {})


def show_category(request, category_name_slug):
	# Create a context dictionary which we can pass # to the template rendering engine. 
	context_dict = {}

	try:
		# Can we find a category name slug with the given name?
		# If we can't, the .get() method raises a DoesNotExist exception.
		# So the .get() method returns one model instance or raises an exception. 
		category = Category.objects.get(slug=category_name_slug)
		
		# Retrieve all of the associated pages.
		# Note that filter() will return a list of page objects or an empty list 
		pages = Page.objects.filter(category=category)
		
		# Adds our results list to the template context under name pages.
		context_dict['pages'] = pages
		# We also add the category object from
		# the database to the context dictionary.
		# We'll use this in the template to verify that the category exists. 
		context_dict['category'] = category
	except Category.DoesNotExist:
		# We get here if we didn't find the specified category. # Don't do anything -
		# the template will display the "no category" message for us.
		context_dict['category'] = None
		context_dict['pages'] = None

	# Go render the response and return it to the client.
	return render(request, 'rango/category.html', context_dict)

def add_category(request):
	form = CategoryForm()

	# A HTTP POST?
	if request.method == 'POST':
		form = CategoryForm(request.POST)

		# Have we been provided with a valid form?
		if form.is_valid():
		# Save the new category to the database. 
			form.save(commit=True)
			# cat = form.save(commit=True)
			# Now that the category is saved
			# We could give a confirmation message
			# But since the most recent category added is on the index page # Then we can direct the user back to the index page.
			return index(request)
		else:
			# The supplied form contained errors - # just print them to the terminal.
			print(form.errors)
			# Will handle the bad form, new form, or no form supplied cases. # Render the form with error messages (if any).
	return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug): 
	context_dict = {}
	try:
		category = Category.objects.get(slug=category_name_slug)
		pages = Page.objects.filter(category=category)

		context_dict['pages'] = pages

	except Category.DoesNotExist:
		category = None
		context_dict['pages'] = None

	form = PageForm()
	if request.method == 'POST':
		form = PageForm(request.POST) 
		if form.is_valid():
			if category:
				page = form.save(commit=False)
				page.category = category
				page.views = 0
				page.save()
				return show_category(request, category_name_slug)
		else: 
			print(form.errors)

	context_dict = {'form':form, 'category': category, 'pages': pages }
	return render(request, 'rango/add_page.html', context_dict)


@login_required
def like_category(request):
	cat_id = None
	if request.method == 'GET':
		cat_id = request.GET['category_id']
		likes = 0
	if cat_id:
		cat = Category.objects.get(id=int(cat_id))
		if cat:
			likes = cat.likes + 1
			cat.likes =  likes
			cat.save()
	return HttpResponse(likes)

def get_category_list(max_results=0, starts_with=''):
	cat_list = []
	if starts_with:
		cat_list = Category.objects.filter(name__istartswith=starts_with)
	if max_results > 0:
		if len(cat_list) > max_results:
			cat_list = cat_list[:max_results]
	return cat_list

def suggest_category(request):
	cat_list = []
	starts_with = ''
	if request.method == 'GET':
		starts_with = request.GET['suggestion']
		cat_list = get_category_list(8, starts_with)
	return render(request, 'rango/cats.html', {'cats': cat_list })





