# Augmentation 

### In the following file you can find a function that creates augmentation blocks for transforming images

![augmentation](augment.gif)

#### How it works

The complete finction consists of 5 blocks of augmentation, and it applies 5 different random transformations to each image in a folder and repeats for 7 times. Returns 5 * 7 = 35 images from only one image, so be careful because it can take a while to load (10 images gives you 350 images in total after you run this function)

#### What I used and why 

Mostly I used Albumentations library with its' transformations. It consists of 5 blocks and each block include random brightness, contrast, blur and noise levels:
* RandomFog - addds some fog to the image;
* RandomSnow - adds the effect of snow on the image;
* Rotate + RandomScale - rotates the image to left or right by at maximum 30 degrees and changes image's quality;
* Affine - geometrically changes the image's shape to make it look unique;
* Perspective - changes the perspective of the image, making it unique as well.