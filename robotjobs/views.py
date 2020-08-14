# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import View
from celery.decorators import task
from lib.django.robot_execute import *

from .management.commands.load_test_data_to_db import load_testdata_to_db
from .models import *
import threading
import time
import re


class GetRobotService():

	def get_robot_service(self):
		return RobotExecute()


class GetModelInfo():

	def get_feature_by_tag(self, group_name):
		return list(set([x.testsuite for x in Testdata.objects.filter(tag__name=group_name)]))

	def get_testsuites_by_feature(self, group_name, feature_name):
		return list(set([x.testfile for x in Testdata.objects.
		 				filter(tag__name=group_name).filter(testsuite=feature_name)]))
	
	def get_testsuite_by_tag(self, group_name):
		return list(set([x.testfile for x in Testdata.objects.filter(tag__name=group_name)]))
	
	def get_testcases_by_testsuite(self, group_name, feature_name, testsuite_name):
		return list(set([x.testcase for x in Testdata.objects.
		 				filter(tag__name=group_name).filter(testsuite=feature_name).
		 				filter(testfile=testsuite_name)]))

	def get_custom_job_info(self):
		job_testsuite_list = [z for x,y,z in Job.objects.all().values_list()]
		custom_data_d = {}
		for each_job_testsuite in job_testsuite_list:
			test_cases = [y for x,y,z in 
				Job.objects.filter(testfile=each_job_testsuite).first().testcases.values_list()]
			custom_data_d[each_job_testsuite] = test_cases
		return custom_data_d

	def get_custom_added_jobs(self):
		return [(y,z) for x,y,z in Job.objects.all().values_list()]

class JobScheduler(View):
	template_name = 'job_scheduler.html'
	robot_data = GetRobotService().get_robot_service()

	def get(self, request, *args, **kwargs):


		#get git update when model is not populated
		load_testdata_to_db()
		# letswaitalot.delay(5)
		# print('escape')


		#add the full and custom to the above
		job_group_info_view = ['sanity','intermediate','full','custom']
		# job_group_selected = 'sanity'
		# job_group_selected = None
		job_run_list = None
		test_suite_list = None
		test_case_list = None
		
		context = {
		'job_groups': job_group_info_view,
		# 'job_group_selected': job_group_selected,
		'job_run_list': job_run_list,
		'test_suite_list': test_suite_list,
		'test_case_list': test_case_list
		}

		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		return render(request, self.template_name, {})
		


class JobGroup(View):
	template_name = 'job_scheduler.html'
	robot_data = GetRobotService().get_robot_service()
	get_model_info = GetModelInfo()
	
	def get(self, request, job_group_selected=None, *args, **kwargs):
		# suite_info, job_group_info = self.robot_data.get_suiteinfo()

		# #get all job groups
		# job_group_info_view = job_group_info.keys()
		#add the full and custom to the above
		job_group_info_view = ['sanity','intermediate','full','custom']
		
		#get the list of suite names in the group
		if job_group_selected != 'custom':
			job_run_list = self.get_model_info.get_feature_by_tag(job_group_selected)
		else:
			job_run_list = self.get_model_info.get_feature_by_tag('full')


		if job_group_selected != 'custom':
			job_feature_selected = job_run_list[0]
			test_suite_list = self.get_model_info.get_testsuites_by_feature(job_group_selected, job_feature_selected)
			job_testsuite_selected = test_suite_list[0]
			test_case_list = self.get_model_info.get_testcases_by_testsuite(job_group_selected, job_feature_selected,
									job_testsuite_selected)
			added_jobs = None
			job_added_flag = None
		else:
			test_suite_list = None
			test_case_list = None
			job_feature_selected = None
			job_testsuite_selected = None
		
			#Check if any custom jobs were added
			added_jobs = self.get_model_info.get_custom_added_jobs()
			job_added_flag = 'true' if added_jobs else None
				
		
		context = {
		'job_groups': job_group_info_view,
		'job_group_selected': job_group_selected,
		'job_run_list': job_run_list,
		'job_feature_selected': job_feature_selected,
		'test_suite_list': test_suite_list,
		'job_testsuite_selected': job_testsuite_selected,
		'test_case_list': test_case_list,
		'added_jobs': added_jobs,
		'job_added_flag': job_added_flag
		}

		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		return render(request, self.template_name, {})		


