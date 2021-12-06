

VERSION = "v1.01.301"
cmd_out_decode = "utf-8"

DEBUG = False

UITYPE="UI"
ASSETTYPE=["Animal", "Building", "Character", "Effect","Environment", "Prop", UITYPE, "Weapon"]
ANISTEP = "Animation"
TEXTURESTEP = "Texture"
STEP = [ANISTEP, "Mesh", "StaticMesh", "Rig", TEXTURESTEP, "PCG", "Concept", "Icon"]
ANIMODEL = ["Idle", "Walk", "Run"]

MAYALEVEL = {
    "Rig":{
        "work": ["|master|Rig"],
        "publish": ["|master"],
        "type": "asset"
    },

    "Mesh": {
        "work": ["|master|Mesh"],
        "publish": ["|master"],
        "type": "asset"
    },

    "StaticMesh": {
        "work": ["|master|Mesh"],
        "publish": ["|master"],
        "type": "asset"
    },

    ANISTEP: {
        "work": ["|ani|model"],
        "publish": ["|ani|model"],
        "type": "shot"
    }
}








