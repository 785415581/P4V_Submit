from AssetBrowser.publish_hooks.basePublish import BasePublish


class RigPublish(BasePublish):

    def publish(self):
        """Publish files from drag in widget files"""
        print('step publish class')