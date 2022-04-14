import random
import os


def create_test(initial_path, test_path):
    # create test folder
    os.mkdir(test_path)

    # loop through all folders in train
    for folder in os.listdir(initial_path):
        # create list to store images
        images_to_choose = []

        # loop through images and store them to the list
        for img in os.listdir(f"{initial_path}/{folder}"):
            images_to_choose.append(img)

        # run randomly removing 7 images from each folder to test set
        for i in range(7):
            pic = random.choice(images_to_choose)
            images_to_choose.remove(pic)
            os.replace(f"{initial_path}/{folder}/{pic}",
                       f"{test_path}/{pic}_{str(folder)}.png")
    print("Successfully Done")


"""
This will create a test folder by randomly choosing 7 images from train folder (removing them)
    to avoid data leakage.
Take path to train folder and path to future test folder (it will be created).
"""
if __name__ == "__main__":
    path_to_files = "C:/Users/Daniil/Desktop/qq"
    path_to_test = "C:/Users/Daniil/Desktop/test"

    create_test(path_to_files, path_to_test)
