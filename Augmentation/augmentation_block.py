# data augmentation offline
import os
import albumentations as A
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# adds fog, blur, noise, changes brightness and contrast (all at random)
transformer_fogger = A.Compose([
    A.augmentations.transforms.RandomFog(fog_coef_lower=0.3, fog_coef_upper=0.5, alpha_coef=0.7, p=1),
    A.RandomBrightnessContrast(brightness_limit=0.3, contrast_limit=0.3, p=0.6),
    A.augmentations.transforms.Blur(blur_limit=3, p=0.3),
    A.augmentations.transforms.GaussNoise(var_limit=(10.0, 50.0), mean=0, per_channel=True, p=0.4)
])

# adds snow, blur, noise, changes brightness and contrast (all at random)
transformer_snower = A.Compose([
    A.augmentations.transforms.RandomSnow(snow_point_lower=0.1, snow_point_upper=0.6, brightness_coeff=1.5, p=1),
    A.RandomBrightnessContrast(brightness_limit=0.3, contrast_limit=0.3, p=0.6),
    A.augmentations.transforms.Blur(blur_limit=3, p=0.3),
    A.augmentations.transforms.GaussNoise(var_limit=(10.0, 50.0), mean=0, per_channel=True, p=0.4)
])

# adds blur, noise, changes brightness, rotates and scales image (all at random)
transformer_rotater = A.Compose([
    A.augmentations.geometric.rotate.Rotate(limit=[-30, 30], p=1),
    A.augmentations.geometric.resize.RandomScale(0.3, p=1),
    A.augmentations.transforms.Blur(blur_limit=3, p=0.3),
    A.augmentations.transforms.GaussNoise(var_limit=(10.0, 50.0), mean=0, per_channel=True, p=0.4),
    A.augmentations.transforms.RandomBrightness(limit=0.4, p=0.5)
])

# adds blur, noise, changes brightness and applies geometric transform (all at random)
transformer_affine = A.Compose([
    A.augmentations.geometric.transforms.Affine(p=1),
    A.augmentations.transforms.Blur(blur_limit=3, p=0.3),
    A.augmentations.transforms.GaussNoise(var_limit=(10.0, 50.0), mean=0, per_channel=True, p=0.4),
    A.augmentations.transforms.RandomBrightness(limit=0.4, p=0.7)
])

# adds blur, noise, changes brightness and perspective (all at random)
transformer_perspective = A.Compose([
    A.augmentations.geometric.transforms.Perspective(p=1),
    A.augmentations.transforms.Blur(blur_limit=3, p=0.3),
    A.augmentations.transforms.GaussNoise(var_limit=(10.0, 50.0), mean=0, per_channel=True, p=0.4),
    A.augmentations.transforms.RandomBrightness(limit=0.4, p=0.7)
])


def create_augment_block(transformer, img):
    thresh = transformer(image=img)
    image_transformed = thresh["image"]
    return image_transformed


def augment(path):
    images = os.listdir(path)
    names = 0

    for img in images:
        names += 1

        # convert to RGB to be pretty sure
        img = Image.open(path + "/" + str(img))
        img = img.convert("RGB")
        img = np.array(img)

        for i in range(7):
            # block 1
            plt.imsave(f"{path}/{names}_{str(i)}.png", create_augment_block(transformer_fogger, img))

            # block 2
            plt.imsave(f"{path}/{names}_{str(i + 8)}.png", create_augment_block(transformer_snower, img))

            # block 3
            plt.imsave(f"{path}/{names}_{str(i + 16)}.png", create_augment_block(transformer_rotater, img))

            # block 4
            plt.imsave(f"{path}/{names}_{str(i + 24)}.png", create_augment_block(transformer_affine, img))

            # block 5
            plt.imsave(f"{path}/{names}_{str(i + 32)}.png", create_augment_block(transformer_perspective, img))


"""
This will augment all the images in selected folder
Takes path
Returns nothing but a filled folder with images

Augmentation works like - take one image, apply first transform, save; apply second 
    transform to original image and so on. Repeat 6 more times.
5 blocks of augmentation per image, 7 iterations over loop, so 5 * 7 = 35 images in total from only one.
From 10 images you will get 350, so this may take a while to load. Be careful.
"""
if __name__ == "__main__":
    path_to_files = "C:/Users/Daniil/Desktop/qq"
    augment(path_to_files)
