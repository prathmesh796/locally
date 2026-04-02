import platform

os_name = platform.system()

if os_name == "Windows":
    print("Running on Windows")
elif os_name == "Darwin":
    print("Mac")
else:
    print("Linux")