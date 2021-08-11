
class Leaf(object):
    def __init__(self, name, value="0"):
        self.name = name
        self.value = value
        self.children = []

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

    def add_child(self, node):
        self.children.append(node)

    def set_value(self, value):
        self.value = value

    def to_json(self):
        res = dict()
        res['value'] = self.value
        res['name'] = self.name
        res['children'] = []
        for child in self.children:
            res['children'].append(child.to_json())
        return res