#!/usr/bin/env python3
"""
File: make_clips.py
Author: Yuki Fujishima
Email: yfujishima1001@gmail.com Github: https://github.com/yukids123
Description: Create video clips.
"""

from datetime import datetime
startTime = datetime.now()
import os
from pathlib import Path

import pandas as pd

import moviepy
from moviepy.editor import VideoFileClip, AudioFileClip


if __name__ == "__main__":

    """
    1. Make sure video file (mp4), timestamp file (csv),
       and/or audio file (mp3) are in the same directory

    2. Set the following variables.
        base: Path to the directory in which the files are
        dir_name: Name of the directory for the current project
        vid_fname: Name of a video file
        aud_fname: Name of a audio file
            Uncomment it out when you are using a separate audio
        ts_name: File name of a timestamp file. e.g. timestamp.csb 
    """
    base = Path('/Users/yukifujishima/OneDrive - Kyushu University/UJA/Interviews')
    dir_name = 'Yamada'
    vid_fname = 'yamada_zoom.mp4'
#   aud_fname = 'yamada_zoom.mp3'
    ts_name = 'timestamp.csv'

    """
    End
    """

    clip_dir = base / dir_name / 'clips'
    if os.path.exists(str(clip_dir)):
        print(datetime.now() - startTime, "Already exists:", str(clip_dir))
    else:
        os.mkdir(str(clip_dir))
        print(datetime.now() - startTime, "Created dicrectory:", str(clip_dir))

    original = VideoFileClip(str(base / dir_name / vid_fname))
    if 'aud_fname' in locals():
        audio = AudioFileClip(str(base / dir_name / aud_fname))
    timestamp = pd.read_csv(str(base / dir_name / ts_name))
    
    ts = timestamp[timestamp.columns[0:7]]

    for i in range(ts.shape[0]):
        print('Trimming...', ts['start'].loc[i], ts['end'].loc[i],
              ts['content'].loc[i])
        vid = original.subclip(ts['start'].loc[i], ts['end'].loc[i])
        if 'audio' in locals():
            aud = audio.subclip(ts['start'].loc[i], ts['end'].loc[i])
            vid.set_audio(aud)
        else:
            continue
        vid_path = str(clip_dir / str(ts['content'].loc[i] + '.mp4'))
        vid.write_videofile(vid_path,
                            codec='libx264',
                            audio_codec='aac')
        print(datetime.now() - startTime, "Saved:", vid_path)
