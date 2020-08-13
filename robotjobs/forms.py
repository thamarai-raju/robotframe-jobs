from django import forms

from .models import Product

class ProductForm(forms.ModelForm):
	title = forms.CharField(widget=forms.Textarea(
							attrs={ 
								"placeholder":'Your title'
								}
							) 						
			)# override the below 'title'
	class Meta:
		model = Product
		fields = [
			'title',
			'description',
			'price'
			]

	# def clean_title(self):
	# 	title =self.cleaned_data.get('title')
	# 	if 'title' in title:
	# 		return title
	# 	else:
	# 		raise forms.ValidationError('Please have \'title\' ')


class RawJobScedule(forms.Form):
	# title = forms.CharField()
	# description = forms.CharField(
	# 					required=False,
	# 					widget=forms.Textarea(
	# 						attrs={
	# 							"placeholder":'Your desciption',
	# 							"class": "new-class-name two",
	# 							"id": "my-id",
	# 							"rows":20,
	# 							'cols': 120,
	# 						}
	# 					)
	# 				)
	# price = forms.DecimalField()
	job_suite = forms.CharField()
	job_testcase = forms.CharField()
	job_tags = forms.CharField()
	job_variables = forms.CharField()

	
		