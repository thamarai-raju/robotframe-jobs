# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import View
from lib.django.robot_execute import RobotExecute
import threading
import time
import re

class GetRobotService():

	def get_robot_service(self):
		return RobotExecute()

class JobScheduler(View):
	template_name = 'job_scheduler.html'
	robot_data = GetRobotService().get_robot_service()

	def get(self, request, *args, **kwargs):
		suite_info, job_group_info = self.robot_data.get_suiteinfo()

		#get all job groups
		job_group_info_view = job_group_info.keys()
		#add the full and custom to the above
		job_group_info_view.extend(['full','custom'])
		job_group_selected = 'sanity'
		job_run_list = None
		test_suite_list = None
		test_case_list = None
		
		context = {
		'job_groups': job_group_info_view,
		'job_group_selected': job_group_selected,
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
	
	def get(self, request, job_group_selected=None, *args, **kwargs):
		suite_info, job_group_info = self.robot_data.get_suiteinfo()

		#get all job groups
		job_group_info_view = job_group_info.keys()
		#add the full and custom to the above
		job_group_info_view.extend(['full','custom'])
		
		#get the list of suite names in the group
		job_run_list = job_group_info[job_group_selected].keys()
		# job_run_list = ['VPN', 'ROUTING']
			
		# job_run_list = None
		test_suite_list = None
		test_case_list = None
		
		
		context = {
		'job_groups': job_group_info_view,
		'job_group_selected': job_group_selected,
		'job_run_list': job_run_list,
		'test_suite_list': test_suite_list,
		'test_case_list': test_case_list
		}

		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		return render(request, self.template_name, {})		


class JobFeature(View):
	template_name = 'job_scheduler.html'
	robot_data = GetRobotService().get_robot_service()
	
	def get(self, request, job_group_selected=None, job_feature_selected=None, *args, **kwargs):
		suite_info, job_group_info = self.robot_data.get_suiteinfo()

		#get all job groups
		job_group_info_view = job_group_info.keys()
		#add the full and custom to the above
		job_group_info_view.extend(['full','custom'])
		
		#get the list of suite names in the group
		job_run_list = job_group_info[job_group_selected].keys()
		# job_run_list = ['VPN', 'ROUTING']
		
		#get the testsuite list
		test_suite_list = ['testsuite1','testsuite2']

		# job_run_list = None
		# test_suite_list = None
		test_case_list = None

		context = {
		'job_groups': job_group_info_view,
		'job_group_selected': job_group_selected,
		'job_run_list': job_run_list,
		'job_feature_selected': job_feature_selected,
		'test_suite_list': test_suite_list,
		'test_case_list': test_case_list
		}

		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		return render(request, self.template_name, {})		



class JobTestsuite(View):
	template_name = 'job_scheduler.html'
	robot_data = GetRobotService().get_robot_service()
	
	def get(self, request, job_group_selected=None, job_feature_selected=None,job_testsuite_selected=None, *args, **kwargs):
		suite_info, job_group_info = self.robot_data.get_suiteinfo()

		#get all job groups
		job_group_info_view = job_group_info.keys()
		#add the full and custom to the above
		job_group_info_view.extend(['full','custom'])
		
		#get the list of suite names in the group
		job_run_list = job_group_info[job_group_selected].keys()
		# job_run_list = ['VPN', 'ROUTING']
		
		#get the testsuite list
		test_suite_list = ['testsuite1','testsuite2']

		#get the testcase list
		test_case_list = ['testcase1', 'testcase2']

		context = {
		'job_groups': job_group_info_view,
		'job_group_selected': job_group_selected,
		'job_run_list': job_run_list,
		'job_feature_selected': job_feature_selected,
		'test_suite_list': test_suite_list,
		'job_testsuite_selected': job_testsuite_selected,
		'test_case_list': test_case_list
		}

		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		return render(request, self.template_name, {})		

class JobRobotRun(View):
	
	def get(self, request, job_group_selected=None, *args, **kwargs):
		return JobView().get(request, job_group_selected)	

	def post(self, request, *args, **kwargs):
		return render(request, self.template_name, {})		


class JobView(View):
	template_name = 'job_view.html'
	robot_data = GetRobotService().get_robot_service()
	
	def get(self, request, job_group_selected=None, time_stamp=None, *args, **kwargs):
		input_job_d = [
			{
				'testsuite_id':'1',
				'suite_name':'vpn_tests',
				# 'include_tags':[],
				'include_tags':['test1'],
				# 'exclude_tags':['test1','test2','test3','test4'],
				# 'exclude_tags':[],
				# 'testcases':['Verify SPOKE ANYNET per site'],
			},
			{
				'testsuite_id':'2',
				'suite_name':'route_manager_cli_tests',
				'include_tags':['sanity'],
				# 'exclude_tags':['sanity'],
				'testcases':[],
			},
			# {
			# 	'testsuite_id':'3',
			# 	'suite_name':'colgate',
			# 	'include_tags':[],
			# 	'exclude_tags':[],
			# 	'testcases':['Changes for colgate customer config'],
			# }
		]
		
		# self.robot_data.run_jobs(input_job_d)
		
		# download_thread = threading.Thread(target=self.robot_data.run_jobs, args=input_job_d)
		# download_thread.start()
		job_result_data_service = self.robot_data.get_status(time_stamp)
		#get suite name
		job_name = '-'.join(job_result_data_service.get('job_name'))
		#get teimstamp
		job_timestamp = job_result_data_service.get('timestamp')

		job_testsuite_result = []
		result_each_id = []
		for each_job_result_data in job_result_data_service['results']:
			testsuite_status = each_job_result_data.get('testsuite_status')
			testsuite_name = each_job_result_data.get('testsuite_name')
			if testsuite_status == 'RUNNING' or \
					testsuite_status == 'YET TO START':
				job_testsuite_result.append((testsuite_name,testsuite_status))
			else:
				job_testsuite_result.append((testsuite_name,
					each_job_result_data.get('testsuite_result')))
			testcases_list = each_job_result_data.get('testcases')
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

		job_testcase_result = None

		context = {
		'job_name':job_name,
		'job_timestamp':job_timestamp,
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
		job_timestamp = job_result_data_service.get('timestamp')

		job_testsuite_result = []
		job_testcase_result = []
		result_each_id = []
		for each_job_result_data in job_result_data_service['results']:
			testsuite_status = each_job_result_data.get('testsuite_status')
			testsuite_name = each_job_result_data.get('testsuite_name')
			if testsuite_status == 'RUNNING' or \
					testsuite_status == 'YET TO START':
				job_testsuite_result.append((testsuite_name,testsuite_status))
			else:
				job_testsuite_result.append((testsuite_name,
					each_job_result_data.get('testsuite_result')))
			testcases_list = each_job_result_data.get('testcases')
			if testsuite_name == job_suite_selected:
				for each_testcase_name in testcases_list:
					job_testcase_result.append((each_testcase_name['name'], each_testcase_name['testcase_result']))
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
		'job_timestamp':job_timestamp,
		'full_job_status': full_job_status,
		'job_testsuite_result': job_testsuite_result,
		'job_suite_selected': job_suite_selected,
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

