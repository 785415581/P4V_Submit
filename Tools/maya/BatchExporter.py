#-----------------------------------------#
# Batch Exporter For Maya
#-----------------------------------------#

import maya.cmds as cmds
import os

# Function for window creation and UI.
def CreationWindow():
   
    # If window already exists, close and re-open.
    if cmds.window("BatchExport", ex = True):
       cmds.deleteUI("BatchExport")
    cmds.window("BatchExport", title = "Batch Exporter - v1.0",widthHeight=(400,600), s= True, menuBar = True)
    cmds.window("BatchExport",edit=True ,widthHeight=(350,120), backgroundColor = [0.25, 0.25, 0.25] )
    cmds.columnLayout(adjustableColumn=True)
    
   
    # Main UI Layouts
    cmds.frameLayout( label='Batch Export To Folder', backgroundShade = True, backgroundColor = [0.3, 0.3, 0.3] )
    cmds.rowColumnLayout (numberOfColumns = 1, columnWidth = ( [1,316] ) )
    # help doc
    cmds.rowColumnLayout (numberOfColumns = 1, columnWidth = (  [1,315]  ) )
    cmds.button( label="Help",c=HelpCF, ann="Help CF")
    # Textfield path
    cmds.rowColumnLayout (numberOfColumns = 1, columnWidth = ( [1,315] ) )
    cmds.textField("FilePath", text="", pht="No Folder Selected...", ed=True, dif=True, editable=True, bgc=[0.3, 0.3, 0.3], h=24)
    cmds.setParent("..")

    # Export, choose fbx or obj, show and select folder
    cmds.rowColumnLayout (numberOfColumns = 4, columnWidth = ( [1,200], [2,56], [3,32],[4,32] ) )
    cmds.button( label="Export",c=ExportFile, ann="Export Selected Meshes")



    cmds.optionMenu ("fileTypeOM",height=24 )
    cmds.menuItem("fbxMI", label='FBX' )
    cmds.menuItem("objMI", label='OBJ' )
    
    cmds.iconTextButton( style='iconOnly', h=24, image1="folder-new.png", c=GetPath, ann="Select folder for exporting" )
    cmds.iconTextButton( style='iconOnly', h=24, image1="folder-open.png", c=ShowPath, ann="Show selected folder" )
    cmds.setParent("..")
    
    # Main UI Layouts SetParents
    cmds.setParent("..")
    cmds.setParent("..")
    
    # Show Window
    cmds.showWindow("BatchExport")
  
    
# -------------------------------------------- Get Folder Path ---------------------------------- #
def GetPath(*args):
    
    #Select folder to export
    getpath = cmds.fileDialog2(fm = 3, okc='Select Folder')[0]
    cmds.textField ("FilePath", e=True, tx=getpath)

# -------------------------------------------- Show Folder -------------------------------------- #
def ShowPath(*args):
    
    #Show windows folder
    showpath = cmds.textField ("FilePath", q=True, tx=True)
    if showpath:
        os.startfile(showpath)
    else:
        cmds.confirmDialog(t='Info', icon="information", m='Please select a Folder', button='Ok')


# -------------------------------------------- Export ------------------------------------------- #
def ExportFile(*args):
      
    fileType = ""
    fileTypeSelected = cmds.optionMenu("fileTypeOM", value=True, q=True)
    
    if fileTypeSelected == "FBX":
        fileType = "FBX export"
    if fileTypeSelected == "OBJ":
        fileType = "OBJexport"
        
    meshSel = cmds.ls(sl=True)
    for objSel in meshSel:
        
        if objSel:
            #Query field
            path = cmds.textField ("FilePath", q=True, tx=True)
            
            #Select object and export
            cmds.select(objSel)
            objNames = cmds.ls(sl=True)
            splitName = objNames[0].split('|')
            objName = splitName[-1]
            
            #Export to selected path
            exportPath = path+'/'+objName+'.obj'
            cmds.file (exportPath, es=True, force=True, type=fileType, op="groups=0; ptgroups=0; materials=0; smoothing=1; normals=0")


def HelpCF(*args):
    import webbrowser
    webbrowser.open("https://cf.at.yingxiong.com/pages/viewpage.action?pageId=61346669")

# Run window creation
CreationWindow()