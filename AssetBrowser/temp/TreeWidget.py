# import re
# import os
# import sys
# import subprocess
# from PySide2 import QtWidgets
# from PySide2 import QtGui
# from PySide2 import QtCore
# from P4 import P4
#
#
#
# class MainWindow(QtWidgets.QWidget):
#     def __init__(self):
#         super(MainWindow, self).__init__()
#         self.treeWidget = QtWidgets.QTreeWidget()
#         self.buildBtn = QtWidgets.QPushButton('Push')
#         self.Vlay = QtWidgets.QVBoxLayout()
#         self.Vlay.addWidget(self.treeWidget)
#         self.Vlay.addWidget(self.buildBtn)
#         self.setLayout(self.Vlay)
#         self.buildBtn.clicked.connect(self.buildTree)
#
#     def buildTree(self):
#
#         first_no = 10  # 一集目录从10开始,二级目录为对应的一级目录*100开始,三级四季依次类推
#         import subprocess
#         root = "//Assets/main/Character"
#         cmd_files = 'p4 files -i ' + root + '...'
#         res_files = subprocess.getoutput(cmd_files)
#         process = subprocess.Popen('p4 files //Assets/main/Character/...', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#         res_files, err = process.communicate()
#         print(out)
#         res_files = res_files.split('\n')
#
#         root_node = Node(root)  # 根节点
#         for res in res_files:
#             if re.findall(r'#\d+(.*?)delete(.*?)[)]', res):
#                 continue
#             out = res.split(root)[-1].split('/')
#             temp = list()
#             index = str()
#             for level in range(len(out)):
#                 if out[level]:
#                     if level == 0:
#                         index = out[level]
#                         temp.append(index)
#                     else:
#                         index = index + '/' + out[level]
#                         temp.append(index)
#             lines = temp
#             first_node = Node(lines[0])
#             if first_node.name not in [child.name for child in root_node.children]:
#                 first_node.set_value(str(first_no))
#                 first_no = first_no + 1
#                 root_node.add_child(first_node)
#
#             cur_node = root_node.search(first_node)
#             for node in [Node(name=lines[tmp]) for tmp in range(1, len(lines))]:  # 二级以后直接根据一级目录的编号开始
#                 if node.name not in [child.name for child in cur_node.children]:
#                     length = len(cur_node.children)
#                     node.set_value(str(length + 100 * int(cur_node.value)))
#                     cur_node.add_child(node)
#                 cur_node = root_node.search(node)
#         data = root_node.to_json()
#         with open('./temp.json', 'w') as fp:
#             import json
#             jsonData = json.dumps(data, indent=2)
#             fp.write(jsonData)
#             fp.close()
#         rootItem = QtWidgets.QTreeWidgetItem(self.treeWidget)
#         rootItem.setText(0, os.path.basename(root))
#         self.setTree(rootItem, data)
#
#     def setTree(self, leaf, leafName):
#         if leafName['children']:
#             for child in leafName['children']:
#                 child_root = QtWidgets.QTreeWidgetItem(leaf)
#                 child_root.setText(0, os.path.basename(child['name']))
#                 self.setTree(child_root, child)
#
#
# class Node(object):
#     def __init__(self, name, value="0"):
#         self.name = name
#         self.value = value
#         self.children = []
#
#     def search(self, node):
#         if self.name == node.name:
#             return self
#         if not self.children:
#             return None
#         else:
#             for child in self.children:
#                 child_res = child.search(node)
#                 if child_res:
#                     return child_res
#             return None
#
#     def add_child(self, node):
#         self.children.append(node)
#
#     def set_value(self, value):
#         self.value = value
#
#     def to_json(self):
#         res = dict()
#         res['value'] = self.value
#         res['name'] = self.name
#         res['children'] = []
#         for child in self.children:
#             res['children'].append(child.to_json())
#         return res
#
#
# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     app.exec_()
