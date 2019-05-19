import skimage.draw
import numpy as np
import itertools
import skimage.io
import cv2
import os
import argparse
from skimage.viewer import ImageViewer

def num_in_name(ele):
	"""name parser for the output video"""
	return int(ele.split('.')[0].split('_')[-1])
	
def bg_mask(dir_path,save_path):
	for f in os.listdir(dir_path):
		if f.endswith('png'):
			print(f)
			img = skimage.io.imread('{}/{}'.format(dir_path,f))
			for i in range(0,len(img)):
				for a in range(0,len(img[i])):
					if img[i][a] ==0:
						img[i][a]=255
					else:
						img[i][a]=0
			#viewer = ImageViewer(img)
			#viewer.show()
			if not os.path.exists(save_path):
				os.makedirs(save_path)
			skimage.io.imsave('{}/{}'.format(save_path,f), img)

def crop(crop_mask, ori_img, crop_save):
	#read in resource
	for f in os.listdir(crop_mask):
		if f.endswith('png'):
			print(f)
			src1_mask = cv2.imread('{}/{}'.format(crop_mask,f),0)
			src1      = cv2.imread('{}/{}'.format(ori_img,f),1)
			print(src1.shape)		

			#put mask on the image 
			#change mask to a 3 channel image 
			src1_mask=cv2.cvtColor(src1_mask,cv2.COLOR_GRAY2BGR)
			mask_out=cv2.subtract(src1_mask,src1)
			mask_out=cv2.subtract(src1_mask,mask_out)
			print(mask_out.shape)		

			if not os.path.exists(crop_save):
				os.makedirs(crop_save)
			#cv2.imshow('image',mask_out)
			cv2.imwrite('{}/{}'.format(crop_save, f),mask_out)
			#cv2.waitKey(0)
			#cv2.destroyAllWindows()

def overlap(from_img, to_img, masker,ind):
	# Load two images
	img1 = cv2.imread(from_img)
	img2 = cv2.imread(to_img)
	#print(img1.shape)
	#print(img2.shape)
	# I want to put logo on top-left corner, So I create a ROI
	rows,cols,channels = img2.shape
	roi = img1[0:rows, 0:cols]
	# Now create a mask of logo and create its inverse mask also
	img2gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
	ret, mask1 = cv2.threshold(img2gray, 0, 255, cv2.THRESH_BINARY)
	#print(mask1.shape)
	mask = cv2.imread(masker,0)
	mask_inv = cv2.bitwise_not(mask)	
	# Now black-out the area of logo in ROI
	img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)	
	# Take only region of logo from logo image.
	img2_fg = cv2.bitwise_and(img2,img2,mask = mask)
	# Put logo in ROI and modify the main image
	dst = cv2.add(img1_bg,img2_fg)
	img1[0:rows, 0:cols ] = dst
	#cv2.imshow('res',img1)
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()
	cv2.imwrite('./result3/out_{}.png'.format(ind),img1)

def linker(frame_path, save_path):
	dir_path = frame_path
	ext = 'png'

	images = []
	for f in os.listdir(dir_path):
		if f.endswith(ext):
			#print(f)
			images.append(f)
	images.sort(key=num_in_name)
	print(images)
	#print(len(images))
	# Determine the width and height from the first image
	image_path = os.path.join(dir_path, images[0])
	frame = cv2.imread(image_path)
	#cv2.imshow('video',frame)
	height, width, channels = frame.shape	

	# Define the codec and create VideoWriter object
	fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Be sure to use lower case
	out = cv2.VideoWriter(save_path, fourcc, 20.0, (width, height))	

	for image in images:	

		image_path = os.path.join(dir_path, image)
		frame = cv2.imread(image_path)	

		out.write(frame) # Write out frame to video	

		#cv2.imshow('video',frame)
		if (cv2.waitKey(1) & 0xFF) == ord('q'): # Hit `q` to exit
			break	

	# Release everything if job is finished
	out.release()
	cv2.destroyAllWindows()	

	print("The save_path video is {}".format(save_path))

#for i in range(1,52):
#	overlap('./object/the_simpsons_12/the_simpsons_12_frame_{}.png'.format(i),'./result2/out_{}.png'.format(i),
#		'./mask/the_simpsons_12_bg/the_simpsons_12_frame_{}.png'.format(i),i)
#	overlap('./object/the_simpsons_4/the_simpsons_4_frame_{}.png'.format(i), './result2/out_{}.png'.format(i),
#		'./mask/the_simpsons_4_bg/the_simpsons_4_frame_{}.png'.format(i),i)
#	overlap('./object/the_simpsons_17/the_simpsons_17_frame_{}.png'.format(i), 
#			'./bg/the_simpsons_18/the_simpsons_18_frame_{}.png'.format(i),
#			'./mask/the_simpsons_17_bg/the_simpsons_17_frame_{}.png'.format(i),i)


#if __name__ == "__main__":
#	print('------Setup parameters------')
#	parser = argparse.ArgumentParser(description = 'Process the command.')
#	parser.add_argument('--index',required = True ,type=int)
#	#parser.add_argument('--output-video-path',type=str)
#	parser.add_argument('--extension', default='png',type=str)
#	parser.add_argument('--component-path',type=str)
#	parser.add_argument('--component-save', type=str)
#	args = parser.parse_args()
#	obj_mask_dir_path = './mask/the_simpsons_{}'.format(args.index)
#	origin_img_path   = './frames/the_simpsons_{}'.format(args.index)
#	bg_mask_save_path = './mask/'+obj_mask_dir_path.split('/')[-1]+'_bg'
#	bg_save_path      = './bg/'+obj_mask_dir_path.split('/')[-1]
#	obj_save_path     = './object/'+obj_mask_dir_path.split('/')[-1]
#	bg_mask(obj_mask_dir_path, bg_mask_save_path)
#	#bg
#	crop(bg_mask_save_path, origin_img_path, bg_save_path)
#	#obj
#	crop(obj_mask_dir_path, origin_img_path, obj_save_path)
#	linker(args.component_path,args.component_save)
linker('./result3/','./good5.mp4')














