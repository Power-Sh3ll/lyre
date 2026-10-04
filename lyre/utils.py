import shutil
import sys

def dependancy_check():

    os_name = ""
    os_version = ""
    os_build = ""
    os_platform = ""
    ffmpeg_installed = False
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path is not None:
        ffmpeg_installed = True

    # Windows, Mac, and Linux platform check
    if sys.platform.startswith("win"):
        os_name = "Windows"
    elif sys.platform.startswith("darwin"):
        os_name = "Mac"
    else:
        os_name = "Linux"

    # OS Version check
    if sys.platform.startswith("win"):
        version, minor, platform, build = sys.getwindowsversion()[:4]
        os_version = f"{version}.{minor}"
        os_build = f"{build}"
        os_platform = f"{platform}"
    elif sys.platform.startswith("darwin"):
        os_version = f"{platform.mac_ver()[0]}"
        os_build = f"{platform.mac_ver()[2]}"
    else:
        os_version = f"{platform.release()}"
        os_build = f"{platform.version()}"

    return os_name, os_version, os_build, os_platform, ffmpeg_installed

if __name__ == "__main__":
    os_name, os_version, os_build, os_platform, ffmpeg_installed = dependancy_check()
    print(f"OS Name: {os_name}")
    print(f"OS Version: {os_version}")
    print(f"OS Build: {os_build}")
    print(f"OS Platform: {os_platform}")
    print(f"FFmpeg Installed: {ffmpeg_installed}")