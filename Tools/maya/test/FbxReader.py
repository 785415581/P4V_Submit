"""
   Copyright (C) 2017 Autodesk, Inc.
   All rights reserved.

   Use of this software is subject to the terms of the Autodesk license agreement
   provided at the time of installation or download, or which otherwise accompanies
   this software in either electronic or hard copy form.

"""
import os, sys


def TriangulateSplitAllMeshes(pScene, pManager):
    lNode = pScene.GetRootNode()
    lConverter = FbxGeometryConverter(pManager)

    if lNode:
        for i in range(lNode.GetChildCount()):
            lChildNode = lNode.GetChild(i)
            if lChildNode.GetNodeAttribute() != None:
                lAttributeType = (lChildNode.GetNodeAttribute().GetAttributeType())

                if lAttributeType == FbxNodeAttribute.EType.eMesh:
                    lMesh = lChildNode.GetNodeAttribute()

                    print("\nMESH NAME :: %s" % lMesh.GetName())
                    print("MESH POLYGONS :: %i" % lMesh.GetPolygonCount())
                    print("MESH EDGES :: %i" % lMesh.GetMeshEdgeCount())
                    print("TRIANGULATING MESH")
                    lTriangulatedMesh = lConverter.Triangulate(lMesh, False)
                    print("\nTRIANGULATING MESH COMPLETED")
                    print("TRIANGULATED MESH POLYGONS :: %i" % lTriangulatedMesh.GetPolygonCount())
                    print("TRIANGULATED MESH EDGES :: %i" % lTriangulatedMesh.GetMeshEdgeCount())

                    lChildNode.RemoveNodeAttribute(lMesh)
                    lChildNode.AddNodeAttribute(lTriangulatedMesh)

                    # Mesh is triangulated, we can now split it per material
                    lResult = lConverter.SplitMeshPerMaterial(lTriangulatedMesh, False)
                    # lChildNode.RemoveNodeAttribute(lTriangulatedMesh)


def ListAllMeshesCount(pScene):
    print("NUMBER OF GEOMETRIES :: %i" % pScene.GetGeometryCount())


if __name__ == "__main__":
    # try:
    #     sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    #     import FbxCommon
    #     from fbx import *
    # except ImportError:
    #     print("Error: module FbxCommon module failed to import.\n")
    #     sys.exit(1)
    import FbxCommon
    from fbx import *
    # Prepare the FBX SDK.
    lSdkManager, lScene = FbxCommon.InitializeSdkObjects()

    # The example can take a FBX file as an argument.

    fbxFile = "D:/temp/multiplematerials.FBX"

    lResult = FbxCommon.LoadScene(lSdkManager, lScene, fbxFile)

    if not lResult:
        print("\n\nAn error occurred while loading the scene...")
    else:
        print("BEFORE SPLITTING MESHES")
        ListAllMeshesCount(lScene)
        TriangulateSplitAllMeshes(lScene, lSdkManager)

        print("\nAFTER SPLITTING MESHES")
        ListAllMeshesCount(lScene)

        FbxCommon.SaveScene(lSdkManager, lScene, "D:/temp/multiplematerials_output.fbx")

    # Destroy all objects created by the FBX SDK.
    lSdkManager.Destroy()

    sys.exit(0)
