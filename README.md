# Image Restoration Using AI (Real-ESRGAN and DeOldify)

This is a Image restoration tool created with the help of [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) used for enhancing image resolution and faces (utilizes [GFPGAN](https://github.com/TencentARC/GFPGAN) internally) and [Deoldify](https://github.com/jantic/DeOldify) used for colorizing images, built with Flask web application as UI.

<br>
Real-ESRGAN : https://github.com/xinntao/Real-ESRGAN<br>
Deoldify : https://github.com/jantic/DeOldify<br><br>

This projcet was inspired by youtuber Nicholas Renotte's Real-ESRGAN and Deoldify videos.<br>
Go checkout his YouTube channel for some amazing Data Science content - https://www.youtube.com/c/NicholasRenotte

## ⚡ Example Results

<img src="https://user-images.githubusercontent.com/37840005/158203902-6b0115d8-8197-4b07-b032-bc9a22c7a99b.jpg" width="300" height="400" />

Original

<img src="https://user-images.githubusercontent.com/37840005/158204087-3be9af37-5b1b-479b-bb50-2f8db363ada1.jpg" width="500" height="600" />

High Resolution, Real-ESRGAN

<img src="https://user-images.githubusercontent.com/37840005/158205119-05f3b12d-1175-4a2e-bb44-6d60d5a58b3a.jpg" width="500" height="600" />

Colorized - Deoldify

![tiger b w](https://user-images.githubusercontent.com/37840005/158205633-38cf4b37-5571-4925-a13e-20c54bc1c3e6.jpg)

Original

![tiger_high_res](https://user-images.githubusercontent.com/37840005/158205670-a5da3add-331f-4ddc-8722-a4f086a9472a.jpg)

High Resolution, Real-ESRGAN

![tiger_colored](https://user-images.githubusercontent.com/37840005/158205713-9b539bd2-1dda-426c-aa6a-18a9e6caaf6a.jpg)

Colorized - Deoldify

## 🖥️ Flask UI Demo

![demo](https://user-images.githubusercontent.com/37840005/158206153-e89ce0fa-2fb5-4f0d-87bb-d47ec5d7de35.gif)

## 🔧 Dependencies and Installation
* Python
* [PyTorch + CUDA](https://pytorch.org/get-started/locally/)
* Flask
* BeautifulSoup
* OpenCV

### Installation

1.&nbsp;&nbsp;Get the repo
```
Clone repo or downlaod code - "https://github.com/VaisakNair7/Image-Restoration-using-AI"
cd Image-Restoration-using-AI/src/Real-ESRGAN 
OR clone/download Real-ESRGAN repo from "https://github.com/xinntao/Real-ESRGAN" and place it inside "src" folder
```
    
2.&nbsp;&nbsp;Setup Real-ESRGAN 
```
!pip install basicsr
!pip install facexlib
!pip install gfpgan
!pip install -r requirements.txt
!python setup.py develop

Download pre-trained model, RealESRGAN_x4plus.pth and place it inside experiments/pretrained_models
```
&nbsp;&nbsp;&nbsp;[RealESRGAN_x4plus.pth](https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth)<br><br>
&nbsp;&nbsp;&nbsp;If you face any difficulty in setting up Real-ESRGAN check their [github repo](https://github.com/xinntao/Real-ESRGAN) for installation details.<br>

3.&nbsp;&nbsp;Setup DeOldify
```  
cd ../Deoldify 
OR clone/download DeOldify repo from "https://github.com/jantic/DeOldify" and place it inside "src" folder

!pip install -r requirements.txt

Create "models" folder if not alredy present 
Downlaod Artsitic and Stable model
Place both models inside "models" folder
```
&nbsp;&nbsp;&nbsp;[Artistic Model](https://data.deepai.org/deoldify/ColorizeArtistic_gen.pth)<br>
&nbsp;&nbsp;&nbsp;[Stable Model](https://www.dropbox.com/s/usf7uifrctqw9rl/ColorizeStable_gen.pth?dl=0)<br><br>
&nbsp;&nbsp;&nbsp;If you face any difficulty in setting up DeOldify check their [github repo](https://github.com/jantic/DeOldify) for installation details.<br>

4.&nbsp;&nbsp;Run app.py
```
cd ../..

python app.py
```
  
## 📧 Contact
E-mail : vaisaksnair98@gmail.com <br>
LinkedIn : https://www.linkedin.com/in/vaisaksnair/ <br>
GitHub : https://github.com/VaisakNair7
    


