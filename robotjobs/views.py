# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import View
from lib.django.robot_execute import *
from celery.decorators import task

from robot_model_write import load_testdata_to_db
from .models import *
import threading
import time
import re



from robot import run as robot_run_custom
import re
import os
import sys
from pprint import pprint
import pdb
import glob
import socket
from datetime import datetime
import json
from celery.decorators import task
import time

@task(name="justsleeps")
def letswaitalot(t):
    time.sleep(t)
    print("yoooooo")
    with open('myfile.txt', 'w') as fp:
        pass


@task(name="views.run_jobs")
def run_jobs(input_job_d):
	'''
	'''
	time.sleep(10)
	# robot_suites_path = '/home/ubuntu/roboframe/tests'
	# django_log_path = '/home/ubuntu/roboframe/tests/django_logs/'

	# log_folder_name = django_log_path+'robot_log_files'
	# jobs_list_file =  'jobs_list'
	# apache_robot_folder = 'roboframe'
	# jobs_list_file_path = log_folder_name +'/'+ jobs_list_file


	# print('INSIDE FUNCTION')
	# print(robot_suites_path)

	# # #delete all existing log files
	# # log_fileList = glob.glob(self.log_folder_name+'/*')
	# # # Iterate over the list of filepaths & remove each file.
	# # for each_file in log_fileList:
	# #     try:
	# #         os.remove(each_file)
	# #     except:
	# #         print("Error while deleting file : ", each_file)

	# #creating a timestamp folder for this run
	# timestamp = re.sub('[:]', '-', re.sub('[ ]', '_', str(datetime.now())))
	# current_log_folder_name = log_folder_name +'/'+ timestamp
	# os.mkdir(current_log_folder_name)


	# #add the current run to the list of executed jobs 
	# if os.path.exists(jobs_list_file_path):
	# 	with open(jobs_list_file_path) as jobs_list_file_io: 
	# 		jobs_list_data = json.load(jobs_list_file_io)
	# else:
	# 	jobs_list_data = []

	# jobs_list_data.append({
	# 		'testsuite_id_l' : [x.get('testsuite_id') for x in input_job_d],
	# 		'timestamp' : timestamp,
	# 		'suite_names' : [x.get('suite_name') for x in input_job_d],
	# 	})
	# with open(jobs_list_file_path, 'w') as jobs_list_file_io:
	# 		json.dump(jobs_list_data, jobs_list_file_io)


	# #run the robot script
	# for each_input_job in input_job_d:

	# 	id = each_input_job.get('testsuite_id')
	# 	suite_name = each_input_job.get('suite_name')
	# 	testcases = each_input_job.get('testcases',[])
	# 	include_tags = each_input_job.get('include_tags',[])
	# 	exclude_tags = each_input_job.get('exclude_tags',[])
	# 	status_file = current_log_folder_name+'/'+id+'_status.txt'
	# 	console_log_file = current_log_folder_name+'/'+id+'_console_log.txt'
	# 	console_err_file = current_log_folder_name+'/'+id+'_console_err.txt'

	# 	with open(status_file, 'w+') as statusFile:
	# 		statusFile.write('RUNNING')
	# 	try:
	# 		logFile = open(console_log_file, 'w+')
	# 		logErrFile = open(console_err_file, 'w+')
	# 		log = robot_run_custom.run(robot_suites_path, stdout=logFile,stderr=logErrFile, suite=suite_name, test=testcases,
	# 			include=include_tags, exclude=exclude_tags,
	# 			variable=['testbed_name:scale/scale','scale_tb_num:1', 'duts_list:none'],splitlog=True,
	# 			log=id+'_log.html', report=id+'_report.html', output=id+'_output.xml', outputdir=current_log_folder_name)
	# 		logErrFile.close()
	# 		logFile.close()
	# 	except Exception as e:
	# 		print(e)
	# 		with open(status_file, 'w+') as statusFile:
	# 			statusFile.write('ERROR')
	# 	with open(status_file, 'w+') as statusFile:
	# 		statusFile.write('COMPLETED')
		


class GetRobotService():

	def get_robot_service(self):
		return RobotExecute()


class GetModelInfo():

	def get_feature_by_tag(self, group_name):
		print(group_name)
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

class JobScheduler(View):
	template_name = 'job_scheduler.html'
	robot_data = GetRobotService().get_robot_service()

	def get(self, request, *args, **kwargs):


		#only when a update is needed
		# load_testdata_to_db()
		letswaitalot.delay(5)
		print('escape')

		#add the full and custom to the above
		job_group_info_view = ['Sanity','Intermediate','Full','Custom']
		# job_group_selected = 'Sanity'
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
		job_group_info_view = ['Sanity','Intermediate','Full','Custom']
		
		#get the list of suite names in the group
		job_run_list = self.get_model_info.get_feature_by_tag(job_group_selected)
		print(job_run_list)


		if job_group_selected != 'Custom':
			job_feature_selected = job_run_list[0]
		else:
			job_feature_selected = None

		test_suite_list = self.get_model_info.get_testsuites_by_feature(job_group_selected, job_feature_selected)
		if job_group_selected != 'Custom':
			job_testsuite_selected = test_suite_list[0]
		else:
			job_testsuite_selected = None
		test_case_list = self.get_model_info.get_testcases_by_testsuite(job_group_selected, job_feature_selected,
								job_testsuite_selected)

		
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


