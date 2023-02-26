import sys
import os
import cv2
import time
from cv2 import VideoWriter
from cv2 import VideoWriter_fourcc
from pynput import keyboard

camid = int(sys.argv[1]) # device id
protfolder = sys.argv[2] # exclamation id from medical information system
# resolution parameters height and width
resolh = int(sys.argv[3])
resolv = int(sys.argv[4])
isvideo = 0
vfolder = os.getcwd()+'\\'#+protfolder+'\\'

def for_canonical(f):
    return lambda k: f(l.canonical(k))

def on_snapshot():
	#Take photo
	imgfile = vfolder+time.strftime("%d-%m-%Y-%H-%M-%S")+".jpg"
	cv2.imwrite(filename=imgfile, img=frame)

def on_start_video_record():
	#Get videofile and start recording
	isvideo = 1
	vfile = vfolder + time.strftime("%d-%m-%Y-%H-%M-%S")+".avi"
	video = VideoWriter(vfile, VideoWriter_fourcc(*'MP42'), 25.0, (resolh, resolv))

def on_stop_video_record():
	#Stop recording video
	isvideo = 0
	video.release()

def on_exit_scope():
	#Release device and close the application
	if isvideo == 1:
		video.release()
	cv2.destroyAllWindows()
	webcam.release()

#Getting the stream from device
webcam = cv2.VideoCapture(camid)

with keyboard.GlobalHotKeys({
		'<ctrl>+<alt>+s': on_snapshot,
		'<ctrl>+<alt>+v': on_start_video_record,
		'<ctrl>+<alt>+x': on_stop_video_record,
		'<ctrl>+<alt>+e': on_exit_scope}) as h:
	h.join()

while True:
	#Getting frame from device
	stream_ok, frame = webcam.read()

	if stream_ok:
		#Showing current frame from device
		cv2.namedWindow('Celsus.Videoscope', cv2.WND_PROP_FULLSCREEN)
		cv2.moveWindow('Celsus.Videoscope', 0, 0)
		cv2.setWindowProperty('Celsus.Videoscope', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
		cv2.imshow('Celsus.Videoscope', frame)
		if isvideo == 1:
			#Write current frame to our videofile
			video.write(frame)

		if cv2.waitKey(1) & 0xFF == 27: break
		
	
#Release device and close the application
if isvideo == 1:
	video.release()
cv2.destroyAllWindows()
webcam.release()
