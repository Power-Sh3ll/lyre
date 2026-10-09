import os, subprocess
from pathlib import Path


ALLOWED_AUDIO_FORMATS = [
    ".mp3", ".wav", ".flac", ".aac", ".m4a", ".ogg", ".wma", ".aiff", ".ape", ".alac"
]

ALLOWED_VIDEO_FORMATS = [
    ".mp4", ".mov", ".m4v", ".mkv", ".webm", ".avi", ".flv", ".wmv", ".mpeg", ".mpg", ".3gp", ".ogv", ".ts", ".mts"
] 

def sanitize_path(path: str | os.PathLike) -> Path:
    """
    Sanitize the given file path by expanding the user tilde and converting it to an absolute path.
    """
    return Path(os.path.abspath(os.path.expanduser(path)))

def check_format(path: str | os.PathLike) -> str:
    """
    Check if the given file path has an allowed audio or video format.

    Args:
        path (str | os.PathLike): The file path to check.

    Returns:
        str: "audio" if the file is an allowed audio format, 
        "video" if the file is an allowed video format, "unknown" otherwise.
    """
    file_ext = os.path.splitext(path)[1].lower()
    media_type = "audio" if file_ext in ALLOWED_AUDIO_FORMATS else "video" if file_ext in ALLOWED_VIDEO_FORMATS else "unknown"

    return media_type

def confirm_overwrite(path: str | os.PathLike) -> bool:
    """
    Prompt the user on the console to confirm overwriting an existing file.

    Args:
        path (str | os.PathLike): The file path that would be overwritten.

    Returns:
        bool: True if the user confirms the overwrite, False otherwise.
    """
    response = input(f"File '{path}' already exists. Overwrite? [y/N] ").strip().lower()
    return response in ("y", "yes")

def rip_and_convert(path: str | os.PathLike, overwrite: bool | None = None) -> Path:
    """
    Use ffmpeg to extract the audio from the given file path and convert it to
    16 kHz mono 16-bit PCM WAV. A .wav input is left untouched and the result is
    written to "<name>_ingested.wav".

    Args:
        path (str | os.PathLike): The file path of the media to rip.
        overwrite (bool | None): Whether to overwrite the output file if it already exists.
            True always overwrites, False never overwrites (keeping the existing file), and
            None (default) prompts the user on the console when the output file already exists.

    Returns:
        path.Path: The file path of the ripped audio file if successful, None otherwise.
    """
    output_path = path.with_suffix(".wav")
    if output_path == path:
        # ffmpeg cannot write over its own input, so never touch the original WAV
        output_path = path.with_name(f"{path.stem}_ingested.wav")

    if output_path.exists():
        if overwrite is None:
            overwrite = confirm_overwrite(output_path)
        if not overwrite:
            return output_path

    command = [
        "ffmpeg",
        "-y",
        "-i", str(path),
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        str(output_path),
    ]
    try:
        subprocess.run(command, check=True)
    except FileNotFoundError:
        print("ffmpeg was not found. Install it and make sure it is on your PATH.")
        return None
    except subprocess.CalledProcessError as e:
        print(f"ffmpeg failed to convert '{path}' (exit code {e.returncode}).")
        return None
    return output_path

def ingest_media(path: str | os.PathLike, overwrite: bool | None = None) -> Path:
    """
    Sanitize the file path and check if the media has a valid format. Strip audio from video and convert everything to 16 kHz mono WAV.

    Args:
        path (str | os.PathLike): The file path of the media to ingest.
        overwrite (bool | None): Whether to overwrite the output file if it already exists.
            True always overwrites, False never overwrites (keeping the existing file), and
            None (default) prompts the user on the console when the output file already exists.

    Returns:
        path.Path: The sanitized file path of the media if conversion was successful, None otherwise.
    """
    media_path = sanitize_path(path)

    media_type = check_format(media_path)
    if media_type == "unknown":
        print(f"Unsupported media format for file: {media_path}")
        return None

    # Check if video or audio and process accordingly
    return rip_and_convert(media_path, overwrite=overwrite)

if __name__ == "__main__":
    test_path = Path.cwd() / "Thants_Not_Jorge.mp4"
    if ingest_media(test_path, overwrite=True) is None:
        print("Failed to ingest media.")
    else:
        print("Media ingested successfully.")