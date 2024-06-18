
import pyblish.api
import pyblish.lib


class CollectCurrentDate(pyblish.api.ContextPlugin):
    """Inject the current time into the Context"""

    order = pyblish.api.CollectorOrder
    label = "Current date"
    hosts = ['example']
    def process(self, context):
        context.data['date'] = pyblish.lib.time()