class JobFeature(View):
	template_name = 'job_scheduler.html'
	robot_data = GetRobotService().get_robot_service()
	get_model_info = GetModelInfo()

	def get(self, request, job_group_selected=None, job_feature_selected=None, *args, **kwargs):
		# suite_info, job_group_info = self.robot_data.get_suiteinfo()

		# #get all job groups
		# job_group_info_view = job_group_info.keys()
		#add the full and custom to the above
		job_group_info_view = ['sanity','intermediate','full','custom']
		
		#get the list of suite names in the group
		if job_group_selected != 'custom':
			job_run_list = self.get_model_info.get_feature_by_tag(job_group_selected)
		else:
			job_run_list = self.get_model_info.get_feature_by_tag('full')
		
		#get the list of suite suites in the group
		if job_group_selected != 'custom':
			test_suite_list = self.get_model_info.get_testsuites_by_feature(job_group_selected, job_feature_selected)
		else:
			test_suite_list = self.get_model_info.get_testsuites_by_feature('full', job_feature_selected)

		if job_group_selected != 'custom':
			job_testsuite_selected = test_suite_list[0]
			test_case_list = self.get_model_info.get_testcases_by_testsuite(job_group_selected, job_feature_selected,
								job_testsuite_selected)
			added_jobs = None
			job_added_flag = None
		else:
			job_testsuite_selected = None
			test_case_list = None
			#Check if any custom jobs were added
			added_jobs = self.get_model_info.get_custom_added_jobs()
			job_added_flag = 'true' if added_jobs else None

		print(test_suite_list)

		context = {
		'job_groups': job_group_info_view,
		'job_group_selected': job_group_selected,
		'job_run_list': job_run_list,
		'job_feature_selected': job_feature_selected,
		'test_suite_list': test_suite_list,
		'job_testsuite_selected': job_testsuite_selected,
		'test_case_list': test_case_list,
		'added_jobs': added_jobs,
		'job_added_flag': job_added_flag
		}

		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		return render(request, self.template_name, {})		



class JobTestsuite(View):
	template_name = 'job_scheduler.html'
	robot_data = GetRobotService().get_robot_service()
	get_model_info = GetModelInfo()

	def get(self, request, job_group_selected=None, job_feature_selected=None,job_testsuite_selected=None, *args, **kwargs):

		#add the full and custom to the above
		job_group_info_view = ['sanity','intermediate','full','custom']
		
		#get the list of suite names in the group
		if job_group_selected != 'custom':
			job_run_list = self.get_model_info.get_feature_by_tag(job_group_selected)
		else:
			job_run_list = self.get_model_info.get_feature_by_tag('full')
		if job_group_selected != 'custom':
			test_suite_list = self.get_model_info.get_testsuites_by_feature(job_group_selected, job_feature_selected)
		else:
			test_suite_list = self.get_model_info.get_testsuites_by_feature('full', job_feature_selected)

		if job_group_selected != 'custom':
			test_case_list = self.get_model_info.get_testcases_by_testsuite(job_group_selected, job_feature_selected,
								job_testsuite_selected)
			added_jobs = None
			job_added_flag = None
		else:
			test_case_list = self.get_model_info.get_testcases_by_testsuite('full', job_feature_selected,
								job_testsuite_selected)
			#Check if any custom jobs were added
			added_jobs = self.get_model_info.get_custom_added_jobs()
			job_added_flag = 'true' if added_jobs else None

		context = {
		'job_groups': job_group_info_view,
		'job_group_selected': job_group_selected,
		'job_run_list': job_run_list,
		'job_feature_selected': job_feature_selected,
		'test_suite_list': test_suite_list,
		'job_testsuite_selected': job_testsuite_selected,
		'test_case_list': test_case_list,
		'added_jobs': added_jobs,
		'job_added_flag': job_added_flag
		}

		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		return render(request, self.template_name, {})		

class JobRobotRun(View):
	
	def get(self, request, job_group_selected=None, *args, **kwargs):
		return JobView().get(request, job_group_selected)	

	def post(self, request, *args, **kwargs):
		return render(request, self.template_name, {})		

class JobRobotAdd(View):
	template_name = 'job_scheduler.html'
	get_model_info = GetModelInfo()

	def get(self, request, job_group_selected=None,  job_feature_selected=None, job_testsuite_selected=None, *args, **kwargs):
		return render(request, self.template_name, {})

	def post(self, request, job_group_selected=None, job_feature_selected=None, job_testsuite_selected=None, *args, **kwargs):
		
		#print(request.POST.getlist('testcase'))
		# print(job_group_selected)
		# print(job_feature_selected)
		# print(job_testsuite_selected)

		testcases = request.POST.getlist('testcase')

		job = Job(testsuite=job_feature_selected, testfile=job_testsuite_selected)
		job.save()
		for testcase in testcases:
			TestCase.objects.create(description=testcase, job=job)


		added_jobs = self.get_model_info.get_custom_added_jobs()
		
		#add the full and custom to the above
		job_group_info_view = ['sanity','intermediate','full','custom']
		
		#get the list of suite names in the group
		job_run_list = self.get_model_info.get_feature_by_tag('full')
		test_suite_list = self.get_model_info.get_testsuites_by_feature('full', job_feature_selected)
		test_case_list = self.get_model_info.get_testcases_by_testsuite('full', job_feature_selected,
								job_testsuite_selected)

		context = {
		'job_groups': job_group_info_view,
		'job_group_selected': job_group_selected,
		'job_run_list': job_run_list,
		'job_feature_selected': job_feature_selected,
		'test_suite_list': test_suite_list,
		'job_testsuite_selected': job_testsuite_selected,
		'test_case_list': test_case_list,
		'added_jobs': added_jobs,
		'job_added_flag': 'true'
		}


		return render(request, self.template_name, context)		
	
