import json

from PySide2 import QtWidgets
from PySide2.QtWidgets import QApplication
from PySide2 import QtCore
from Tools.maya.CreateLODGroup.UI_LODExportManage import Ui_MainWindow
import sys, os
import json
from enum import Enum, EnumMeta, unique
from functools import partial
from pprint import pprint

# from maya import cmds

DEBUG = False

DataBase = {'|LOD_Group_1': {'Check': 'UnCheck',
                  'LOD_0': {'Level': 'LOD_0',
                            'UVShell': 1,
                            'face': 400,
                            'index': 0,
                            'longName': '|LOD_Group_1|LOD_0',
                            'name': '|LOD_Group_1|LOD_0',
                            'parentGroup': '|LOD_Group_1',
                            'platform': 'Mobile',
                            'shapes': ['|LOD_Group_1|LOD_0|pSphere1|pSphereShape1'],
                            'shortName': 'LOD_0',
                            'vertex': 382},
                  'LOD_1': {'Level': 'LOD_1',
                            'UVShell': 1,
                            'face': 260,
                            'index': 1,
                            'longName': '|LOD_Group_1|LOD_1',
                            'name': '|LOD_Group_1|LOD_1',
                            'parentGroup': '|LOD_Group_1',
                            'platform': 'HD_PC',
                            'shapes': ['|LOD_Group_1|LOD_1|pSphere1|pSphereShape1',
                                       '|LOD_Group_1|LOD_1|pSphere1|polySurfaceShape1'],
                            'shortName': 'LOD_1',
                            'vertex': 242},
                  'LOD_2': {'Level': 'LOD_2',
                            'UVShell': 1,
                            'face': 180,
                            'index': 2,
                            'longName': '|LOD_Group_1|LOD_2',
                            'name': '|LOD_Group_1|LOD_2',
                            'parentGroup': '|LOD_Group_1',
                            'platform': 'Mobile',
                            'shapes': ['|LOD_Group_1|LOD_2|pSphere1|pSphereShape1',
                                       '|LOD_Group_1|LOD_2|pSphere1|polySurfaceShape2'],
                            'shortName': 'LOD_2',
                            'vertex': 162}},
 '|LOD_Group_2': {'Check': 'UnCheck',
                  'LOD_0': {'Level': 'LOD_0',
                            'UVShell': 1,
                            'face': 400,
                            'index': 0,
                            'longName': '|LOD_Group_2|LOD_0',
                            'name': '|LOD_Group_2|LOD_0',
                            'parentGroup': '|LOD_Group_2',
                            'platform': 'Mobile',
                            'shapes': ['|LOD_Group_2|LOD_0|pSphere2|pSphereShape2'],
                            'shortName': 'LOD_0',
                            'vertex': 382},
                  'LOD_1': {'Level': 'LOD_1',
                            'UVShell': 1,
                            'face': 260,
                            'index': 1,
                            'longName': '|LOD_Group_2|LOD_1',
                            'name': '|LOD_Group_2|LOD_1',
                            'parentGroup': '|LOD_Group_2',
                            'platform': 'HD_PC',
                            'shapes': ['|LOD_Group_2|LOD_1|pSphere2|pSphereShape2',
                                       '|LOD_Group_2|LOD_1|pSphere2|polySurfaceShape3'],
                            'shortName': 'LOD_1',
                            'vertex': 242},
                  'LOD_2': {'Level': 'LOD_2',
                            'UVShell': 1,
                            'face': 180,
                            'index': 2,
                            'longName': '|LOD_Group_2|LOD_2',
                            'name': '|LOD_Group_2|LOD_2',
                            'parentGroup': '|LOD_Group_2',
                            'platform': 'Mobile',
                            'shapes': ['|LOD_Group_2|LOD_2|pSphere2|pSphereShape2',
                                       '|LOD_Group_2|LOD_2|pSphere2|polySurfaceShape4'],
                            'shortName': 'LOD_2',
                            'vertex': 162}}}

@unique
class NodeType(Enum):
    NodeDir = 0;
    NodeFile = 1


