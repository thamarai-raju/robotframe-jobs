from django.conf.urls import url, include
from . import views
from django.contrib.auth.decorators import login_required, permission_required

urlpatterns = [
    # url('', views.hello_world, name='hello_world'),
    #url(r'^$', views.product_index, name='product_index'),
    #url(r'^(?P<pk>[0-9]+)$', views.product_detail, name='product_detail'), #pk is the parameter name = path(<int:post_id>)
    # url(r'create', views.product_create, name='product_create'), 

    url(r'index/$', login_required(views.ProductClassView.as_view(), login_url='login'), name='product_class_index'), 
    url(r'index/(?P<id>[0-9]+)', views.ProductClassView.as_view(template_name='product_index.html'), name='product_class_refresh'),
    url(r'^list/(?P<id>[0-9]+)$', views.ProductClassView.as_view(template_name='product_detail.html', list_obj=True), name='product_class_detail'), 
    url(r'create', login_required(views.ProductClassView.as_view(template_name='product_create.html', create_obj=True), login_url='login'), name='product_class_create'), 
    url(r'^delete/(?P<id>[0-9]+)$', views.ProductClassView.as_view(delete_obj=True), name='product_class_delete'), 
    url(r'^update/(?P<id>[0-9]+)$', views.ProductClassView.as_view(template_name='product_create.html', update_obj=True), name='product_class_update'), 
     

    url(r"^", include("django.contrib.auth.urls")),
    # url(r'logout/', login_required(views.ProductClassView.as_view(), login_url='login'), name='logout' )
    
]
