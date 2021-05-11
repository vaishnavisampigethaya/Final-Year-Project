def main():
    from keras.layers import Input,Lambda,Dense,Flatten
    from keras.models import Model
    from keras.applications.vgg16 import VGG16
    from keras.applications.vgg16 import preprocess_input
    from keras.preprocessing import image
    from keras.preprocessing.image import ImageDataGenerator
    from keras.models import Sequential
    import numpy as np
    from glob import glob
    import matplotlib.pyplot as plt
    import os
    import cv2
    import tensorflow as tf
    from keras.applications.vgg16 import decode_predictions

    categories=['train','test']
    categories1=['without_mask','with_mask']
    data1=[]
    for category in categories1:
        path=os.path.join('../../../../Dataset',category)
        label1=categories1.index(category)
        for file in os.listdir(path):
           img_path=os.path.join(path,file)
           img=cv2.imread(img_path)
           img=cv2.resize(img,(224,224))
           data1.append([img,label1])

    data=[]
    cate=[]
    for category in categories:
        path=os.path.join('Dataset',category)
        for file in os.listdir(path):
            if not file.startswith('.'):
                img_path=os.path.join(path,file)
                cate.append(file)
                label=cate.index(file)
                files=os.listdir(img_path)
                for i in files:
                    p=os.path.join(img_path,i)
                    img_path=os.path.join(path,file)
                    #print(p)
                    img=cv2.imread(p)
                    img=cv2.resize(img,(224,224))
                    data.append([img,label])

    import random
    random.shuffle(data1)
    x1=[]
    y1=[]
    for features1,label1 in data1:
        x1.append(features1)
        y1.append(label1)

    import numpy as np

    x1=np.array(x1)
    y1=np.array(y1)

    x1.shape
    y1.shape

    x1=x1/255
    x1[0]
    from sklearn.model_selection  import train_test_split
    x_train1,x_test1,y_train1,y_test1=train_test_split(x1,y1,test_size=0.2)
    x_train1.shape
    x_test1.shape
    from tensorflow.keras.applications.vgg16 import VGG16
    vgg1=VGG16()
    vgg1.summary()

    from keras import Sequential
    model1=Sequential()
    for layer in vgg1.layers[:-1]:
        model1.add(layer)

    model1.summary()
    for layer in model1.layers:
        layer.trainable=False

    model1.summary()
    from keras.layers import Dense

    model1.add(Dense(1,activation='sigmoid'))
    model1.summary()
    model1.compile(optimizer='Adam',loss='binary_crossentropy',metrics=['accuracy'])
    model1.fit(x_train1,y_train1,epochs=3,validation_data=(x_test1,y_test1))
    h=(int(len(cate)/2))
    del cate[:h]
    print(cate)
    print(len(cate))
    random.shuffle(data)
    x=[]
    y=[]
    for features,label in data:
        x.append(features)
        y.append(label)
    x=np.array(x)
    y=np.array(y)
    x.shape
    y.shape
    x=x/255
    x[0]
    from sklearn.model_selection  import train_test_split
    x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2)
    x_train.shape
    x_test.shape
    vgg=VGG16()
    vgg.summary()
    from keras import Sequential
    model=Sequential()
    for layer in vgg.layers[:-1]:
        model.add(layer)

    model.summary()
    for layer in model.layers:
        layer.trainable=False

    model.summary()

    model.add(Dense(len(cate),activation='softmax'))

    model.summary()
    model.compile(optimizer='Adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])
    model.fit(x_train,y_train,epochs=5,validation_data=(x_test,y_test))
    cap=cv2.VideoCapture(0)
    while True:
        ret,frame=cap.read()
        img=cv2.resize(frame,(224,224))
        img=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        coord=haar.detectMultiScale(img)
        coord1=coord=haar1.detectMultiScale(img)
        haar=cv2.CascadeClassifier('haarcascade_eye.xml')
        haar1=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        for x,y,w,h in coord:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        for x,y,w,h in coord1:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        y_pred1=model1.predict_classes(img.reshape(1,224,224,3))
        y_pred=int(model.predict_classes(img.reshape(1,224,224,3)))
        str1=""
        if y_pred1[0][0]==0:
            str1="No Mask "+cate[y_pred]
        else:
            str1="With Mask "+cate[y_pred]
        print(y_pred)
        pos=(30,30)
        bg_color=(0,0,255)
        text_size=cv2.getTextSize(str1,cv2.FONT_HERSHEY_SIMPLEX,1,cv2.FILLED)
        end_x=pos[0]+text_size[0][0]+2
        end_y=pos[1]+text_size[0][1]-2
        cv2.rectangle(frame,pos,(end_x,end_y),bg_color,cv2.FILLED)
        cv2.putText(frame,str1,pos,cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),1,cv2.LINE_AA)
        cv2.imshow('window',frame)
        return str1
        if cv2.waitKey(1) & 0xFF== ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()



