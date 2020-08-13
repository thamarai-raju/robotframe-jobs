# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from products.models import Product
from django.http import HttpResponse, HttpResponseRedirect
from products.forms import ProductForm, RawProductForm
from django.views import View
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.

def hello_world(request):
	return render(request, 'hello_world.html', {})
	# return HttpResponse('<h1>Hello, World!</h1>')

# def product_index(request):
# 	products = Product.objects.all()
# 	context = {
# 		'products_key': products
# 	}
# 	return render(request, 'product_index.html', context)


# def product_detail(request, pk):
# 	product = Product.objects.get(pk=pk)
# 	context = {
# 		'product_key': product
# 	}
# 	return render(request, 'product_detail.html', context)


# def product_create(request):
	
# 	# below example for getting data from database
# 	# setting initial data
# 	initial_data = {
# 		'title':'My title'
# 	}

# 	# obj = Product.objects.get(title='adqwq')
# 	# obj = get_object_or_404(Product, title='adqwq')
# 	form = ProductForm(request.POST or None, initial=initial_data)
# 	# form = ProductForm(request.POST or None, initial=initial_data, instance=obj)
# 	# form = ProductForm(request.POST or None)
# 	context = {
# 		'form': form
# 	}
# 	if form.is_valid():
# 		#delete an object
# 		obj = None
# 		try:
# 			obj = Product.objects.get(title=form.cleaned_data.get('title'))
# 			#to delete the default values
# 			form = ProductForm(initial=initial_data)
# 			context = {
# 				'form': form
# 			}
# 			print form
# 		except:
# 			pass
# 		if obj:
# 			obj.delete()
# 		else:
# 			form.save()
	
	
# 	# print(request.GET)
# 	# print(request.POST)
# 	# if request.POST:
# 	# 	my_new_title = request.POST.get('title')
# 	# 	print(my_new_title)
# 	# 	# Product.objects.create(title=my_new_title) # to save to the database
# 	# context = {}
	
# 	# #below example for creatin raw data and saving to database
# 	# form = RawProductForm()# or form = RawProductForm(request.GET) 
# 	# if request.method == 'POST':
# 	# 	form = RawProductForm(request.POST)
# 	# 	if form.is_valid():
# 	# 		print(form.cleaned_data)
# 	# 		Product.objects.create(**form.cleaned_data)
# 	# 	else:
# 	# 		print(form.errors)
# 	# context = {
# 	# 		'form': form
# 	# 	}

# 	return render(request, 'product_create.html', context)



class ProductClassView(View):
	# template_name = 'product_index_old.html'
	template_name = 'product_index.html'
	create_obj = False
	delete_obj = False
	update_obj = False
	list_obj = False

	# @method_decorator(login_required)
	def get(self, request, id=None, *args, **kwargs):
		if self.create_obj:
			form = ProductForm()
			print dir(form)
			print dir(form.fields)
			context = {
				'form': form
			}
		elif self.update_obj:
			obj = get_object_or_404(Product, id=id)
			form = ProductForm(request.POST or None, instance=obj)
			context = {
				'form': form
			}
		elif self.delete_obj:
			product = Product.objects.get(id=id)
			product.delete()
			return HttpResponseRedirect(reverse('product_class_index'))
		elif self.list_obj:
				product = get_object_or_404(Product, id=id)
				context = {
					'product_key': product
				}
		else:
			products = Product.objects.all()
			if not id:	
				product = None
				# product = get_object_or_404(Product, title=products[0].title)				
			else:
				product = get_object_or_404(Product, id=id)
			context = {
					'products_key': products,
					'product_key' : product
				}
		#CALL ur python script 

		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		form = ProductForm(request.POST)
		if form.is_valid():
			# update an object
			obj = None
			try:
				obj = Product.objects.get(title=form.cleaned_data.get('title'))
			except:
				pass
			if obj:
				for each_item in form.cleaned_data:
					setattr(obj, each_item, form.cleaned_data.get(each_item))
				obj.save()
			else:
				form.save()
		return HttpResponseRedirect(reverse('product_class_index'))



