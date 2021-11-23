import pymel.core as pm

def createSubGroups():
    sel_list = pm.ls(sl=1)
    if not sel_list:
        print("No file select")
        return
    sel = sel_list[0]
    child_nodes = pm.listRelatives(sel, allDescendents=True, type="mesh")
    all_trans = []
    for child_node in child_nodes:
        transform_node = pm.listRelatives(child_node, p=True)[0]
        if transform_node not in all_trans:
            group_node = pm.createNode("transform", n=transform_node.name(), parent="|master|Mesh")
            pm.parent(transform_node, group_node)
            all_trans.append(transform_node)