


cmd_out_decode = "utf-8"
ASSETTYPE=["Animal", "Character", "Fashion", "Weapon"]
STEP=["Animation", "Mesh", "Rig", "Texture"]

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

    "Animation": {
        "work": ["|ani|Idle", "|ani|Walk", "|ani|Run"],
        "publish": ["|ani|Idle", "|ani|Walk", "|ani|Run"],
        "type": "shot"
    }
}