class JobRobotCustomRun(View):
		
	def get(self, request, job_group_selected=None, *args, **kwargs):
		return JobView().get(request, job_custom_run=True)	

	def post(self, request, *args, **kwargs):
		return render(request, self.template_name, {})	

"""
class Job(models.Model):
	testsuite = models.CharField(max_length=100)
    testfile  = models.CharField(max_length=200)
"""

class JobView(View):
	template_name = 'job_view.html'
	robot_service_data = GetRobotService()
	robot_data = robot_service_data.get_robot_service()
	get_model_info = GetModelInfo()

	def get(self, request, job_group_selected=None, time_stamp=None, job_custom_run=None, *args, **kwargs):

		if job_group_selected:
			# input_job_d = [
			# 	{
			# 		'testsuite_id':'1',
			# 		'suite_name':'vpn_tests',
			# 		# 'include_tags':[],
			# 		'include_tags':['test1'],
			# 		# 'exclude_tags':['test1','test2','test3','test4'],
			# 		# 'exclude_tags':[],
			# 		# 'testcases':['Verify SPOKE ANYNET per site'],
			# 	},
			# 	{
			# 		'testsuite_id':'2',
			# 		'suite_name':'route_manager_cli_tests',
			# 		'include_tags':['sanity'],
			# 		# 'exclude_tags':['sanity'],
			# 		'testcases':[],
			# 	},
			# 	# {
			# 	# 	'testsuite_id':'3',
			# 	# 	'suite_name':'colgate',
			# 	# 	'include_tags':[],
			# 	# 	'exclude_tags':[],
			# 	# 	'testcases':['Changes for colgate customer config'],
			# 	# }
			# ]

			job_testsuite_list = self.get_model_info.get_testsuite_by_tag(job_group_selected)
			input_job_d = []
			count =1
			include_tags = [job_group_selected] if job_group_selected != 'full' else []
			for each_job_testsuite in job_testsuite_list:
				each_input_job_d = {
						'testsuite_id': str(count),
						'suite_name': each_job_testsuite,
						'include_tags': include_tags
					}
				count += 1
				input_job_d.append(each_input_job_d)

			print(input_job_d)

			# @task(name="justsleeps")
			# def temp1():
			# 	time.sleep(10)

			run_jobs.delay(input_job_d)
		
			# download_thread = threading.Thread(target=self.robot_data.run_jobs, args=input_job_d)
			# download_thread.start()
		elif job_custom_run:
			
			job_testsuite_d = self.get_model_info.get_custom_job_info()
			input_job_d = []
			count =1
			for each_job_testsuite,each_job_testcases in job_testsuite_d.iteritems():
				each_input_job_d = {
						'testsuite_id': str(count),
						'suite_name': each_job_testsuite,
						'testcases': each_job_testcases
					}
				count += 1
				input_job_d.append(each_input_job_d)

			print(input_job_d)

			run_jobs.delay(input_job_d)

			Job.objects.all().delete()
			TestCase.objects.all().delete()

		# return render(request, self.template_name, {})

			


		job_result_data_service = self.robot_data.get_status(time_stamp)
		#get suite name
		job_name = '-'.join(job_result_data_service.get('job_name'))
		#get teimstamp
		org_timestamp = job_result_data_service.get('timestamp')
		display_timestamp = re.sub('[-]',':',org_timestamp.split('.')[0])

		job_testsuite_result = []
		result_each_id = []
		for each_job_result_data in job_result_data_service['results']:
			testsuite_status = each_job_result_data.get('testsuite_status')
			testsuite_name = each_job_result_data.get('testsuite_name')
			testsuite_error = each_job_result_data.get('error')
			testcases_list = each_job_result_data.get('testcases',[])
			if not testsuite_error:
				testsuite_result_link = each_job_result_data.get('result_link')
				if testsuite_status == 'RUNNING' or \
						testsuite_status == 'YET TO START':
					job_testsuite_result.append((testsuite_name,testsuite_status,testsuite_result_link))
				elif 'ERROR' in testsuite_status:
					job_testsuite_result.append((testsuite_name,'Error', None))
				else:
					job_testsuite_result.append((testsuite_name,
						each_job_result_data.get('testsuite_result'),testsuite_result_link))
			else:
				job_testsuite_result.append((testsuite_name,'Error', None))
			if testcases_list:
				for each_testcase_name in testcases_list:
						result_each_id.append(each_testcase_name['testcase_result'])
			else:
				result_each_id.append('ERROR')

		#compute the final result
		full_job_status = 'PASS'
		for x in result_each_id:
			if x == 'YET TO START' or x == 'RUNNING':
				full_job_status = 'RUNNING'
				break
			elif x != 'PASS':
				full_job_status = 'FAIL'
				break

		job_testcase_result = None

		context = {
		'job_name':job_name,
		'org_timestamp':org_timestamp,
		'display_timestamp':display_timestamp,
		'full_job_status': full_job_status,
		'job_testsuite_result': job_testsuite_result,
		'job_testcase_result': job_testcase_result,
		}
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		return render(request, self.template_name, {})		



