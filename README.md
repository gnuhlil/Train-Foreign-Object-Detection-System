# 基於YOLO演算法之軌道異物偵測系統
### 主要目標是實作一軌道異物偵測系統，用來協助駕駛員盡早發現危險狀況，避免可能發生的危害

***
#### 流程步驟
1. 一開始透過Camera讀入影像後，對影像做預處理，透過cv2.Canny()產生邊緣偵測的影像<br/>
<img src="https://github.com/gnuhlil/Project/assets/79434458/e0270f95-b796-4e4e-b655-934ea199433b" alt="First Image" width="395"/> <img src="https://github.com/gnuhlil/Project/assets/79434458/fb0d3582-a503-4254-9a76-f6587dcf025d" alt="Second Image" width="395"/>
2. 用設定座標的方式來圈選出鐵軌所在的區域為ROI (Region of Interest)，讓結果能更加明確，也能節省處理不必要區域的時間<br/>
<img src="https://github.com/gnuhlil/Project/assets/79434458/fb0d3582-a503-4254-9a76-f6587dcf025d" alt="First Image" width="395"/> <img src="https://github.com/gnuhlil/Project/assets/79434458/d7def93c-8abe-44ad-b359-ed845a9d2fd2" alt="Second Image" width="395"/>
3. 透過cv2.HoughLinesP在ROI中實作line detection，標示出鐵軌位置<br/>
<img src="https://github.com/gnuhlil/Project/assets/79434458/d7def93c-8abe-44ad-b359-ed845a9d2fd2" alt="First Image" width="395"/> <img src="https://github.com/gnuhlil/Project/assets/79434458/cf1bbdb4-2809-4ea7-ab2c-d6855d652ec3" alt="Second Image" width="395"/>
4. 接著，以YOLO物件偵測模型來偵測異物，這裡提供兩種偵測方式，第一種是偵測整張畫面，對於偵測到的每個物體，再以物體座標和鐵軌線的直線方程式判斷是否有侵入鐵軌，第二種是只偵測ROI的區域，因為ROI就是鐵軌所在的區域，只要偵測到物體就代表已侵入到鐵軌；若異物入侵鐵軌則會以聲音來警示駕駛員。在程式執行中會持續輸出畫面以供駕駛員參考，畫面中會標示鐵軌線以及框出偵測到的物體。
<img src="https://github.com/gnuhlil/Project/assets/79434458/cf1bbdb4-2809-4ea7-ab2c-d6855d652ec3" alt="First Image" width="395"/> <img src="" alt="Second Image" width="395"/>

![GITHUB](https://github.com/gnuhlil/Project/assets/79434458/56c3a351-0e56-41ae-9e3f-8dea3083b2b2)

*引用darknet的coco.names*
