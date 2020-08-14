from django.conf.urls import url, include
from . import views
from django.contrib.auth.decorators import login_required, permission_required

urlpatterns = [
    # url('', views.hello_world, name='hello_world'),
    #url(r'^$', views.product_index, name='product_index'),
    #url(r'^(?P<pk>[0-9]+)$', views.product_detail, name='product_detail'), #pk is the parameter name = path(<int:post_id>)
    # url(r'create', views.product_create, name='product_create'), 

    url(r'scheduler/$',login_required(views.JobScheduler.as_view(), login_url='login'), name='job_scheduler'), 
    url(r'scheduler/group/(?P<job_group_selected>[^//]+)$', views.JobGroup.as_view(), name='job_group'), 
    url(r'scheduler/feature/(?P<job_group_selected>[^//]+)/(?P<job_feature_selected>[^//]+)$', views.JobFeature.as_view(), name='job_feature'), 
    url(r'scheduler/suite/(?P<job_group_selected>[^//]+)/(?P<job_feature_selected>[^//]+)/(?P<job_testsuite_selected>[^//]+)$', views.JobTestsuite.as_view(), name='job_testsuite'), 
    url(r'scheduler/jobrun/(?P<job_group_selected>[^//]+)$', views.JobRobotRun.as_view(), name='job_robot_run'), 
    url(r'scheduler/jobadd/(?P<job_group_selected>[^//]+)/(?P<job_feature_selected>[^//]+)/(?P<job_testsuite_selected>[^//]+)/(?P<job_testcase_selected>[^//]+)$', 
        views.JobRobotAdd.as_view(), name='job_robot_add'), 

    url(r'jobview/$', login_required(views.JobView.as_view(), login_url='login'), name='job_view'), 
    url(r'jobview/(?P<time_stamp>[^//]+)$', views.JobView.as_view(), name='job_view'),
    url(r'jobview/(?P<time_stamp>.*)/(?P<job_suite_selected>[^//]+)$', views.JobViewSuite.as_view(), name='job_view_suite'), 
    url(r'completed/$', login_required(views.JobCompleted.as_view(), login_url='login'), name='job_completed'), 
    
    # url(r'index/(?P<id>[0-9]+)', views.ProductClassView.as_view(template_name='product_index.html'), name='product_class_refresh'),
    # url(r'^list/(?P<id>[0-9]+)$', views.ProductClassView.as_view(template_name='product_detail.html', list_obj=True), name='product_class_detail'), 
    # url(r'create', login_required(views.ProductClassView.as_view(template_name='product_create.html', create_obj=True), login_url='login'), name='product_class_create'), 
    # url(r'^delete/(?P<id>[0-9]+)$', views.ProductClassView.as_view(delete_obj=True), name='product_class_delete'), 
    # url(r'^update/(?P<id>[0-9]+)$', views.ProductClassView.as_view(template_name='product_create.html', update_obj=True), name='product_class_update'), 
     

    url(r"^", include("django.contrib.auth.urls")),
    # url(r'logout/', login_required(views.ProductClassView.as_view(), login_url='login'), name='logout' )
    
]
