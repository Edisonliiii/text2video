###Text to Video Generation

1. You need to have CoreNLP to run NLP component
2. Download: git clone https://github.com/artpar/languagecrunch.git
		       git clone https://github.com/Lambda-3/Graphene.git
    and make them compile, they are a bit big.
3. Set up Mask R-CNN in your environment. And download mask_rcnn_coco.h5

------ Use languagecrunch and Graphene to setup LSTM readin API.(I can not do this for you since they are too complicated)

------ run crop_origin_to_frames_and_video.py based on the arguments inside.

------ run train_api.py to start the splash and separate the object and the background

------ run convertor.py let it setup every thing to generate the final video


I also remain some evidence to prove my work in Video folder. Enjoy ! Thx!
