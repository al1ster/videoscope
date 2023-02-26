import sys
import os
import cv2
import time
from cv2 import VideoWriter
from cv2 import VideoWriter_fourcc
from pynput import keyboard

camid = int(sys.argv[1]) # id камеры
protfolder = sys.argv[2] # id обследования
resolh = int(sys.argv[3]) # Разрешение по горизонтали
resolv = int(sys.argv[4]) # Разрешение по вертикали
isvideo = 0
vfolder = os.getcwd()+'\\'#+protfolder+'\\'

def for_canonical(f):
    return lambda k: f(l.canonical(k))

def on_snapshot():
	#Делаем фото
	imgfile = vfolder+time.strftime("%d-%m-%Y-%H-%M-%S")+".jpg"
	cv2.imwrite(filename=imgfile, img=frame)

def on_start_video_record():
	#Задаем видеофайл и включаем режим записи потока
	isvideo = 1
	vfile = vfolder + time.strftime("%d-%m-%Y-%H-%M-%S")+".avi"
	video = VideoWriter(vfile, VideoWriter_fourcc(*'MP42'), 25.0, (resolh, resolv))

def on_stop_video_record():
	#Останавливаем запись и выключаем режим
	isvideo = 0
	video.release()

def on_exit_scope():
	#Освобождаем камеру и закрываем окно
	if isvideo == 1:
		video.release()
	cv2.destroyAllWindows()
	webcam.release()

#Получение потока от веб-камеры
webcam = cv2.VideoCapture(camid)

with keyboard.GlobalHotKeys({
		'<ctrl>+<alt>+s': on_snapshot,
		'<ctrl>+<alt>+v': on_start_video_record,
		'<ctrl>+<alt>+x': on_stop_video_record,
		'<ctrl>+<alt>+e': on_exit_scope}) as h:
	h.join()
#Задаем видеофайл для записи потока
#if isvideo == 1:
	#vfile = vfolder + time.strftime("%d-%m-%Y-%H-%M-%S")+".avi"
	#video = VideoWriter(vfile, VideoWriter_fourcc(*'MP42'), 25.0, (resolh, resolv))

while True:
	#Получаем фрейм от камеры
	stream_ok, frame = webcam.read()

	if stream_ok:
		#Отображение текущего фрейма
		#cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
		#cv2.setWindowProperty(windowName,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
		cv2.namedWindow('Celsus.Videoscope', cv2.WND_PROP_FULLSCREEN)
		cv2.moveWindow('Celsus.Videoscope', 0, 0)
		cv2.setWindowProperty('Celsus.Videoscope', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
		cv2.imshow('Celsus.Videoscope', frame)
		if isvideo == 1:
			#Пишем текущий фрейм в наш файл
			video.write(frame)

		if cv2.waitKey(1) & 0xFF == 27: break

		#Выход из трансляции
		
	
#Освобождаем камеру и закрываем окно
if isvideo == 1:
	video.release()
cv2.destroyAllWindows()
webcam.release()