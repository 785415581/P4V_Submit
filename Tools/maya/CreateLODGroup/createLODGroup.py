import json

from PySide2 import QtWidgets
from PySide2.QtWidgets import QApplication
from PySide2 import QtCore
from Tools.maya.CreateLODGroup.UI_LODExportManage import Ui_MainWindow
import sys, os
import json
from enum import Enum, EnumMeta, unique

from maya import cmds


@unique
class NodeType(Enum):
    NodeDir = 0;
    NodeFile = 1

class ExportLOD(QtWidgets.QMainWindow):
    def __init__(self, parent=None, *args):
        super(ExportLOD, self).__init__(parent)
        self.MainUI = Ui_MainWindow()
        self.MainUI.setupUi(self)

        self.MainUI.stackedWidget.setCurrentIndex(0)
        self.Data = self.collectInfo()
        if not self.Data:
            self.MainUI.label_4.setText("None LOD Group")
            self.MainUI.treeWidget.setEnabled(False)
            self.MainUI.stackedWidget.setCurrentIndex(1)

        self.InitTreeView()
        self.MainUI.treeWidget.clicked.connect(self.SettingData)
        self.MainUI.comboBox.currentTextChanged.connect(self.ChangePlatform)
        self.MainUI.comboBox_2.currentTextChanged.connect(self.ChangeLevel)
        self.MainUI.pushButton.clicked.connect(self.SelectPath)
        self.MainUI.pushButton_2.clicked.connect(self.Export)

    def Export(self):
        from maya import cmds
        checked_items = []
        topLevel = self.MainUI.treeWidget.topLevelItemCount()
        for i in range(topLevel):
            TopItem = self.MainUI.treeWidget.topLevelItem(i)
            checked_items = self.get_checked_items(TopItem)
        cmds.select(checked_items)
        filePath = self.MainUI.lineEdit.text()
        if filePath:
            cmds.file(filePath, force=True, type="FBX export", es=True, esc=(self.python_export_callback, "TEMP_EXPORT"))
            cmds.confirmDialog(title="Info", message="Export Success", button=['OK'], defaultButton='OK',
                               cancelButton='OK',
                               icon='information')
        else:
            self.show_warning_dialog()

    def python_export_callback(self):
        """
    	Print all nodes to be exported and triangulate all mesh shapes.
    	"""
        lodGroups = cmds.ls(sl=1, type="lodGroup", long=True)
        lodDetail = {}
        for lodGroup in lodGroups:
            lodDetail[lodGroup] = {}
            if cmds.listRelatives(lodGroup):
                for lod in cmds.listRelatives(lodGroup):
                    lodDetail[lodGroup][lod] = {}
                    lodLongName = lodGroup + "|" + lod
                    lodDetail[lodGroup][lod]["name"] = lodLongName
                    shapes = self.get_shapes_from_group(lodLongName)
                    if shapes:
                        Result = cmds.polyEvaluate(shapes[0])
                        lodDetail[lodGroup][lod]["shapes"] = shapes
                        lodDetail[lodGroup][lod]["UVShell"] = Result.get("shell")
                        lodDetail[lodGroup][lod]["face"] = Result.get("face")
                        lodDetail[lodGroup][lod]["vertex"] = Result.get("vertex")
                        lodDetail[lodGroup][lod]["platform"] = "Mobile"
                        lodDetail[lodGroup][lod]["Level"] = lod
        filePath = self.MainUI.lineEdit.text()
        configPath = filePath.replace(".fbx", ".json")
        with open(configPath, "w") as fp:
            json.dump(lodDetail, fp, indent=4)
        from pprint import pprint
        pprint(lodDetail)

    def show_warning_dialog(self):
        title = "Warning!"
        message = "Export path is None"

        # 使用 cmds.confirmDialog() 创建弹窗警告
        result = cmds.confirmDialog(title=title, message=message, button=['OK'], defaultButton='OK', cancelButton='OK',
                                    icon='warning')

        # 处理用户响应（这里只有一个 OK 按钮）
        if result == 'OK':
            print("User acknowledged the warning!")


    def get_checked_items(self, parent_item):
        checked_items = []

        for index in range(parent_item.childCount()):
            child = parent_item.child(index)
            if child.checkState(0) == QtCore.Qt.Checked:
                checked_items.append(child.text(0))
            # Recursively check children
            checked_items.extend(self.get_checked_items(child))

        return checked_items
    def SelectPath(self):
        """
        Select export file path
        :return:
        """
        multipleFilters = "Fbx (*.fbx);;All Files (*.*)"
        file = cmds.fileDialog2(fileFilter=multipleFilters, dialogStyle=2)

        # 如果用户选择了文件夹，将路径显示在标签上
        if file:
            self.MainUI.lineEdit.setText(f"{file[0]}")

        else:
            self.MainUI.lineEdit.setText("")

    def ChangePlatform(self, text):
        item = self.MainUI.treeWidget.currentItem()
        Info = item.data(0, QtCore.Qt.UserRole)
        Info["platform"] = text
        item.setData(0, QtCore.Qt.UserRole, Info)
        # level = Info.get("Level")

    def ChangeLevel(self, text):
        item = self.MainUI.treeWidget.currentItem()
        Info = item.data(0, QtCore.Qt.UserRole)
        Info["Level"] = text
        item.setData(0, QtCore.Qt.UserRole, Info)

    def SettingData(self, QModeIndex):
        item = self.MainUI.treeWidget.currentItem()
        if item.data(1, QtCore.Qt.UserRole) == "child":
            self.MainUI.comboBox.setEnabled(True)
            self.MainUI.comboBox_2.setEnabled(True)
            Info = item.data(0, QtCore.Qt.UserRole)
            platform = Info.get("platform")
            level = Info.get("Level")
            self.MainUI.comboBox.setCurrentText(platform)
            self.MainUI.comboBox_2.setCurrentText(level)

        else:
            self.MainUI.comboBox.setEnabled(False)
            self.MainUI.comboBox_2.setEnabled(False)

    def InitTreeView(self):

        self.RootNode = QtWidgets.QTreeWidgetItem(self.MainUI.treeWidget, type=NodeType.NodeDir.value)
        self.RootNode.setText(0, "Outliner")
        self.RootNode.setData(1, QtCore.Qt.UserRole, "Parent")
        self.RootNode.setExpanded(True)
        for name, LodInfo in self.Data.items():
            ChildNode = QtWidgets.QTreeWidgetItem(self.RootNode, type=NodeType.NodeDir.value)
            ChildNode.setText(0, name)
            ChildNode.setData(0, QtCore.Qt.UserRole, LodInfo)
            ChildNode.setData(1, QtCore.Qt.UserRole, "Parent")
            ChildNode.setFlags(self.RootNode.flags() | QtCore.Qt.ItemIsUserCheckable)
            ChildNode.setCheckState(0, QtCore.Qt.Unchecked)
            ChildNode.setExpanded(True)
            self.BuildTreeLeaf(ChildNode, LodInfo)
        self.MainUI.treeWidget.addTopLevelItem(self.RootNode)

    def BuildTreeLeaf(self, Node, LodInfo):
        for name, Info in LodInfo.items():
            subNode = QtWidgets.QTreeWidgetItem(Node, type=NodeType.NodeDir.value)
            subNode.setText(0, name)
            subNode.setData(0, QtCore.Qt.UserRole, Info)
            subNode.setData(1, QtCore.Qt.UserRole, "child")

    def get_shapes_from_group(self, group_name):
        from maya import cmds

        # 检查输入的对象是否存在且是一个组
        if not cmds.objExists(group_name) or not cmds.nodeType(group_name) == "transform":
            cmds.error(f"{group_name} 不是一个有效的组节点")

        shapes = []

        # 获取组下面的所有子节点
        all_descendants = cmds.listRelatives(group_name, allDescendents=True, fullPath=True) or []

        for node in all_descendants:
            # 检查节点类型是否是shape类型
            if cmds.nodeType(node) in ["mesh", "nurbsCurve", "nurbsSurface", "subdiv"]:
                shapes.append(node)

        return shapes


    def get_face_count(self, object_name):
        from maya import cmds
        if not cmds.objExists(object_name):
            cmds.error(f"{object_name} 对象不存在")

        # 确保对象是多边形网格
        if cmds.nodeType(object_name) != "mesh":
            # 如果输入的是变换节点，获取其下面的shape节点
            shapes = cmds.listRelatives(object_name, shapes=True, fullPath=True)
            if shapes and cmds.nodeType(shapes[0]) == "mesh":
                object_name = shapes[0]
            else:
                cmds.error(f"{object_name} 不是一个多边形网格")

        # 使用 polyEvaluate 命令获取面的数量
        face_count = cmds.polyEvaluate(object_name, face=True)
        return face_count

    def collectInfo(self):
        from maya import cmds
        lodGroups = cmds.ls(type="lodGroup", long=True)
        lodDetail = {}
        for lodGroup in lodGroups:
            lodDetail[lodGroup] = {}
            if cmds.listRelatives(lodGroup):
                for lod in cmds.listRelatives(lodGroup):
                    lodDetail[lodGroup][lod] = {}
                    lodLongName = lodGroup + "|" + lod
                    lodDetail[lodGroup][lod]["name"] = lodLongName
                    shapes = self.get_shapes_from_group(lodLongName)
                    if shapes:
                        faces = self.get_face_count(shapes[0])
                        Result = cmds.polyEvaluate(shapes[0])
                        lodDetail[lodGroup][lod]["shapes"] = shapes
                        lodDetail[lodGroup][lod]["UVShell"] = Result.get("shell")
                        lodDetail[lodGroup][lod]["face"] = Result.get("face")
                        lodDetail[lodGroup][lod]["vertex"] = Result.get("vertex")
                        lodDetail[lodGroup][lod]["platform"] = "Mobile"
                        lodDetail[lodGroup][lod]["Level"] = lod
        return lodDetail


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = ExportLOD()
    myapp.show()
    sys.exit(app.exec_())