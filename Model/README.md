# CNN Model 

### In this part of repository you can find the realization of CNN model and training, its' weights, prediction function that is used in Bot

#### You can find:

* config.py with all params used while training;
* model.json - .json file with model;
* model.py - realization of model in tensorflow + keras with training;
* model_predict.py - loading model and adding weights from file with prediction function used in Bot;
* weights.h5 - model weights that can be used instead of training model.

CNN architecture (+ online augmentation, 30 epochs and learning rate 0.001):
* Block_1 - ConvD2 + Conv2D + MaxPool2D + BatchNormalization;
* Block_2 - ConvD2 + Conv2D + MaxPool2D + BatchNormalization;
* Block_3 - Flatten + Dense + BatchNormalization + Dropout;
* Output - Dense.

P.S. To see complete description of model, its' building and scorings read README in "Notebook" directory.