# 基於YOLO演算法之軌道異物偵測系統
### 主要目標是實作一軌道異物偵測系統，來協助駕駛員盡早發現危險，避免可能發生的危害。 <br />
***
## Table of Contents
* [Hardwares](#hardwares)
* [Flow chart](#flow-chart)
* [Standard Operating Procedures](#standard-operating-procedures)
* [Experiment](#experiment)
* [Features](#features)
* [Training Tools](#training-tools)
* [Contact](#contact)


***
## Hardwares
<table>
  <tr>
    <td>
      <h4> Raspberry Pi 4B </h4>
      <ul>
        <li>SoC：Broadcom BCM2711</li>
        <li>CPU：四核Cortex-A72（ARM v8）@ 1.5GHz</li>
        <li>RAM：4GB(LPDDR4-2400)</li>
        <li>other：Micro HDMI、H.265 (4kp60 decode)</li>
      </ul>
      <img src="https://github.com/gnuhlil/Train-Foreign-Object-Detection-System/assets/79434458/7742fc28-20a0-4b8c-837c-3708663b5182" alt="raspberry pi 4B"  width="395" height="240" />
    </td>
    <td>
      <h4> Raspberry Pi High Quality Camera </h4>
      <ul>
        <li>Sony IMX477R stacked, back-illuminated sensor</li>
        <li>12.3 megapixels</li>
        <li>7.9mm diagonal image size</li>
        <li>1.55 μm × 1.55 μm pixel size</li>
      </ul>
      <img src="https://github.com/gnuhlil/Train-Foreign-Object-Detection-System/assets/79434458/ed983721-a056-4aff-96c5-efa4d0617d60" alt="Camera" width="395" height="240" />
    </td>
  </tr>
</table>


***
## Flow chart
<p align = "center">
<img src="https://github.com/gnuhlil/Project/assets/79434458/56c3a351-0e56-41ae-9e3f-8dea3083b2b2" alt="flow chart"
<p/><br/>


***
## Standard Operating Procedures
1. 一開始透過`cv2.VideoCapture()`讀入影像後，對影像做預處理，透過`cv2.Canny()`產生邊緣偵測的影像。<br/>
<img src="https://github.com/gnuhlil/Project/assets/79434458/e0270f95-b796-4e4e-b655-934ea199433b" alt="First Image" width="395"/> <img src="https://github.com/gnuhlil/Project/assets/79434458/fb0d3582-a503-4254-9a76-f6587dcf025d" alt="Second Image" width="395"/>


2. 由於Webcam架設的位置固定，因此需要根據讀入影像的鐵軌位置來設定`ROI (Region of Interest)`座標。<br/>
<img src="https://github.com/gnuhlil/Project/assets/79434458/fb0d3582-a503-4254-9a76-f6587dcf025d" alt="First Image" width="395"/> <img src="https://github.com/gnuhlil/Project/assets/79434458/d7def93c-8abe-44ad-b359-ed845a9d2fd2" alt="Second Image" width="395"/>


3. 透過`cv2.HoughLinesP`在ROI中實作Line Detection，利用`numpy.ployfit`找到最佳擬合數據點的直線，並根據斜率正負分成左、右線，最後取所有截距和斜率的平均值，透過`getLineCoordinates.py`取得對應的座標，並標示出鐵軌位置。<br/>
<img src="https://github.com/gnuhlil/Project/assets/79434458/d7def93c-8abe-44ad-b359-ed845a9d2fd2" alt="First Image" width="395"/> <img src="https://github.com/gnuhlil/Project/assets/79434458/cf1bbdb4-2809-4ea7-ab2c-d6855d652ec3" alt="Second Image" width="395"/>


4. 以`YOLO`物件偵測模型來偵測異物，這裡提供兩種偵測方式，**Option 1**是偵測整張畫面，對於偵測到的每個物體，再以物體座標和鐵軌線的line detection判斷是否有侵入鐵軌，**Option 2**是只偵測ROI的區域，因為ROI就是鐵軌所在的區域，只要偵測到物體就代表已侵入到鐵軌，若異物入侵鐵軌則會以聲音來警示駕駛員。
* **Option 1** <br />
<img src="https://github.com/gnuhlil/Project/assets/79434458/cf1bbdb4-2809-4ea7-ab2c-d6855d652ec3" alt="First Image" width="395"/> <img src="https://github.com/gnuhlil/Project/assets/79434458/b1e70d38-0b46-4388-819e-e53cc86e3cb8" alt="Second Image" width="395"/>
* **Option 2** <br />
<img src="https://github.com/gnuhlil/Project/assets/79434458/cf1bbdb4-2809-4ea7-ab2c-d6855d652ec3" alt="First Image" width="395"/> <img src="https://github.com/gnuhlil/Project/assets/79434458/db3c583f-d022-491c-9f05-78699adb69ad" alt="Second Image" width="395"/>


***
## Experiment
<img src="https://github.com/gnuhlil/Train-Foreign-Object-Detection-System/assets/79434458/aad6d1c5-bcf3-475f-b2fc-081fcb56bb14" alt="image" width="395" height="240" />
<img src="https://github.com/gnuhlil/Train-Foreign-Object-Detection-System/assets/79434458/c276d234-cf66-4f2a-8193-fd9b9bca6ddd" alt="image" width="395" height="240" />


***
## Features
* YOLO其最大的特點是運算速度快，可以用於實時系統。
  * 在實時物件偵測環境下，能同時兼顧精準度和運算速度的話更好，而我使用的是`yolov4-Tiny`。
    
    || COCO mAP(0.5) | FLOPs | Weight Size |
    | -------- | -------- | -------- | -------- |
    | yolov4-Tiny  | 40.2%  | 6.9 BFlops  | 23.1M  |
    | yolo-fastest-1.1-xl  | 34.33%  | 0.725BFlops  | 3.7M  |

    Reference：<https://github.com/dog-qiuqiu/Yolo-Fastest>

    
* 因為火車Webcam架設的位置固定，可用設定座標的方式來圈選出鐵軌所在的區域，讓結果能更加明確，也能節省處理不必要區域的時間。
* YOLO兩種偵測方式可以根據不同情境來選擇是否需要偵測鐵軌以外的異物。


***
## Training Tools
* **OpenCV DNN Model**
* **MS COCO(Common Objects in Context) dataset**
* **Yolov4-Tiny.cfg**、**Yolov4-Tiny.weight**
* **Railway Track Videos**


***
## Contact
👋**Tse-Hung Kung** <br/>
✉**as115582038@gmail.com**
