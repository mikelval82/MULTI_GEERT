# -*- coding: utf-8 -*-
"""
@author: %(Mikel Val Calvo, Juan Antonio Barios Heredero, Arturo Bertomeu-Motos)
@email: %(mikel1982mail@gmail.com, juan.barios@gmail.com, arturobm90@gmail.com)
@institution: %(Dpto. de Inteligencia Artificial, Universidad Nacional de Educación a Distancia (UNED); Center for Biomedical Technology, Universidad Politécnica, Madrid, Spain; Neuroengineering medical group (UMH) ) 
@DOI: 
"""
#%%
from multiprocessing import Process
import numpy as np
import ffmpeg
import os
   

def write_AV(video_frames, path, trial, framerate=10, vcodec='libx264'):
    data_file = os.path.join('.', path + '_' + 'WEBCAM' + '_trial_' + str(trial)) + '.mp4'
    
    p = Process(target=save, args=(data_file,framerate,vcodec,video_frames))
    p.start()

    
def save(data_file, framerate, vcodec, video_frames):
    output = data_file
    
    n,height,width,channels = video_frames.shape
    
    if not isinstance(video_frames, np.ndarray):
        video_frames = np.asarray(video_frames)

    process = (
        ffmpeg
            .input('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(width, height))
            .output(output, pix_fmt='yuv420p', vcodec=vcodec, r=framerate)  
            .overwrite_output()
            .run_async(pipe_stdin=True)
    )

    for frame in video_frames:
        process.stdin.write(
            frame
                .astype(np.uint8)
                .tobytes()
        )
        
        
    process.stdin.close()
    process.wait()
    

