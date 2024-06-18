import pyblish.api


class CollectMeshInstances(pyblish.api.ContextPlugin):
  """ 检查模型的点和UV的数量是否一致"""
  # order = pyblish.api.CollectorOrder - 0.1
  order = 0
  label = "Static mesh Vertices Check"
  hosts = ['maya']
  version = (0, 1, 0)
  InstanceName = "CollectMesh"
  def process(self, context):
    context.create_instance(self.InstanceName, family="StaticMesh")
    print("hel")

class ValidateMeshVertices(pyblish.api.InstancePlugin):
  """ 检查模型的点和UV的数量是否一致"""
  order = 1
  hosts = ['maya']
  families = ["StaticMesh"]
  label = "Static mesh Vertices Check"
  def process(self, instance):
    from maya import cmds
    nUVMesh = list()
    for mesh in cmds.ls(ni=1, type="mesh"):
      vtxNum = cmds.polyEvaluate(mesh, v=1)
      uvNum = cmds.polyEvaluate(mesh, uv=1)

      if uvNum < vtxNum:
        nUVMesh.append(mesh)
    assert len(nUVMesh) == 0, " Sorry, This mesh does't creact"


class ValidateMeshVertices(pyblish.api.InstancePlugin):
  """ 检查模型的点和UV的数量是否一致"""
  order = 1
  hosts = ['maya']
  families = ["StaticMesh"]
  label = "Static mesh Vertices Check"
  def process(self, instance):
    from maya import cmds
    nUVMesh = list()
    for mesh in cmds.ls(ni=1, type="mesh"):
      vtxNum = cmds.polyEvaluate(mesh, v=1)
      uvNum = cmds.polyEvaluate(mesh, uv=1)

      if uvNum < vtxNum:
        nUVMesh.append(mesh)
    assert len(nUVMesh) == 0, " Sorry, This mesh does't creact"


class ValidateMesh():
  pass
