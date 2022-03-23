from pytube import YouTube
from moviepy.editor import *
import os 
import re
import json

with open('config.json', 'r') as f:
    config_load = json.load(f)

PREFIX_VIDEO = config_load['PREFIX_VIDEO']
PREFIX_AUDIO = config_load['PREFIX_AUDIO']
THREADS = config_load['THREADS']
OUTPUT_PATH = config_load['OUTPUT_PATH']
TEMP_FILE_NAME = config_load['TEMP_FILE_NAME']

youtube_link = input(">> Link: ")

yt = YouTube(youtube_link)

video_streams = yt.streams.filter(adaptive=True, type="video")
audio_streams = yt.streams.filter(adaptive=True, type="audio")

print('----------------------VIDEO STREAMS----------------------')
[print(i, line) for (i, line) in enumerate(video_streams, start=1)]
print('----------------------AUDIO STREAMS----------------------')
[print(i, line) for (i, line) in enumerate(audio_streams, start=1)]
print('---------------------------------------------------------')

video_stream_num, audio_stream_num = map(int, input('Pick video and audio number (example: 0 1): ').split())

selected_video_stream = video_streams[video_stream_num-1]
selected_audio_stream = audio_streams[audio_stream_num-1]

print('\nVideo stream: {}'.format(selected_video_stream))
print('Audio stream: {}\n'.format(selected_audio_stream))

video_stream = yt.streams.get_by_itag(selected_video_stream.itag)
audio_stream = yt.streams.get_by_itag(selected_audio_stream.itag)

print('Downloading video stream...')
video_stream.download(output_path = OUTPUT_PATH, filename_prefix = PREFIX_VIDEO, filename = "{0}.{1}".format(TEMP_FILE_NAME, selected_video_stream.mime_type.split("/")[1]), skip_existing=False)
print('Done!')
print('Downloading audio stream...')
audio_stream.download(output_path = OUTPUT_PATH, filename_prefix = PREFIX_AUDIO, filename = "{0}.{1}".format(TEMP_FILE_NAME, selected_audio_stream.mime_type.split("/")[1]), skip_existing=False)
print('Done!\n')

video_name = "{0}{1}.{2}".format(PREFIX_VIDEO, TEMP_FILE_NAME, selected_video_stream.mime_type.split("/")[1])
audio_name = "{0}{1}.{2}".format(PREFIX_AUDIO, TEMP_FILE_NAME, selected_audio_stream.mime_type.split("/")[1])

video = VideoFileClip('{0}{1}'.format(OUTPUT_PATH, video_name))
audio = AudioFileClip('{0}{1}'.format(OUTPUT_PATH, audio_name))

videoclip = video.set_audio(audio)

videoclip.write_videofile('{0}{1}{2}'.format(OUTPUT_PATH, re.sub(r'([^\s\w]|_)+', '', selected_video_stream.title), '.mp4'), threads = THREADS)

if os.path.exists('{0}{1}'.format(OUTPUT_PATH, video_name)):
    os.remove('{0}{1}'.format(OUTPUT_PATH, video_name))
else:
    print('No temporary video file to delete')
if os.path.exists('{0}{1}'.format(OUTPUT_PATH, audio_name)):
    os.remove('{0}{1}'.format(OUTPUT_PATH, audio_name))
else: 
    print('No temporary audio file to delete')

input("\nPRESS ENTER TO CLOSE...")