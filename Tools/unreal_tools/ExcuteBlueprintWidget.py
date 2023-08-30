#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: 785415581@qq.com
Date: 2023/8/29 17:02
"""


def ExcuteUtilityWidget(UtilityWidgetPackagePath):
    import unreal
    EdSubsystem = unreal.EditorUtilitySubsystem()
    AssetRegistry = unreal.AssetRegistryHelpers.get_asset_registry()
    Asset = AssetRegistry.get_asset_by_object_path(UtilityWidgetPackagePath)
    EUWAsset = Asset.get_asset()
    if isinstance(EUWAsset, unreal.EditorUtilityWidgetBlueprint):
        BPLib = unreal.BlueprintEditorLibrary()
        BPLib.compile_blueprint(EUWAsset)
        EdSubsystem.spawn_and_register_tab(EUWAsset)


if __name__ == '__main__':
    UtilityWidgetPackagePath = "/Game/Debug/Utilities/CheckTextureAlpha/EUW_CheckTextureAlpha.EUW_CheckTextureAlpha"
    # ExcuteUtilityWidget(UtilityWidgetPackagePath)

"""
LogBlueprintUserMessages: [NewEditorUtilityWidgetBlueprint_C_15] /Game/Debug/Utilities/BP_SortAsset.BP_SortAsset
LogBlueprintUserMessages: [NewEditorUtilityWidgetBlueprint_C_15] /Game/Debug/Utilities/BP_CheckAsset.BP_CheckAsset
LogBlueprintUserMessages: [NewEditorUtilityWidgetBlueprint_C_15] /Game/Debug/Utilities/EUW_GetAllTexture.EUW_GetAllTexture
LogBlueprintUserMessages: [NewEditorUtilityWidgetBlueprint_C_15] /Game/Debug/Utilities/EUW_GoodsReplace.EUW_GoodsReplace
LogBlueprintUserMessages: [NewEditorUtilityWidgetBlueprint_C_15] /Game/Debug/Utilities/EUW_HLODLayerChecker.EUW_HLODLayerChecker
LogBlueprintUserMessages: [NewEditorUtilityWidgetBlueprint_C_15] /Game/Debug/Utilities/EUW_IntegrateInstances.EUW_IntegrateInstances
LogBlueprintUserMessages: [NewEditorUtilityWidgetBlueprint_C_15] /Game/Debug/Utilities/EUW_LayerMaterialChecker.EUW_LayerMaterialChecker
LogBlueprintUserMessages: [NewEditorUtilityWidgetBlueprint_C_15] /Game/Debug/Utilities/EUW_MergeSplineMesh.EUW_MergeSplineMesh
LogBlueprintUserMessages: [NewEditorUtilityWidgetBlueprint_C_15] /Game/Debug/Utilities/EUW_PhysicalMaterialChecker.EUW_PhysicalMaterialChecker
LogBlueprintUserMessages: [NewEditorUtilityWidgetBlueprint_C_15] /Game/Debug/Utilities/EUW_ResaveAssets.EUW_ResaveAssets
LogBlueprintUserMessages: [NewEditorUtilityWidgetBlueprint_C_15] /Game/Debug/Utilities/EUW_RuntimeGridChecker.EUW_RuntimeGridChecker
LogBlueprintUserMessages: [NewEditorUtilityWidgetBlueprint_C_15] /Game/Debug/Utilities/ExtractBlueprint.ExtractBlueprint
LogBlueprintUserMessages: [NewEditorUtilityWidgetBlueprint_C_15] /Game/Debug/Utilities/FindBoundingBox.FindBoundingBox
LogBlueprintUserMessages: [NewEditorUtilityWidgetBlueprint_C_15] /Game/Debug/Utilities/FindExternalActors.FindExternalActors
LogBlueprintUserMessages: [NewEditorUtilityWidgetBlueprint_C_15] /Game/Debug/Utilities/InstancedFoliageActorChecker.InstancedFoliageActorChecker
LogBlueprintUserMessages: [NewEditorUtilityWidgetBlueprint_C_15] /Game/Debug/Utilities/InstancedFoliageActorManage.InstancedFoliageActorManage
LogBlueprintUserMessages: [NewEditorUtilityWidgetBlueprint_C_15] /Game/Debug/Utilities/SetMeshPlatformsLOD.SetMeshPlatformsLOD


"""