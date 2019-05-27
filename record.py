import pyaudio
import wave
import argparse
import logging.config
import threading
import time
import re
import os
import numpy as np
from scipy.io import wavfile

from audio.captor import Captor
from audio.processor import WavProcessor, format_predictions

parser = argparse.ArgumentParser(description='Capture and process audio')
print('PetKix--SoundClassification--Author: Bin Bo')
parser.add_argument('--min_time', type=float, default=3.5, metavar='SECONDS',
                    help='Minimum capture time')
parser.add_argument('--max_time', type=float, default=5, metavar='SECONDS',
                    help='Maximum capture time')
class Capture(object):
    chunk = 1024  
    sample_format = pyaudio.paInt16
    channels = 1
    fs = 44100   
    seconds = 5
    sleep=0.05
    _process_buf =None
    _ask_data =None
    _save_path=None

    def __init__(start,min_time,max_time, path=None):

        start._save_path = path
        start._ask_data = threading.Event()
        start._captor = Captor(min_time,max_time, start._ask_data, start._process)

    def _process(start, data):
        start._process_buf = np.frombuffer(data, dtype=np.int16)

    
    def start(start):
        start._captor.start()
        start._process_loop()

    def _process_loop(start):
        with WavProcessor() as proc:
            start._ask_data.set()
            
            while True :
                if start._process_buf is None:
                    time.sleep(start.sleep)
                    continue    
                start._ask_data.clear()
                print('Recording :')
                predictions = proc.get_predictions(
                    start.fs,start._process_buf)
                rate_max=str("".join(filter(str.isdigit, (format_predictions(predictions)))))
                sound_max=format_predictions(predictions)
                if(rate_max[0:3]=="100") :
                    searchObj = re.search( r'(.*): 1.00(.*?) .*', format_predictions(predictions), re.M|re.I)
                    print ("Type Sound : ", searchObj.group(1),rate_max[0:3])
                else :
                    print("Not detection --"rate_max[0:3])
                print('Stop Recording')
                print('                 ')
                start._process_buf= None
                start._ask_data.set()


if __name__ == '__main__':
    args = parser.parse_args()
    c = Capture(**vars(args))
    c.start()
