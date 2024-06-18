import pyblish.api
# class FirstPlugin(pyblish.api.ContextPlugin):
#   """Inject the current workspace into context"""
#
#   order = pyblish.api.CollectorOrder - 0.5
#   label = "My First outside plugin"
#
#   hosts = ['maya']
#   version = (0, 1, 0)
#
#   def process(self, context):
#     print("hello")
#
# class SecondPlugin(pyblish.api.ContextPlugin):
#   order = 1
#
#   def process(self, context):
#     print("world")
