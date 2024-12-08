""" Converts files from m4a to mp3"""

from pydub import AudioSegment# Load the M4A file
audio = AudioSegment.from_file("samaltman_short.m4a", format="m4a")

# Export to MP3
audio.export("samaltman_short.mp3", format="mp3")