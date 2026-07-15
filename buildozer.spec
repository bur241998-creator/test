[app]
title = Steam Idler
package.name = steamidler
package.domain = org.kendiprojem
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# Sadece kivy ve saf python bağımlılığı olan kütüphaneleri bırakıyoruz
requirements = python3,kivy,steam,urllib3,certifi,chardet,idna

orientation = portrait
fullscreen = 0
android.archs = arm64-v8a
android.accept_sdk_license = 1
