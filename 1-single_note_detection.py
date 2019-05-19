import numpy as np
import math
import wave
import os
import struct


def audio_file_rewind(audio_file):
    audio_file.rewind()


def find_peak(array):
    length = len(array)
    cnt=[]
    flag= -1
    var=0
    imax =0
    for i in range(1,length):
            if array[i-1]<array[i]:
                if flag == -1:
                    flag = 1
            if array[i-1]>array[i]:
                if flag == 1:
                    flag = -1
                    cnt.append(i-1)
    if len(cnt)==1:
        imax = cnt[0]
    else:
        maxm = np.max(array)
        mid = maxm/8
        for i in range(0, len(cnt)):
            #print array[cnt[i]], mid
            if array[cnt[i]] > mid:
                #print cnt[i], mid
                imax = cnt[i+5]
                break
    return imax
    '''this function find_peak() is defined to give the approximate position of the
        fundamental frequency, exact position is given argmax() method in the approx range'''

def freq_find(f):
    notes=["C0","C#0","D0","D#0","E0","F0","F#0","G0","G#0","A0","A#0","B0","C1",
    "C#1","D1","D#1","E1","F1","F#1","G1","G#1","A1","A#1","B1","C2","C#2","D2",
    "D#2","E2","F2","F#2","G2","G#2","A2","A#2","B2","C3","C#3","D3","D#3","E3",
    "F3","F#3","G3","G#3","A3","A#3","B3","C4","C#4","D4","D#4","E4","F4","F#4","G4",
    "G#4","A4","A#4","B4","C5","C#5","D5","D#5","E5","F5","F#5","G5","G#5","A5","A#5",
    "B5","C6","C#6","D6","D#6","E6","F6","F#6","G6","G#6","A6","A#6","B6","C7","C#7",
    "D7","D#7","E7","F7","F#7","G7","G#7","A7","A#7","B7","C8","C#8","D8","D#8","E8",
    "F8","F#8","G8","G#8","A8","A#8","B8"]
    freq=[16.35,17.32,18.35,19.45,20.60,21.83,23.12,24.50,25.96,
    27.50,29.14,30.87,32.70,34.65,36.71,38.89,41.20,43.65,46.25,
    49.00,51.91,55.00,58.27,61.74,65.41,69.30,73.42,77.78,82.41,
    87.31,92.50,98.00,103.83,110.00,116.54,123.47,130.81,138.59,
    146.83,155.56,164.81,174.61,185.00,196.00,207.65,220.00,233.08,
    246.94,261.63,277.18,293.66,311.13,329.23,349.23,369.99,392.00,
    415.30,440.00,466.16,493.88,523.25,554.37,587.33,622.25,659.25,
    698.46,739.99,783.99,830.61,880.00,932.33,987.77,1046.50,1108.73,
    1174.66,1244.51,1318.51,1396.91,1479.98,1567.98,1661.22,1760.00,
    1864.66,1975.53,2093.00,2217.46,2349.32,2489.02,2637.02,2793.83,
    2959.96,3135.96,3322.44,3520.00,3729.31,3951.07,4186.01,4434.92,
    4698.63,4978.03,5274.40,5587.65,5919.91,6271.93,6644.88,7040.00,
    7458.62,7902.13]
    Detected_Note = 0
    for i in range(0,len(notes)):
        if (f < freq[i]):
            k=i
            break
    c=(freq[k]+freq[k-1])/2
    if f>c:
        Detected_Note = notes[k]

    else:
        Detected_Note = notes[k-1]



    return Detected_Note


############################### Your Code Here ##############################################

def note_detect(audio_file):

	#   Input   :   audio_file -- a single test audio_file as input argument
	#   Output  :   Detected_Note -- String corresponding to the Detected Note
	#   Example :   For Audio_1.wav file, Detected_Note = "A4"

        Detected_Note = ""
        wavefile = audio_file
        length = wavefile.getnframes()
        fs = wavefile.getframerate()
        sound_wave = np.zeros(length)
        for i in range (0,length):
                data = wavefile.readframes(1)
                data = struct.unpack("<h", data)
                sound_wave[i] = int(data[0])
        sound_wave = np.divide(sound_wave, float(2**15))

        audio_file_rewind(audio_file)
        new_wave = sound_wave

        samp = len(new_wave)
        freq_domain = abs(np.fft.rfft(new_wave))      #calculating frequecy domain array using dft
        irange= find_peak(freq_domain)                #This gives an aproximate location of the peak
        peak_range = freq_domain[0:irange]
        imax = np.argmax(peak_range)                  #finding the exact peak of the fundamental frequency
        f = (imax*fs)/samp
        Detected_Note = freq_find(f)                  #matching the frequency with correct note
        return Detected_Note


############################### Main Function ##############################################

if __name__ == "__main__":

	

	# code for checking output for single audio file
	path = os.getcwd()

	file_name = path + "\singe_note_files_SINGLE-NOTE-DETECTION\Audio_1.wav"
	audio_file = wave.open(file_name)

	Detected_Note = note_detect(audio_file)

	print("\n\tDetected Note = " + str(Detected_Note))

	# code for checking output for all audio files
	x = raw_input("\n\tWant to check output for all Audio Files - Y/N: ")

	if x == 'Y':

		Detected_Note_list = []

		file_count = len(os.listdir(path + "\singe_note_files_SINGLE-NOTE-DETECTION"))

		for file_number in range(1, file_count):

			file_name = path + "\singe_note_files_SINGLE-NOTE-DETECTION\Audio_"+str(file_number)+".wav"
			audio_file = wave.open(file_name)

			Detected_Note = note_detect(audio_file)

			Detected_Note_list.append(Detected_Note)

		print("\n\tDetected Notes = " + str(Detected_Note_list))


