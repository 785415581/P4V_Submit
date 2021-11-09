


cmd_out_decode = "utf-8"
ASSETTYPE=["Animal", "Building", "Character", "Effect","Environment", "Prop", "UI", "Weapon"]
ANISTEP = "Animation"
STEP = [ANISTEP, "Mesh", "Rig", "Texture", "PCG"]
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








