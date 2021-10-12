
class Leaf(object):
    def __init__(self, name, value="0"):
        self.name = name
        self.value = value
        self.fullPath = ''
        self.children = []
        self.ser_ver = None
        self.local_ver = None

    def search(self, node):
        if self.name == node.name:
            return self
        if not self.children:
            return None
        else:
            for child in self.children:
                child_res = child.search(node)
                if child_res:
                    return child_res
            return None

    def set_ser_ver(self, version):
        self.ser_ver = version

    def set_local_ver(self, version):
        self.local_ver = version

    def add_child(self, node):
        self.children.append(node)

    def set_value(self, value):
        self.value = value

    def set_fullPath(self, value):
        self.fullPath = value

    def to_json(self):
        res = dict()
        res['value'] = self.value
        res['name'] = self.name
        res['path'] = self.fullPath
        res["ser_ver"] = self.ser_ver
        res["local_ver"] = self.local_ver
        res['children'] = []
        for child in self.children:
            res['children'].append(child.to_json())
        return res