class JobFeature(View):
	template_name = 'job_scheduler.html'
	robot_data = GetRobotService().get_robot_service()
	get_model_info = GetModelInfo()

	def get(self, request, job_group_selected=None, job_feature_selected=None, *args, **kwargs):
		# suite_info, job_group_info = self.robot_data.get_suiteinfo()

		# #get all job groups
		# job_group_info_view = job_group_info.keys()
		#add the full and custom to the above
		job_group_info_view = ['Sanity','Intermediate','Full','Custom']
		
		#get the list of suite names in the group
		job_run_list = self.get_model_info.get_feature_by_tag(job_group_selected)
		
		test_suite_list = self.get_model_info.get_testsuites_by_feature(job_group_selected, job_feature_selected)
		if job_group_selected != 'Custom':
			job_testsuite_selected = test_suite_list[0]
		else:
			job_testsuite_selected = None
		test_case_list = self.get_model_info.get_testcases_by_testsuite(job_group_selected, job_feature_selected,
								job_testsuite_selected)

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



class JobTestsuite(View):
	template_name = 'job_scheduler.html'
	robot_data = GetRobotService().get_robot_service()
	get_model_info = GetModelInfo()

	def get(self, request, job_group_selected=None, job_feature_selected=None,job_testsuite_selected=None, *args, **kwargs):

		#add the full and custom to the above
		job_group_info_view = ['Sanity','Intermediate','Full','Custom']
		
		#get the list of suite names in the group
		job_run_list = self.get_model_info.get_feature_by_tag(job_group_selected)
		test_suite_list = self.get_model_info.get_testsuites_by_feature(job_group_selected, job_feature_selected)
		test_case_list = self.get_model_info.get_testcases_by_testsuite(job_group_selected, job_feature_selected,
								job_testsuite_selected)

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
	robot_service_data = GetRobotService()
	robot_data = robot_service_data.get_robot_service()
	
	get_model_info = GetModelInfo()

	def get(self, request, job_group_selected=None, time_stamp=None, *args, **kwargs):

		if job_group_selected:
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
					'include_tags':['Sanity'],
					# 'exclude_tags':['Sanity'],
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
			job_testsuite_list = self.get_model_info.get_testsuite_by_tag(job_group_selected)
			input_job_d = []
			count =1
			include_tags = [job_group_selected] if job_group_selected != 'Full' else []
			for each_job_testsuite in job_testsuite_list:
				each_input_job_d = {
						'testsuite_id': str(count),
						'suite_name': each_job_testsuite,
						'include_tags': include_tags
					}
				count += 1
				input_job_d.append(each_input_job_d)

			# @task(name="justsleeps")
			# def temp1():
			# 	time.sleep(10)

			
			print('STARTED')
			print(input_job_d)
			# run_jobs.delay(input_job_d)

			# run_jobs(input_job_d)
			
			# temp1.delay()
			print('END')
		
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
			testsuite_error = each_job_result_data.get('error')
			testcases_list = each_job_result_data.get('testcases',[])
			if not testsuite_error:
				if testsuite_status == 'RUNNING' or \
						testsuite_status == 'YET TO START':
					job_testsuite_result.append((testsuite_name,testsuite_status))
				else:
					job_testsuite_result.append((testsuite_name,
						each_job_result_data.get('testsuite_result')))
			else:
				job_testsuite_result.append((testsuite_name,'Error'))
			if testcases_list:
				for each_testcase_name in testcases_list:
						result_each_id.append(each_testcase_name['testcase_result'])
			else:
				result_each_id.append('ERROR')

		print(result_each_id)
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
		job_testsuite_error = ''
		for each_job_result_data in job_result_data_service['results']:
			testsuite_status = each_job_result_data.get('testsuite_status')
			testsuite_name = each_job_result_data.get('testsuite_name')
			testsuite_error = each_job_result_data.get('error')
			testcases_list = each_job_result_data.get('testcases',[])
			if not testsuite_error:
				if testsuite_status == 'RUNNING' or \
						testsuite_status == 'YET TO START':
					job_testsuite_result.append((testsuite_name,testsuite_status))
				else:
					job_testsuite_result.append((testsuite_name,
						each_job_result_data.get('testsuite_result')))
				if testsuite_name == job_suite_selected:
					for each_testcase_name in testcases_list:
						job_testcase_result.append((each_testcase_name['name'], each_testcase_name['testcase_result']))
			else:
				job_testsuite_result.append((testsuite_name,'Error'))
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
		'job_timestamp':job_timestamp,
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

