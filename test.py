import platform

# print(platform.freedesktop_os_release())
info_os = platform.freedesktop_os_release()
print(type(info_os))
for i in info_os.values():
    if "fedora" in i.lower():
        print("Fedora")
        break