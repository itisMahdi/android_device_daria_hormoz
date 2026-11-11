#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.file import File
from extract_utils.fixups_blob import (
    BlobFixupCtx,
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove_arch_suffix,
    lib_fixups_user_type,
    libs_clang_rt_ubsan,
)
from extract_utils.tools import (
    llvm_objdump_path,
)
from extract_utils.utils import (
    run_cmd,
)
namespace_imports = [
    'device/daria/hormoz',
    'hardware/mediatek/libion_mtk',
    'hardware/mediatek',
    'hardware/mediatek/libmtkperf_client',
]

lib_fixups: lib_fixups_user_type = {
    libs_clang_rt_ubsan: lib_fixup_remove_arch_suffix,
}

def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None

def blob_fixup_graphic_buffer_size(
    ctx: BlobFixupCtx,
    file: File,
    file_path: str,
    *args,
    **kwargs,
):
    for line in run_cmd(
        [
            llvm_objdump_path,
            '--disassemble-all',
            file_path,
        ]
    ).splitlines():
        line = line.split(maxsplit=5)
        if len(line) != 6:
            continue

        # The size of GraphicBuffer changed from 0x100 to 0xd30
        offset, _, instruction, register, value, _ = line
        if instruction == 'mov' and register[:-1] == 'w0' and value == '#0x100':
            with open(file_path, 'rb+') as f:
                f.seek(int(offset[:-1], 16))
                f.write(b'\x00\xa6\x81\x52')  # AArch64 mov w0, #0xd30

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
       'libneuron_graph_delegate.mtk',
       'libtflite_mtk',
        'vendor.mediatek.hardware.apuware.utils-V1-ndk',
    ): lib_fixup_vendor_suffix,
}


_displayservice_ping = (
    b'_ZN7lineage10frameworks14displayservice4V1_014IEventCallback4pingEv'
)
_displayservice_unresolved = (
    rb'_ZN7lineage10frameworks14displayservice4V1_01[45]I[A-Za-z0-9_]*'
    rb'(?:linkToDeath|unlinkToDeath|getDebugInfo|getHashChain|'
    rb'interfaceChain|interfaceDescriptor|5debug|registerForNotifications)'
    rb'[A-Za-z0-9_]*'
)
_displayservice_ctor_vtable = (
    rb'_ZTCN[A-Za-z0-9_]+E\d+_'
    rb'N7lineage10frameworks14displayservice4V1_01[45]I[A-Za-z0-9_]*E'
)