class JobViewSuite(View):
	template_name = 'job_view.html'
	robot_data = GetRobotService().get_robot_service()
	
	def get(self, request, time_stamp=None, job_suite_selected=None, *args, **kwargs):
		
		print(time_stamp)
		job_result_data_service = self.robot_data.get_status(time_stamp)
		#get suite name
		job_name = '-'.join(job_result_data_service.get('job_name'))
		#get teimstamp
		org_timestamp = job_result_data_service.get('timestamp')
		display_timestamp = re.sub('[-]',':',org_timestamp.split('.')[0])

		job_testsuite_result = []
		job_testcase_result = []
		result_each_id = []
		job_testsuite_error = ''
		for each_job_result_data in job_result_data_service['results']:
			testsuite_status = each_job_result_data.get('testsuite_status')
			testsuite_name = each_job_result_data.get('testsuite_name')
			testsuite_error = each_job_result_data.get('error')
			testcases_list = each_job_result_data.get('testcases',[])
			if not testsuite_error:
				testsuite_result_link = each_job_result_data.get('result_link')
				if testsuite_status == 'RUNNING' or \
						testsuite_status == 'YET TO START':
					job_testsuite_result.append((testsuite_name,testsuite_status,testsuite_result_link))
				elif 'ERROR' in testsuite_status:
					job_testsuite_result.append((testsuite_name,'Error', None))
				else:
					job_testsuite_result.append((testsuite_name,
						each_job_result_data.get('testsuite_result'),testsuite_result_link))
				if testsuite_name == job_suite_selected:
					for each_testcase_name in testcases_list:
						job_testcase_result.append((each_testcase_name['name'], each_testcase_name['testcase_result']))
			else:
				job_testsuite_result.append((testsuite_name,'Error',None))
				if testsuite_name == job_suite_selected:
					job_testsuite_error = testsuite_error

			for each_testcase_name in testcases_list:
					result_each_id.append(each_testcase_name['testcase_result'])

		#compute the final result
		full_job_status = 'PASS'
		for x in result_each_id:
			if x == 'YET TO START' or x == 'RUNNING':
				full_job_status = 'RUNNING'
				break
			elif x == 'FAIL':
				full_job_status = 'FAIL'

		context = {
		'job_name':job_name,
		'org_timestamp':org_timestamp,
		'display_timestamp':display_timestamp,
		'full_job_status': full_job_status,
		'job_testsuite_result': job_testsuite_result,
		'job_suite_selected': job_suite_selected,
		'job_testsuite_error': job_testsuite_error,
		'job_testcase_result': job_testcase_result,
		}
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		return render(request, self.template_name, context)	



class JobCompleted(View):
	template_name = 'job_completed.html'
	robot_data = GetRobotService().get_robot_service()
	
	def get(self, request, *args, **kwargs):
		
		all_jobs_data_service = self.robot_data.get_all_jobs()
		all_jobs_data = []
		count = 1
		for each_all_jobs_data in all_jobs_data_service:
			job_id = count
			org_timestamp = each_all_jobs_data['timestamp']
			display_timestamp = re.sub('[-]',':',each_all_jobs_data['timestamp'].split('.')[0])
			job_name = '-'.join(each_all_jobs_data['suite_names'])
			result = each_all_jobs_data['result']
			all_jobs_data.append((job_id,org_timestamp,display_timestamp,job_name,result))
			count += 1

		context = {
		'all_jobs_data': all_jobs_data
		}
		return render(request, self.template_name, context)


	def post(self, request, *args, **kwargs):
		return render(request, self.template_name, context)		

