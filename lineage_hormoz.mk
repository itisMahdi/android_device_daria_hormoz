#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

# Inherit from those products. Most specific first.
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit_only.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)

# Inherit from hormoz device
$(call inherit-product, device/daria/hormoz/device.mk)

# Inherit some common Lineage stuff.
$(call inherit-product, vendor/lineage/config/common_full_phone.mk)

PRODUCT_DEVICE := hormoz
PRODUCT_NAME := lineage_hormoz
PRODUCT_BRAND := Daria
PRODUCT_MODEL := DM-B70104
PRODUCT_MANUFACTURER := daria

PRODUCT_GMS_CLIENTID_BASE := android-ragentek

PRODUCT_BUILD_PROP_OVERRIDES += \
    BuildDesc="hormoz-user 16 BP2A.250805.005 V7.1.2.5.BOND2 release-keys" \
    BuildFingerprint=Daria/hormoz/hormoz:16/BP2A.250805.005/V7.1.2.5.BOND2:user/release-keys