blob_fixups: blob_fixups_user_type = {
    'vendor/etc/init/android.hardware.neuralnetworks-shim-service-mtk.rc': blob_fixup()
        .regex_replace('start', 'enable'),

     'vendor/bin/hw/android.hardware.security.keymint@3.0-service.trustonic': blob_fixup()
        .replace_needed('android.hardware.security.keymint-V3-ndk.so', 'android.hardware.security.keymint-V3-ndk-v34.so'),
   
    'vendor/lib64/libbluetooth_audio_session_aidl_mtk.so': blob_fixup()
        .replace_needed('vendor.mediatek.hardware.bluetooth.audio-V1-ndk.so', 'vendor.mediatek.hardware.bluetooth.audio-V1-ndk-prebuilt.so'),

   
     'vendor/lib64/hw/android.hardware.soundtrigger3-impl.so': blob_fixup()
        .replace_needed('libaudio_aidl_conversion_common_ndk.so', 'libaudio_aidl_conversion_common_ndk_prebuilt.so'),

     'vendor/lib64/hw/audio.primary.mt6897.so': blob_fixup()
        .fix_soname()
        .binary_regex_replace(b'A2dpsuspendonly', b'A2dpSuspended\x00\x00')
        .binary_regex_replace(b'BTAudiosuspend', b'A2dpSuspended\x00')
        .replace_needed('libalsautils.so', 'libalsautils-v34.so')
        .replace_needed('libtinyxml2.so', 'libtinyxml2-v34.so')
        .replace_needed('vendor.mediatek.hardware.bluetooth.audio-V1-ndk.so', 'vendor.mediatek.hardware.bluetooth.audio-V1-ndk-prebuilt.so')
        .replace_needed('android.hardware.audio.common-V1-ndk.so', 'android.hardware.audio.common-V2-ndk.so'),
     
     'vendor/bin/hw/vendor.mediatek.hardware.mtkpower-service.mediatek': blob_fixup()
        .replace_needed('android.hardware.power-V4-ndk.so', 'android.hardware.power-V2-ndk.so'),

    'vendor/lib64/android.hardware.power-service-mediatek.so': blob_fixup()
        .replace_needed('android.hardware.power-V4-ndk.so', 'android.hardware.power-V2-ndk.so'),

    'vendor/bin/mnld': blob_fixup()
        .replace_needed('libmnl.so', 'libmnl_mtk.so'),

    'vendor/lib64/vendor.mediatek.hardware.bluetooth.audio-V1-ndk-prebuilt.so': blob_fixup()
        .replace_needed('android.hardware.audio.common-V1-ndk.so', 'android.hardware.audio.common-V2-ndk.so'),

    ('vendor/bin/hw/android.hardware.graphics.allocator-V2-service-mediatek',
     'vendor/lib64/egl/mt6897/libGLES_mali.so',
     'vendor/lib64/hw/mt6897/android.hardware.graphics.allocator-V2-mediatek.so',
     'vendor/lib64/hw/mt6897/android.hardware.graphics.mapper@4.0-impl-mediatek.so',
     'vendor/lib64/hw/mt6897/mapper.mediatek.so',
     'vendor/lib64/libaimemc.so',
     'vendor/lib64/mt6897/libmtkcam_grallocutils.so',
     'vendor/lib64/libmtkcam_grallocutils_aidlv1helper.so',
     'vendor/lib64/vendor.mediatek.hardware.camera.isphal-V1-ndk.so',
     'vendor/lib64/vendor.mediatek.hardware.pq_aidl-V2-ndk.so',
     'vendor/lib64/vendor.mediatek.hardware.pq_aidl-V4-ndk.so',
     'vendor/lib64/vendor.mediatek.hardware.pq_aidl-V7-ndk.so'): blob_fixup()
        .replace_needed('android.hardware.graphics.allocator-V1-ndk.so', 'android.hardware.graphics.allocator-V2-ndk.so')
        .replace_needed('android.hardware.graphics.common-V4-ndk.so', 'android.hardware.graphics.common-V7-ndk.so'),
    (
     'system_ext/etc/init/init.vtservice.rc',
     'vendor/etc/init/android.hardware.neuralnetworks-shim-service-mtk.rc'
    ): blob_fixup()
        .regex_replace('start', 'enable'),
    'system_ext/lib64/libimsma.so': blob_fixup()
        .replace_needed('libsink.so', 'libsink-mtk.so'),
    'system_ext/lib64/libsink-mtk.so': blob_fixup()
        .add_needed('libaudioclient_shim.so'),
    'system_ext/priv-app/ImsService/ImsService.apk': blob_fixup()
        .apktool_patch('blob-patches/ImsService'),
   
     'vendor/lib64/mt6897/libpqconfig.so': blob_fixup()
        .replace_needed('android.hardware.sensors-V2-ndk.so', 'android.hardware.sensors-V3-ndk.so'),

    ('vendor/lib64/hw/mt6897/vendor.mediatek.hardware.pq_aidl-impl.so',
     'vendor/lib64/libpqxmlflagparser.so',
     'vendor/lib64/libpqxmlparser.so',
     'vendor/lib64/librt_extamp_intf.so',
     'vendor/lib64/libsilkybrightnesscore.so',
     'vendor/lib64/mt6897/libmmlpqImpl.so'): blob_fixup()
        .replace_needed('libtinyxml2.so', 'libtinyxml2-v34.so'),

    ('vendor/lib64/mt6897/libneuralnetworks_sl_driver_mtk_prebuilt.so',
     'vendor/lib64/libTrueSight.so') : blob_fixup()
        .clear_symbol_version('AHardwareBuffer_allocate')
        .clear_symbol_version('AHardwareBuffer_createFromHandle')
        .clear_symbol_version('AHardwareBuffer_describe')
        .clear_symbol_version('AHardwareBuffer_getNativeHandle')
        .clear_symbol_version('AHardwareBuffer_isSupported')
        .clear_symbol_version('AHardwareBuffer_lock')
        .clear_symbol_version('AHardwareBuffer_lockPlanes')
        .clear_symbol_version('AHardwareBuffer_release')
        .clear_symbol_version('AHardwareBuffer_unlock'),

    'vendor/lib64/mt6897/libmtkcam_hal_android_app_cbadaptor.so': blob_fixup()
        .replace_needed('android.frameworks.displayservice@1.0.so',
                        'lineage.frameworks.displayservice@1.0.so')
        .binary_regex_replace(
            b'7android10frameworks14displayservice',
            b'7lineage10frameworks14displayservice')
        .binary_regex_replace(
            _displayservice_unresolved,
            lambda m: _displayservice_ping.ljust(len(m.group(0)), b'\x00'))
        .binary_regex_replace(
            _displayservice_ctor_vtable,
            lambda m: _displayservice_ping.ljust(len(m.group(0)), b'\x00')),

    'vendor/bin/hw/android.hardware.media.c2@1.2-mediatek-64b': blob_fixup()
        .replace_needed('libcodec2_hidl@1.0.so', 'libcodec2_hidl@1.0-v33.so')
        .replace_needed('libcodec2_hidl@1.1.so', 'libcodec2_hidl@1.1-v33.so')
        .replace_needed('libcodec2_hidl@1.2.so', 'libcodec2_hidl@1.2-v33.so')
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk-v33.so'),
    'vendor/lib64/libcodec2_hidl@1.0-v33.so': blob_fixup()
        .replace_needed('libstagefright_bufferqueue_helper.so', 'libstagefright_bufferqueue_helper-bp2a.so')
        .replace_needed('libcodec2_hidl_plugin.so', 'libcodec2_hidl_plugin-v33.so')
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk-v33.so')
        .replace_needed('libui.so', 'libui-v34.so')
        .add_needed('libbase_shim.so'),
    'vendor/lib64/libcodec2_hidl@1.1-v33.so': blob_fixup()
        .replace_needed('libstagefright_bufferqueue_helper.so', 'libstagefright_bufferqueue_helper-bp2a.so')
        .replace_needed('libcodec2_hidl@1.0.so', 'libcodec2_hidl@1.0-v33.so')
        .replace_needed('libcodec2_hidl_plugin.so', 'libcodec2_hidl_plugin-v33.so')
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk-v33.so')
        .replace_needed('libui.so', 'libui-v34.so')
        .add_needed('libbase_shim.so'),
    'vendor/lib64/libcodec2_hidl@1.2-v33.so': blob_fixup()
        .replace_needed('libstagefright_bufferqueue_helper.so', 'libstagefright_bufferqueue_helper-bp2a.so')
        .replace_needed('libcodec2_hidl@1.0.so', 'libcodec2_hidl@1.0-v33.so')
        .replace_needed('libcodec2_hidl@1.1.so', 'libcodec2_hidl@1.1-v33.so')
        .replace_needed('libcodec2_hidl_plugin.so', 'libcodec2_hidl_plugin-v33.so')
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk-v33.so')
        .replace_needed('libui.so', 'libui-v34.so')
        .add_needed('libbase_shim.so'),
    'vendor/lib64/libcodec2_hidl_plugin-v33.so': blob_fixup()
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk-v33.so'),
    'vendor/lib64/libcodec2_vndk-v33.so': blob_fixup()
        .replace_needed('android.hardware.media.bufferpool2-V1-ndk.so', 'android.hardware.media.bufferpool2-V2-ndk.so')
        .replace_needed('libui.so', 'libui-v34.so')
        .replace_needed('libstagefright_foundation.so', 'libstagefright_foundation-v33.so'),
    'vendor/lib64/libcodec2_soft_common-v33.so': blob_fixup()
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk-v33.so')
        .replace_needed('libstagefright_foundation.so', 'libstagefright_foundation-v33.so')
        .replace_needed('libsfplugin_ccodec_utils.so', 'libsfplugin_ccodec_utils-v33.so'),
    'vendor/lib64/libsfplugin_ccodec_utils-v33.so': blob_fixup()
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk-v33.so')
        .replace_needed('libstagefright_foundation.so', 'libstagefright_foundation-v33.so'),
    (
        'vendor/lib64/libcodec2_vpp_AIMEMC_plugin.so',
        'vendor/lib64/libcodec2_vpp_AISR_plugin.so',
    ): blob_fixup()
        .replace_needed('android.hardware.graphics.allocator-V1-ndk.so', 'android.hardware.graphics.allocator-V2-ndk.so')
        .replace_needed('android.hardware.graphics.common-V4-ndk.so', 'android.hardware.graphics.common-V7-ndk.so')
        .replace_needed('libcodec2_soft_common.so', 'libcodec2_soft_common-v33.so')
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk-v33.so')
        .replace_needed('libstagefright_foundation.so', 'libstagefright_foundation-v33.so')
        .replace_needed('libsfplugin_ccodec_utils.so', 'libsfplugin_ccodec_utils-v33.so')
        .replace_needed('libui.so', 'libui-v34.so'),
    (
        'vendor/lib64/libcodec2_mtk_c2store.so',
        'vendor/lib64/libcodec2_vpp_fa_plugin.so',
        'vendor/lib64/libcodec2_vpp_mi_plugin.so',
        'vendor/lib64/libcodec2_vpp_qt_plugin.so',
        'vendor/lib64/libcodec2_vpp_rs_plugin.so',
    ): blob_fixup()
        .replace_needed('libcodec2_soft_common.so', 'libcodec2_soft_common-v33.so')
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk-v33.so')
        .replace_needed('libstagefright_foundation.so', 'libstagefright_foundation-v33.so')
        .replace_needed('libsfplugin_ccodec_utils.so', 'libsfplugin_ccodec_utils-v33.so')
        .replace_needed('libui.so', 'libui-v34.so'),
    (
        'vendor/lib64/libcodec2_mtk_vdec.so',
        'vendor/lib64/libcodec2_mtk_venc.so',
    ): blob_fixup()
        .replace_needed('libformatter.so', 'libformatter_mtk.so')
        .replace_needed('libcodec2_soft_common.so', 'libcodec2_soft_common-v33.so')
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk-v33.so')
        .replace_needed('libstagefright_foundation.so', 'libstagefright_foundation-v33.so')
        .replace_needed('libsfplugin_ccodec_utils.so', 'libsfplugin_ccodec_utils-v33.so')
        .replace_needed('libui.so', 'libui-v34.so'),

    'vendor/lib64/libBSTSWAD.so': blob_fixup()
        .clear_symbol_version('AHardwareBuffer_allocate')
        .clear_symbol_version('AHardwareBuffer_describe')
        .clear_symbol_version('AHardwareBuffer_lock')
        .clear_symbol_version('AHardwareBuffer_lockPlanes')
        .clear_symbol_version('AHardwareBuffer_release')
        .clear_symbol_version('AHardwareBuffer_unlock'),

    'vendor/lib64/mt6897/libmtkcam_hwnode.jpegnode.so': blob_fixup()
        .replace_needed('libultrahdr.so', 'libultrahdr-v34.so'),

    'vendor/lib64/libultrahdr-v34.so': blob_fixup()
        .replace_needed('libjpegencoder.so', 'libjpegencoder-v34.so')
        .replace_needed('libjpegdecoder.so', 'libjpegdecoder-v34.so'),

     'vendor/lib64/mt6897/lib3a.ae.stat.so': blob_fixup()
        .add_needed('liblog.so'),

     'vendor/lib64/hw/hwcomposer.mtk_common.so': blob_fixup()
        .add_needed('libprocessgroup_shim.so'),

    'vendor/lib64/hw/mt6897/vendor.mediatek.hardware.pq_aidl-impl.so': blob_fixup()
        .add_needed('libui_shim.so'),

    'vendor/lib64/libmorpho_video_stabilizer.so': blob_fixup()
        .add_needed('libutils.so'),

     'vendor/lib64/libcodec2_fsr.so': blob_fixup()
        .call(blob_fixup_graphic_buffer_size)
        .replace_needed('android.hardware.graphics.common-V4-ndk.so', 'android.hardware.graphics.common-V7-ndk.so')
        .replace_needed('android.hardware.graphics.allocator-V1-ndk.so', 'android.hardware.graphics.allocator-V2-ndk.so')
        .replace_needed('libcodec2_soft_common.so', 'libcodec2_soft_common-v33.so')
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk-v33.so')
        .replace_needed('libstagefright_foundation.so', 'libstagefright_foundation-v33.so')
        .replace_needed('libsfplugin_ccodec_utils.so', 'libsfplugin_ccodec_utils-v33.so')
        .replace_needed('libui.so', 'libui-v34.so'),

    'vendor/bin/hw/android.hardware.biometrics.fingerprint-service.hormoz': blob_fixup()
        .replace_needed('android.hardware.biometrics.common.util.so', 'android.hardware.biometrics.common.util-hormoz.so')
        .replace_needed('android.hardware.biometrics.common.thread.so', 'android.hardware.biometrics.common.thread-hormoz.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'hormoz',
    'daria',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
