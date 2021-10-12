# import subprocess
# p = subprocess.Popen(r"R:\ProjectX\Tools\bat\AutoWorkspace\AutoWorkspaceTest.bat chenghuanhuan chenghh_1532oj //Assets/main Assets", stdout=subprocess.PIPE, shell=True)
# out=p.stdout.readlines()[-1].strip()
# print(type(str(out.decode("utf-8"))))


file_path = "//Assets/main/Assets/Character/Male/Animation/Melee/LiKai_Melee_TripleHit/BackIdle/LiKai_Melee_Attack2_To_Idle2_new.mb#1 - add change 1772 (binary+l)"
import re
p = re.compile(r"(//Assets/main/Assets/(Animal|Character|Fashion|Weapon)/(.+)/(Animation|Meshes|Textures)/\S+)#.+")
file_path = "... #3 change 307 branch on 2021/07/21 by sunche@sunche_01yxhy1231_main_UE5 (text) 'Copying  //UnrealEngine/main/UE'"
p=re.compile(r".+#(\d+) change (\d+).+by (\S+)@.+")
groups = p.match(file_path)
print(groups.groups())
#
# real_path, asset_type, asset_name, file_type = groups.groups()
# print(real_path)
# print(asset_type)
# print(asset_name)
# print(file_type)
# from AssetBrowser.utils.Leaf import Leaf
#
# for res in ["//Assets/main/Assets/Character/Cyber Leopard/Animation/Cyber_Leopard_Attack_F/Cyber_Leopard_Attack_F.fbx",
#             "//Assets/main/Assets/Character/Cyber Leopard/Animation/Cyber_Leopard_Attack_F/incrementalSave/Cyber_Leopard_Attack_F.mb/Cyber_Leopard_Attack_F.0001.mb"]:
#     out = res.split('/')
#     temp = list()
#     level = str()
#     for index in range(len(out)):
#         if out[index]:
#             level = level + '/' + out[index]
#             temp.append(level)
#     lines = temp
#
#     first_node = Leaf(lines[0])
#
#     # first_node.set_value(str(first_no))
#     # first_node.set_fullPath("{}{}".format(clientStream, first_node.name))
#     # first_no = first_no + 1
#
#     cur_node = first_node
#     for node in [Leaf(name=lines[tmp]) for tmp in range(1, len(lines))]:
#         if node.name not in [child.name for child in cur_node.children]:
#             length = len(cur_node.children)
#             node.set_value(str(length + 100 * int(cur_node.value)))
#             # node.set_fullPath("{}{}".format(clientStream, (node.name).encode('utf-8')))
#             cur_node.add_child(node)
#         cur_node = first_node.search(node)
#
# data = first_node.to_json()