

import struct
import numpy as np
import math
import wave
import os


def audio_file_rewind(audio_file):
    audio_file.rewind()

def extract_sound_wave(wavefile):                                               #extracting the file in an array
    length = wavefile.getnframes()
    fs = wavefile.getframerate()
    sound_wave = np.zeros(length)
    for i in range (0,length):
        data = wavefile.readframes(1)
        if len(data) < 2:
            print data
        data = struct.unpack("<h", data)
        sound_wave[i] = int(data[0])
    sound_wave = np.divide(sound_wave, float(2**15))
    return sound_wave, length, fs                                               #returning the array, length of the array and framerate
############################### Your Code Here #############################################

def detect_note_duration(audio_file):
    Note_durations=[]
    wavefile = audio_file
    length = wavefile.getnframes()
    fs = wavefile.getframerate()
    sound_wave = np.zeros(length)
    for i in range (0,length):
        data = wavefile.readframes(1)
        if len(data) < 2:
            print data
        data = struct.unpack("<h", data)
        sound_wave[i] = int(data[0])
    sound_wave = np.divide(sound_wave, float(2**15))
    
    thresh = 0.000005                                                           #a value to filter the sound wave
    arr = [[0,0]]
    k = int(0.001*length)                                                       #taking the 1/1000th of length of array
    j=1
    for i in range(0,length/k):
        samp = sound_wave[k*i : k*(i+1)]                                        #taking the sample space of 0.001 from the array
        avg = np.mean(np.square(samp))                                          #finding the square mean of the sample
        if avg < thresh:                                                        #comparing the mean to the thresh
            if arr[j-1][1]==k*i:
                arr[j-1][1] = k*(i+1)                                           #if two consecutive sample array are added, they have to be merged

            else:
                arr.append([k*i,k*(i+1)])                                       #appending the sample array
                j+=1
    arr.append([len(sound_wave),len(sound_wave)])

    arr1=[]
    for i in range(0,len(arr)-1):
        arr1.append ([arr[i][1],arr[i+1][0]])

    for i in range(0,len(arr1)):
        for j in range(0,len(arr1[i])):
            arr1[i][j]=float(arr1[i][j])/44100                                  #convering the frame measure to time measure

    for a in arr1:
        if a[1]-a[0] > 0.02:                                                    #clearing any errors
            Note_durations.append([round(a[0],2),round(a[1],2)])                #rounding of the value to 0.01 values
    audio_file_rewind(audio_file)
    return Note_durations




############################### Your Code Here #############################################

def detect_silence_duration(audio_file):
    Silence_durations=[]
    wavefile = audio_file
    length = wavefile.getnframes()
    fs = wavefile.getframerate()
    sound_wave = np.zeros(length)
    for i in range (0,length):
        data = wavefile.readframes(1)
        if len(data) < 2:
            print data
        data = struct.unpack("<h", data)
        sound_wave[i] = int(data[0])
    sound_wave = np.divide(sound_wave, float(2**15))

    #sound_wave, length, fs = extract_sound_wave(audio_file)                     #a value to filter the sound wave
    thresh = 0.000001
    arr = [[0,0]]
    k = int(0.001*length)
    j=1
    for i in range(0,length/k):
        samp = sound_wave[k*i : k*(i+1)]                                        #taking the sample space of 0.001 from the array
        avg = np.mean(np.square(samp))
        if avg > thresh:                                                        #comparing the mean to the thresh
            if arr[j-1][1]==k*i:
                arr[j-1][1] = k*(i+1)

            else:
                arr.append([k*i,k*(i+1)])
                j+=1
    arr.append([len(sound_wave),len(sound_wave)])

    arr1=[]
    for i in range(0,len(arr)-1):
        arr1.append ([arr[i][1],arr[i+1][0]])

    for i in range(0,len(arr1)):
        for j in range(0,len(arr1[i])):
            arr1[i][j]=float(arr1[i][j])/44100


    for a in arr1:
        if a[1]-a[0] > 0.02:                                                    #clearing any errors
            Silence_durations.append([round(a[0],2),round(a[1],2)])
            audio_file_rewind(audio_file)
    return Silence_durations


############################### Main Function #############################################

if __name__ == "__main__":

	

	# code for checking output for single audio file
	path = os.getcwd()

	file_name = path + "\multiple_note_files_SILENCE-DURATION\Audio_1.wav"
	audio_file = wave.open(file_name)

	Note_durations = detect_note_duration(audio_file)
	Silence_durations = detect_silence_duration(audio_file)

	print("\n\tNotes Duration = " + str(Note_durations))
	print("\n\tSilence Duration = " + str(Silence_durations))

	# code for checking output for all audio files
	x = raw_input("\n\tWant to check output for all Audio Files - Y/N: ")

	if x == 'Y':

		Note_durations_list = []

		Silence_durations_list = []

		file_count = len(os.listdir(path + "\multiple_note_files_SILENCE-DURATION"))

		for file_number in range(1, file_count):

			file_name = path +"\multiple_note_files_SILENCE-DURATION\Audio_"+str(file_number)+".wav"
			audio_file = wave.open(file_name)

			Note_durations = detect_note_duration(audio_file)
			Silence_durations = detect_silence_duration(audio_file)

			Note_durations_list.append(Note_durations)
			Silence_durations_list.append(Silence_durations)

		print("\n\tNotes Duration = " + str(Note_durations_list[0]) + ",\n\t\t\t" + str(Note_durations_list[1]) + ",\n\t\t\t" + str(Note_durations_list[2]))
		print("\n\tSilence Duration = " + str(Silence_durations_list[0]) + ",\n\t\t\t" + str(Silence_durations_list[1]) + ",\n\t\t\t" + str(Silence_durations_list[2]))

