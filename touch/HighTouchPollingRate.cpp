/*
 * SPDX-FileCopyrightText: The LineageOS Project
 * SPDX-License-Identifier: Apache-2.0
 */

#define LOG_TAG "vendor.lineage.touch-service.hormoz"

#include "HighTouchPollingRate.h"

#include <android-base/file.h>
#include <android-base/logging.h>
#include <android-base/strings.h>

namespace aidl {
namespace vendor {
namespace lineage {
namespace touch {

// goodix_ts report rate node. Adjust the values if the node expects something else.
static constexpr const char* kReportRatePath = "/sys/devices/platform/goodix_ts.0/report_rate";
static constexpr const char* kEnabledValue = "1";
static constexpr const char* kDisabledValue = "0";

ndk::ScopedAStatus HighTouchPollingRate::getEnabled(bool* _aidl_return) {
    std::string value;
    if (!android::base::ReadFileToString(kReportRatePath, &value)) {
        PLOG(ERROR) << "Failed to read " << kReportRatePath;
        return ndk::ScopedAStatus::fromExceptionCode(EX_UNSUPPORTED_OPERATION);
    }
    *_aidl_return = android::base::Trim(value) == kEnabledValue;
    return ndk::ScopedAStatus::ok();
}

ndk::ScopedAStatus HighTouchPollingRate::setEnabled(bool enabled) {
    if (!android::base::WriteStringToFile(enabled ? kEnabledValue : kDisabledValue,
                                          kReportRatePath)) {
        PLOG(ERROR) << "Failed to write " << kReportRatePath;
        return ndk::ScopedAStatus::fromExceptionCode(EX_UNSUPPORTED_OPERATION);
    }
    return ndk::ScopedAStatus::ok();
}

}  // namespace touch
}  // namespace lineage
}  // namespace vendor
}  // namespace aidl
