import requests
import json
import time
import sys

# 定义时间格式
TIMEFORMAT = "%Y-%m-%d %H:%M:%S"


# 得到当前时间
def getNowTime():
    nowtime = time.strftime(TIMEFORMAT, time.localtime(time.time()))
    return nowtime


"""
	企业微信通道
"""


class SendWeChatMsg(object):

    def __init__(self):
        """
		初始化企业微信相关权限字段
		注:
		corpid是企业ID，获取路径，登录企业微信官网---我的企业---最底部可寻到
		corpsecret是自建应用的Secret
		agentid是自建应用的AgentId
		这两个参数在 应用管理---自建（新建一个应用）---进入此应用，正文顶部可寻到
		"""
        self.corpid = 'ww8fe691a21dcf15ae'
        self.corpsecret = 'IXDM1OJGwzT_Qwm2XAetogczUVKgYcKTm5tDEiWniMI'
        self.agentid = '1000137'

    def GetToken(self):
        """
		获取企企业微信应该的token
		"""
        if self.corpid is None or self.corpsecret is None:
            return False, '企业微信相关信息未配置'
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + self.corpid + '&corpsecret=' + self.corpsecret
        response = requests.get(url)
        res = response.json()
        self.token = res['access_token']
        print(self.token)
        return True, '企业微信token获取成功'

    def GetLoginUserId(self):
        _isOK, result = self.GetToken()
        if _isOK:
            url = 'https://qyapi.weixin.qq.com/cgi-bin/user/getuserid?access_token=' + self.token
            jsonmsg = {
                "mobile": "13581702404",
            }
            data = (bytes(json.dumps(jsonmsg), 'utf-8'))
            r = requests.post(url, data, verify=False)
            print(r.text)
        else:
            print(result)

    def CreateChat(self):
        _isOK, result = self.GetToken()
        if _isOK:
            url = 'https://qyapi.weixin.qq.com/cgi-bin/appchat/create?access_token=' + self.token
            jsonmsg = {
                "name": "JenkinsMsg",
                "owner": "it-bj@yingxiong.com",
                "userlist": ["zhibin.liu@yingxiong.com", "pengju.zhang@yingxiong.com", "ming.li01@yingxiong.com",
                             "che.sun@yingxiong.com", "zhou.liu@yingxiong.com"],
            }
            data = (bytes(json.dumps(jsonmsg), 'utf-8'))
            r = requests.post(url, data, verify=False)
            print(r.text)
        else:
            print(result)

    def SendMessage(self, msg):
        """
		发送消息方法
		msg:需要发送的消息
		"""
        _isOK, result = self.GetToken()
        if _isOK:
            url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.token
            jsonmsg = {
                # "touser" : "@all",
                "chatid": "",
                "msgtype": "text",
                "agentid": self.agentid,
                "text": {
                    "content": msg
                },
                "safe": 0
            }
            data = (bytes(json.dumps(jsonmsg), 'utf-8'))
            requests.post(url, data, verify=False)
        else:
            print(result)


"""
	Jenkins消息格式化
"""


class Jenkins(object):
    def __init__(self):
        self.wechatMsg = SendWeChatMsg()

    def SendMessage(self, title, job_name, branch, build_url, build_status):
        """
			格式化消息格式
		"""
        message = """
				{}
				---------------------------------
				构建信息
				---------------------------------
				{}
				---------------------------------
				状态：{}
				任务名：{}
				分支名：{}
				构建日志：{} console   
				---------------------------------  
				""".format(title, getNowTime(), build_status, job_name, branch, build_url, build_url)
        self.wechatMsg.SendMessage(message)


def call_jenkins(argv):
    """
		 发送jenkins编译消息给企业微信
		 参数:
					title 提醒标题
					jobname:Jenins任务名
					branch: 分支
					build_url: Jenins编译的url地址
					build_status: 构建的状态
	"""
    job_name = argv[2]
    branch = argv[3]
    build_url = argv[4]
    build_status = argv[5]
    jenkins = Jenkins()
    jenkins.SendMessage('---Jenkins 构建提醒----', job_name, branch, build_url, build_status)


if __name__ == "__main__":
    """
		sys.argv获取命令中的参数list
	"""
    if len(sys.argv) > 1:
        print(sys.argv)
        if sys.argv[1] == 'jenkins':
            print('--- jenkins')
            call_jenkins(sys.argv)
    else:
        print('usage:')
        print('测试Jenkins的命令“   python messagetoWechat.py jenkins ${JOB_NAME} ${GIT_BRANCH}  ${BUILD_URL} 构建成功')
