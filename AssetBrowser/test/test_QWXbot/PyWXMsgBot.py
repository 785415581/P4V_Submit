import requests
import json
import time
import sys

#定义时间格式
TIMEFORMAT = "%Y-%m-%d %H:%M:%S"
 
#得到当前时间
def getNowTime():
	nowtime = time.strftime(TIMEFORMAT, time.localtime(time.time()))
	return nowtime

def get_error_log(job_name):
	error_log = ""
	#todo wait to change
	return error_log
	try:
		import os
		import sys
		os.system('net use \\\\10.0.200.5\HeroFileServer "ZQcPE3QrDCYA4aE&" /user:YXHY\JgProPack')
		sys.path.append("\\\\10.0.200.5\HeroFileServer\ProjectX\Scripts\Python37\Lib\site-packages")
		import jenkins
		import re
		IP = 'http://10.0.11.152:8080/'
		USERNAME = "root"
		PASSWORD = "123"

		server = jenkins.Jenkins(IP, USERNAME, PASSWORD)
		last_number = server.get_job_info(job_name)['lastBuild']['number']
		log_str = server.get_build_console_output(job_name, last_number)

		lines = log_str.split("\n")
		for line in lines:
			re_com = re.compile(r'C:.+ line.+|.+ error.+|.+ Error.+|.+ failed.+|.+ ERROR.+|.+ missing.+')
			matchs = re_com.match(line)
			if matchs:
				error_log +=line
		return error_log

	except Exception as e:
		print(e)
		return error_log
 
def SendMessageByBot(msg, url):

	jsonmsg = {
				"msgtype" : "markdown",
				"markdown" : {
					"content" : msg
				},
			}
	data = (bytes(json.dumps(jsonmsg), 'utf-8'))
	requests.packages.urllib3.disable_warnings()
	resp = requests.post(url, data, verify=False)
	print(resp.text)


def call_jenkins(argv):
	title = argv[1]
	job_name = argv[2]
	branch = argv[3]
	build_url = argv[4]
	build_status = argv[5]
	wx_log = argv[6]

    ################## Set wx Robot ########################
	wx_robot1 = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=28db8e6c-ecfe-4eb7-9dd6-2e16dd48ae7e"
	wx_robot2 = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=518cb04d-1665-4968-aff8-02c2eef3e040"
	send_robot = wx_robot1
	url_dict = {
		wx_robot2: ["Checker/ProjectX_UE5CompileCheck"]
	}
	for bot_name, jobs in url_dict.items():
		if job_name in jobs:
			send_robot = bot_name

    ################# Set message #################################
	alert = '<font color="comment">{}</font>'.format(build_status)
	if build_status.find('ucc') == -1:
		alert = '<font color="red">{}</font>'.format(build_status)
	#error_log = get_error_log(job_name)
	message = """
				---------------------------------
				{}
				---------------------------------
				{}
				---------------------------------
				状态：<font color="info">{}</font>
				任务名：{}
				分支名：{}

				构建日志：[{}]({}//console)
				错误信息：{}
				---------------------------------  
				""".format(title, getNowTime(), alert, job_name, branch, build_url, build_url, wx_log)

	SendMessageByBot(message, send_robot)
 
 
if __name__ == "__main__":
	#sys.argv获取命令中的参数list
	if len(sys.argv) > 1:
		print(sys.argv)
		call_jenkins(sys.argv)