class ExportLOD(QtWidgets.QMainWindow):
    """
    LOD 导出工具
    """

    def __init__(self, parent=None, *args):
        super(ExportLOD, self).__init__(parent)
        # 初始化界面
        self.MainUI = Ui_MainWindow()
        self.MainUI.setupUi(self)
        if DEBUG:
            self.setWindowTitle("LOD Export - Debug")
            self.AllLODItems = DataBase
        else:
            self.setWindowTitle("LOD Export")
            # 获取场景中的所有LOD 信息，给后面的界面填充数据
            self.AllLODItems = self.CollectLodInfo()
        self.MainUI.stackedWidget.setCurrentIndex(0)
        if not self.AllLODItems:
            self.MainUI.label_4.setText("None LOD Group")
            self.MainUI.treeWidget.setEnabled(False)
            self.MainUI.stackedWidget.setCurrentIndex(1)

        # 初始化树界面
        self.InitTreeView()

        # 注册声明信号
        self.MainUI.treeWidget.clicked.connect(self.SettingData)
        self.MainUI.treeWidget.itemChanged.connect(self.TreeItemChanged)
        self.MainUI.comboBox.currentTextChanged.connect(self.ChangePlatform)
        self.MainUI.comboBox_2.currentTextChanged.connect(self.ChangeLevel)
        self.MainUI.pushButton.clicked.connect(self.SelectPath)
        self.MainUI.pushButton_3.clicked.connect(self.Refresh)
        self.MainUI.pushButton_2.clicked.connect(self.Export)

    def Refresh(self):
        """ 刷新当前Lod信息 """
        self.RebuildTreeView()

    def TreeItemChanged(self, item, column):
        """ 树节点改变时 """
        if item.data(1, QtCore.Qt.UserRole) == "Parent":
            if item.checkState(column) == QtCore.Qt.Checked:
                self.AllLODItems[item.text(column)]["Check"] = "Check"
            else:
                self.AllLODItems[item.text(column)]["Check"] = "Uncheck"

    # def RegisterEventCallBack(self):
    #     """ 注册回调"""
    #     import maya.api.OpenMaya as om
    #     callBackID = om.MEventMessage.addEventCallback("DagObjectCreated", self.OnDagObejctCreated)
    #     return callBackID

    def Export(self):
        """ 导出LOD 数据 """

        pprint(self.AllLODItems)
        from maya import cmds
        checked_items = []
        topLevel = self.MainUI.treeWidget.topLevelItemCount()
        for i in range(topLevel):
            TopItem = self.MainUI.treeWidget.topLevelItem(i)
            checked_items = self.GetCheckedItems(TopItem)
        cmds.select(checked_items)
        filePath = self.MainUI.lineEdit.text()
        if filePath:
            cmds.file(filePath, force=True, type="FBX export", es=True, esc=(self.PythonExportCallback, "TEMP_EXPORT"))
            cmds.confirmDialog(title="Info", message="Export Success", button=['OK'], defaultButton='OK',
                               cancelButton='OK',
                               icon='information')
        else:
            self.ShowWarningDialog()

    def PythonExportCallback(self):
        """Maya 的callback 输出json信息 """
        lodDetail = self.AllLODItems
        filePath = self.MainUI.lineEdit.text()
        configPath = filePath.replace(".fbx", ".json")
        with open(configPath, "w") as fp:
            json.dump(lodDetail, fp, indent=4)
        from pprint import pprint
        pprint(lodDetail)

    def ShowWarningDialog(self):
        """ 显示警告弹窗 """
        title = "Warning!"
        message = "Export path is None"

        # 使用 cmds.confirmDialog() 创建弹窗警告
        result = cmds.confirmDialog(title=title, message=message, button=['OK'], defaultButton='OK', cancelButton='OK',
                                    icon='warning')

        # 处理用户响应（这里只有一个 OK 按钮）
        if result == 'OK':
            print("User acknowledged the warning!")

    def GetCheckedItems(self, parent_item):
        """ 获取所有选中的节点 """
        checked_items = []

        for index in range(parent_item.childCount()):
            child = parent_item.child(index)
            if child.checkState(0) == QtCore.Qt.Checked:
                checked_items.append(child.text(0))
            # Recursively check children
            checked_items.extend(self.GetCheckedItems(child))

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
        """改变LOD的平台设置"""
        item = self.MainUI.treeWidget.currentItem()
        Info = item.data(0, QtCore.Qt.UserRole)
        Info["platform"] = text
        item.setData(0, QtCore.Qt.UserRole, Info)
        Name = Info.get("shortName")
        self.AllLODItems[item.parent().text(0)][Name]["platform"] = text
        if text == "HD_PC":
            ItemWidget = self.MainUI.treeWidget.itemWidget(item, 0)
            ItemWidget.label.setStyleSheet("background-color: #2ecc71;")
        elif text == "Mobile":
            ItemWidget = self.MainUI.treeWidget.itemWidget(item, 0)
            ItemWidget.label.setStyleSheet("background-color: rgb(60, 63, 65);")

    def ChangeLevel(self, text):
        """ 改变Lod 的Level 层级"""
        item = self.MainUI.treeWidget.currentItem()
        Info = item.data(0, QtCore.Qt.UserRole)
        Info["Level"] = text
        item.setData(0, QtCore.Qt.UserRole, Info)
        Name = Info.get("shortName")
        self.AllLODItems[item.parent().text(0)][Name]["Level"] = text

    def SettingData(self, QModeIndex):
        """ 选择Item 改变当前设置 """

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
        """初始化树状结构"""
        self.MainUI.treeWidget.clear()
        self.RootNode = QtWidgets.QTreeWidgetItem(self.MainUI.treeWidget, type=NodeType.NodeDir.value)
        self.RootNode.setText(0, "Outliner")
        self.RootNode.setData(1, QtCore.Qt.UserRole, "Outliner")
        self.RootNode.setExpanded(True)
        for name, LodInfo in self.AllLODItems.items():
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
        """创建叶子节点 """
        for name, Info in LodInfo.items():
            if isinstance(Info, dict):
                subNode = QtWidgets.QTreeWidgetItem(Node, type=NodeType.NodeDir.value)
                ItemWidget = TreeWidgetItemWidget(name)
                self.MainUI.treeWidget.setItemWidget(subNode, 0, ItemWidget)
                subNode.setData(0, QtCore.Qt.UserRole, Info)
                subNode.setData(1, QtCore.Qt.UserRole, "child")
                self.MainUI.comboBox.setCurrentText(LodInfo.get("platform"))
                self.MainUI.comboBox_2.setCurrentText(LodInfo.get("Level"))
                ItemWidget.button.clicked.connect(partial(self.PreviewLod, subNode, ItemWidget, Node))
            elif isinstance(Info, str):
                if Info == "Check":
                    Node.setCheckState(0, QtCore.Qt.Checked)
                else:
                    Node.setCheckState(0, QtCore.Qt.Unchecked)

    def PreviewLod(self, subNode, ItemWidget, Node):
        """ 预览Lod 的不同层级 """
        if ItemWidget.isPreview:
            ItemWidget.button.setStyleSheet("background-color: rgb(60, 63, 65);")
            ItemWidget.isPreview = False
            self.ChangeLodDisplayWay(subNode, ItemWidget, Node)
        else:
            ItemWidget.button.setStyleSheet("background-color: #e74c3c;")
            ItemWidget.isPreview = True
            self.ChangeLodDisplayWay(subNode, ItemWidget, Node)

    def ChangeLodDisplayWay(self, subNode, ItemWidget, Node):
        """  改变Lod 组的不同级别进行显示方式设置"""
        from maya import cmds as cmds
        LodInfo = subNode.data(0, QtCore.Qt.UserRole)
        parentGroup = LodInfo.get("parentGroup")
        if ItemWidget.isPreview:
            for lod in enumerate(cmds.listRelatives(parentGroup)):
                print(lod[1], "------------>", LodInfo.get("shortName"))
                if lod[1] == LodInfo.get("shortName"):
                    cmds.setAttr(parentGroup + ".displayLevel[" + str(lod[0]) + "]", 1)
                else:
                    cmds.setAttr(parentGroup + ".displayLevel[" + str(lod[0]) + "]", 2)
        else:
            for lod in enumerate(cmds.listRelatives(parentGroup)):
                cmds.setAttr(parentGroup + ".displayLevel[" + str(lod[0]) + "]", 0)

    def RebuildTreeView(self):
        """ 清除之前的Tree， 重新创建Tree， 因为有数据更新，创建出来的Tree要记录上次的设置信息"""
        self.MainUI.treeWidget.clear()
        # 暂时停止信号， 在写入Data 的时候userRole数据会发生信号传递
        self.MainUI.treeWidget.itemChanged.disconnect(self.TreeItemChanged)
        self.RootNode = QtWidgets.QTreeWidgetItem(self.MainUI.treeWidget, type=NodeType.NodeDir.value)
        self.RootNode.setText(0, "Outliner")
        self.RootNode.setData(1, QtCore.Qt.UserRole, "Parent")
        self.RootNode.setExpanded(True)
        if DEBUG:
            self.AllLODItems = self.AllLODItems
        else:
            self.AllLODItems = self.ReCollectLodInfo()
        for name, LodInfo in self.AllLODItems.items():
            ChildNode = QtWidgets.QTreeWidgetItem(self.RootNode, type=NodeType.NodeDir.value)
            ChildNode.setText(0, name)
            ChildNode.setData(0, QtCore.Qt.UserRole, LodInfo)
            ChildNode.setData(1, QtCore.Qt.UserRole, "Parent")
            ChildNode.setFlags(self.RootNode.flags() | QtCore.Qt.ItemIsUserCheckable)
            ChildNode.setExpanded(True)
            self.BuildTreeLeaf(ChildNode, LodInfo)

        self.MainUI.treeWidget.addTopLevelItem(self.RootNode)
        # 恢复信号传递
        self.MainUI.treeWidget.itemChanged.connect(self.TreeItemChanged)

    def ReCollectLodInfo(self):
        """ 重新组织Lod 信息， 为后面的输出做准备"""
        lodGroups = cmds.ls(type="lodGroup", long=True)
        lodDetail = self.AllLODItems
        for lodGroup in lodGroups:
            # 添加新的Lod节点信息
            if lodGroup not in self.AllLODItems:
                lodDetail[lodGroup] = {}
                lodDetail[lodGroup]["Check"] = "UnCheck"
                if cmds.listRelatives(lodGroup):
                    index = 0
                    for lod in cmds.listRelatives(lodGroup):
                        lodDetail[lodGroup][lod] = {}
                        lodLongName = lodGroup + "|" + lod
                        shapes = self.GetShapeFromGroup(lodLongName)
                        if shapes:
                            Result = cmds.polyEvaluate(shapes[0])
                            lodDetail[lodGroup][lod]["shortName"] = lod
                            lodDetail[lodGroup][lod]["longName"] = lodLongName
                            lodDetail[lodGroup][lod]["index"] = index
                            lodDetail[lodGroup][lod]["shapes"] = shapes
                            lodDetail[lodGroup][lod]["UVShell"] = Result.get("shell")
                            lodDetail[lodGroup][lod]["face"] = Result.get("face")
                            lodDetail[lodGroup][lod]["vertex"] = Result.get("vertex")
                            lodDetail[lodGroup][lod]["platform"] = "Mobile"
                            lodDetail[lodGroup][lod]["Level"] = lod
                            lodDetail[lodGroup][lod]["parentGroup"] = lodGroup
                            index += 1
            else:
                # 更新旧的节点信息
                if cmds.listRelatives(lodGroup):
                    index = 0
                    for lod in cmds.listRelatives(lodGroup):
                        lodLongName = lodGroup + "|" + lod
                        shapes = self.GetShapeFromGroup(lodLongName)
                        if shapes:
                            Result = cmds.polyEvaluate(shapes[0])
                            lodDetail[lodGroup][lod]["shortName"] = lod
                            lodDetail[lodGroup][lod]["longName"] = lodLongName
                            lodDetail[lodGroup][lod]["index"] = index
                            lodDetail[lodGroup][lod]["shapes"] = shapes
                            lodDetail[lodGroup][lod]["UVShell"] = Result.get("shell")
                            lodDetail[lodGroup][lod]["face"] = Result.get("face")
                            lodDetail[lodGroup][lod]["vertex"] = Result.get("vertex")
                            lodDetail[lodGroup][lod]["Level"] = lod
                            lodDetail[lodGroup][lod]["parentGroup"] = lodGroup
                            index += 1
        return lodDetail

    def GetShapeFromGroup(self, group_name):
        """ 获取组下面的所有shape节点 """
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

    def GetFaceCount(self, object_name):
        """ 获取对象的面数量 """
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

    def CollectLodInfo(self):
        """ 收集场景中的Lod 的信息 """
        from maya import cmds
        lodGroups = cmds.ls(type="lodGroup", long=True)
        lodDetail = {}
        for lodGroup in lodGroups:
            lodDetail[lodGroup] = {}
            lodDetail[lodGroup]["Check"] = "UnCheck"
            if cmds.listRelatives(lodGroup):
                index = 0
                for lod in cmds.listRelatives(lodGroup):
                    lodDetail[lodGroup][lod] = {}
                    lodLongName = lodGroup + "|" + lod
                    lodDetail[lodGroup][lod]["name"] = lodLongName
                    shapes = self.GetShapeFromGroup(lodLongName)
                    if shapes:
                        faces = self.GetFaceCount(shapes[0])
                        Result = cmds.polyEvaluate(shapes[0])
                        lodDetail[lodGroup][lod]["shortName"] = lod
                        lodDetail[lodGroup][lod]["index"] = index
                        lodDetail[lodGroup][lod]["shapes"] = shapes
                        lodDetail[lodGroup][lod]["UVShell"] = Result.get("shell")
                        lodDetail[lodGroup][lod]["face"] = Result.get("face")
                        lodDetail[lodGroup][lod]["vertex"] = Result.get("vertex")
                        lodDetail[lodGroup][lod]["platform"] = "Mobile"
                        lodDetail[lodGroup][lod]["Level"] = lod
                        lodDetail[lodGroup][lod]["parentGroup"] = lodGroup
                        index += 1
        return lodDetail

    def ReorderGroup(self):
        pass


class TreeWidgetItemWidget(QtWidgets.QWidget):
    def __init__(self, text, parent=None):
        super(TreeWidgetItemWidget, self).__init__(parent)
        self.isPreview = False
        layout = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel(text)
        self.button = QtWidgets.QPushButton("Preview")

        layout.addWidget(self.label)
        layout.addWidget(self.button)
        layout.addStretch()
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = ExportLOD()
    myapp.show()
    sys.exit(app.exec_())
