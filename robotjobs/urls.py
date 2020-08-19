from django.conf.urls import url, include
from . import views
from django.contrib.auth.decorators import login_required, permission_required

urlpatterns = [

    url(r'scheduler/$',login_required(views.JobScheduler.as_view(), login_url='login'), name='job_scheduler'), 
    url(r'scheduler/group/(?P<job_group_selected>[^//]+)$', views.JobGroup.as_view(), name='job_group'), 
    url(r'scheduler/feature/(?P<job_group_selected>[^//]+)/(?P<job_feature_selected>[^//]+)$', views.JobFeature.as_view(), name='job_feature'), 
    url(r'scheduler/suite/(?P<job_group_selected>[^//]+)/(?P<job_feature_selected>[^//]+)/(?P<job_testsuite_selected>[^//]+)$', views.JobTestsuite.as_view(), name='job_testsuite'), 
    url(r'scheduler/jobrun/(?P<job_group_selected>[^//]+)$', views.JobRobotRun.as_view(), name='job_robot_run'), 
    url(r'scheduler/jobadd/(?P<job_group_selected>[^//]+)/(?P<job_feature_selected>[^//]+)/(?P<job_testsuite_selected>[^//]+)$', 
        views.JobRobotAdd.as_view(), name='job_robot_add'), 
    url(r'scheduler/jobcustomrun/$', views.JobRobotCustomRun.as_view(), name='job_robot_custom_run'), 

    url(r'jobview/$', login_required(views.JobView.as_view(), login_url='login'), name='job_view'), 
    url(r'jobview/(?P<time_stamp>[^//]+)$', views.JobView.as_view(), name='job_view'),
    url(r'jobview/(?P<time_stamp>.*)/(?P<job_suite_selected>[^//]+)$', views.JobViewSuite.as_view(), name='job_view_suite'), 
    url(r'completed/$', login_required(views.JobCompleted.as_view(), login_url='login'), name='job_completed'), 
    url(r'gitbranch/(?P<branch_name>.*)$', login_required(views.GitBranchSelect.as_view(), login_url='login'), name='git_branch'), 
    
    
    url(r"^", include("django.contrib.auth.urls")),
    
]
