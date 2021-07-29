import os


def createAsset(assetPath):
    if not os.path.isdir(assetPath):
        os.mkdir(assetPath)
        aniPath = os.path.join(assetPath, 'Animation')
        meshPath = os.path.join(assetPath, 'Mesh')
        rigPath = os.path.join(assetPath, 'Rig')
        texPath = os.path.join(assetPath, 'Textures')
        os.mkdir(aniPath)
        os.mkdir(meshPath)
        os.mkdir(rigPath)
        os.mkdir(texPath)


def formatName():
    pass
