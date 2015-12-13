#!/usr/bin/env python 
import os

directory = os.getcwd()
target_pdf = directory+'/pdfs'
target_mp3 = directory+'/Music'
target_img = directory+'/Pictures'
target_zip = directory+'/zip'
target_docs = directory+'/docs'


if not os.path.exists(target_pdf):
	os.makedirs(target_pdf)
if not os.path.exists(target_mp3):
	os.makedirs(target_mp3)
if not os.path.exists(target_img):
	os.makedirs(target_img)
if not os.path.exists(target_zip):
	os.makedirs(target_zip)
if not os.path.exists(target_docs):
	os.makedirs(target_docs)

print("Scanning Files")

for file in os.listdir(directory):
	if(file.endswith('.mp3')):
		os.rename(''+directory+'/'+file,''+target_mp3+'/'+file)
	elif(file.endswith('.pdf')):
		os.rename(''+directory+'/'+file,''+target_pdf+'/'+file)
	elif(file.endswith('.png') or file.endswith('.jpg') or file.endswith('jpeg')):
		os.rename(''+directory+'/'+file,''+target_img+'/'+file)
	elif(file.endswith('.zip')):
		os.rename(''+directory+'/'+file,''+target_zip+'/'+file)
	elif(file.endswith('.docx') or file.endswith('doc')):
		os.rename(''+directory+'/'+file,''+target_docs+'/'+file)

print("Done!")
