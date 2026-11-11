echo 'Starting to clone stuffs needed to build for hormoz'


echo 'cloning prebuilt kernel'
git clone https://github.com/daria-mt6897-devs/android_device_daria_hormoz-kernel device/daria/hormoz-kernel

echo 'cloning hardware mediatek'
git clone https://github.com/LineageOS/android_hardware_mediatek -b lineage-24.0 hardware/mediatek

echo 'cloning sepolicy_vndr'
git clone https://github.com/LineageOS/android_device_mediatek_sepolicy_vndr -b lineage-24.0 device/mediatek/sepolicy_vndr
