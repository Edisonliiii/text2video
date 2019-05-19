import cv2
import argparse
import subprocess
import os

def num_in_name(ele):
	"""name parser for the output video"""
	return int(ele.split('.')[0].split('_')[-1])

def cut_video(input_path,from_point, to_point):
	"""extract the single frames"""
	vidcap = cv2.VideoCapture(input_path)
	target_store_dir_name = os.path.splitext(input_path)[0]
	target_store_dir_name = target_store_dir_name.split('/')
	target_store_dir_name = target_store_dir_name[-1]
	success,image = vidcap.read()
	count = 0
	count_for_name=0
	success = True

	store_path = './frames/{}/'.format(target_store_dir_name)
	os.makedirs(store_path)
	#filelist = glob.glob(os.path.join(mydir, "*.jpg"))
	#for f in filelist:
	#	os.remove(f)
	while success:
		if count>=from_point and count<=to_point:
			count_for_name+=1
			cv2.imwrite("{}{}_frame_{}.png".format(store_path, target_store_dir_name, count_for_name), image)
		success,image = vidcap.read()
		#print('Read a new frame: ', success)
		count += 1
		if count>to_point:
			success = False
	return_list=[]
	return_list.append(store_path)
	return_list.append(target_store_dir_name)
	return return_list

def connect_frames2video(path_list,extension_str):
	"""link the frames together"""
	# Arguments
	dir_path = path_list[0]
	ext = extension_str
	output = './output_video/{}.mp4'.format(path_list[1])

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
	out = cv2.VideoWriter(output, fourcc, 20.0, (width, height))	

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

	print("The output video is {}".format(output))

if __name__ == "__main__":
	print('------Setup parameters------')
	parser = argparse.ArgumentParser(description = 'Process the command.')
	parser.add_argument('--video-source', required = True, type = str)
	parser.add_argument('--video-index', required = True, type = int)
	parser.add_argument('--input-video', type=str)
	parser.add_argument('--from-which', type=int)
	parser.add_argument('--to-which', type=int)
	#parser.add_argument('--output-video-path',type=str)
	parser.add_argument('--extension', default='png',type=str)
	args = parser.parse_args()
	print('---------------Download videos--------------')
	args.input_video = './video/the_simpsons_{}.mp4'.format(args.video_index)
	subprocess.call(['youtube-dl','-o',args.input_video,'-f','mp4',args.video_source])
	print('------------Cut video into frame you want frame based----------')
	get_for_output = cut_video(args.input_video, args.from_which, args.to_which)
	print('------------link into video---------------')
	connect_frames2video(get_for_output, args.extension)

