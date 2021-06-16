# Final


首先，先用line detection偵測直線，來定義方向。過了直線後，就利用偵測Apriltag，來控制移動方向。最後，由於和Apriltag的距離小於15，車子因此停止並同時利用Xbee回傳K來代表完成整段路徑。
