


cmd_out_decode = "utf-8"
UITYPE="UI"
ASSETTYPE=["Animal", "Building", "Character", "Effect","Environment", "Prop", UITYPE, "Weapon"]
ANISTEP = "Animation"
TEXTURESTEP = "Texture"
STEP = [ANISTEP, "Mesh", "Rig", TEXTURESTEP, "PCG", "Concept", "Icon"]
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

    ANISTEP: {
        "work": ["|ani|Idle", "|ani|Walk", "|ani|Run"],
        "publish": ["|ani|Idle", "|ani|Walk", "|ani|Run"],
        "type": "shot"
    }
}








