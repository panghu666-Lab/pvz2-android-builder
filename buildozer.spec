[app]

# 应用名称
title = PVZ2脚本工具

# 应用包名
package.name = pvz2tool

# 应用域名（反向）
package.domain = org.pvz2

# 应用版本
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 3.5

# 应用需求
requirements = python3,kivy,requests,colorama

# 应用方向
orientation = portrait

# 全屏模式
fullscreen = 0

# Android API级别
android.api = 33
android.minapi = 21
android.ndk = 25b
android.arch = armeabi-v7a,arm64-v8a

# 权限
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# 应用图标（如果有）
# icon.filename = icon.png
# icon.filename_background = icon_background.png

# 启动画面
# presplash.filename = presplash.png

# 日志级别
log_level = 2

[buildozer]

# 构建目录
build_dir = .buildozer

# 二进制目录
bin_dir = bin

# 日志级别
log_level = 2

# 警告级别
warn_on_root = 1
