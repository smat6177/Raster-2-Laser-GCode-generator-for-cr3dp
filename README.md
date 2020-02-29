# Various Inkscape extensions
 - Raster 2 Laser GCode for cr3dp
 
#Descriptions
- Raster 2 Laser GCode generator is an extension to generate Gcode for a laser cutter/engraver (or pen plotter), it can generate various type of outputs from a simple B&W (on/off) to a more detailed Grayscale (pwm)
- Raster 2 Laser GCode for cr3dp is an extension revision from Raster 2 Laser GCode generator to suit for Creality 3d print


#Installing:

Simply copy all the files in the folder "Extensions" of Inkscape

>Windows ) "C:\<...>\Inkscape\share\extensions"

>Linux ) "/usr/share/inkscape/extensions"

>Mac ) "/Applications/Inkscape.app/Contents/Resources/extensions"


for unix (& mac maybe) change the permission on the file:

>>chmod 755 for all the *.py files

>>chmod 644 for all the *.inx files



#Usage of "Raster 2 Laser GCode generator":

[Required file: png.py / raster2laser_gcode_4_cr3dp.inx / raster2laser_gcode_4_cr3dp.py]

- Step 1) Resize the inkscape document to match the dimension of your working area on the laser cutter/engraver (Shift+Ctrl+D) 

- Step 2) Draw or import the image

- Step 3) To run the extension go to: Extension > 305 Engineering > Raster 2 Laser GCode for cr3dp

- Step 4) Play!

#Note
I have created all the file except for png.py , see that file for details on the license

詳細使用介紹，請參見 黃聖順老師的隨便記記 
http://smathuang.cc/wordpress/2019/02/13/605/

2016/10/25 修正灰階模式下，黑色區域錯誤解析成白色的問題。

2016/10/23 更新內容：
1.增加灰階模式下對比值設定。
2.增加不需雷雕區域的移動速度。
3.增加預設XYZ值，及自動定位到預設位置選項。
4.不需手動調整XYZ軸了。SD直接插入CR8就可Print From SD開始雷雕。
變得很方便使用了。

2016/11/01 增加 Default Position 雷雕前開啟弱光雷射並暫停動作，讓使用者可以定位待雕材料

2017/02/14 增加 No Homing 雷雕前開啟弱光雷射並暫停動作，讓使用者可以定位待雕材料

2017/02/26 Disable G04 in grayscale

2017/12/12 更新內容：
1.修正 add numeric suffix to filename 未勾選時的執行錯誤
2.增加以弱光雷射原點及弱光掃描矩形邊框的定位功能選項
3.調整選單順序

2018/03/22 更新內容：
1.弱光掃描矩形邊框的定位功能選項改為下拉式選單，讓使用者可以決定掃描次數 0 到 5次
2.修正部分中文翻譯

2019/02/13 更新內容：
1.取消弱光雷射定位功能。
2.增加最高雷射功率設定。
3.以[G4 S3]暫停3秒指令,取代[M0]暫停指令，以讓沒有控制旋鈕的機型可以使用。
目前止程式在 cr7/8/10sPro 及Ender-3 試用正常。

2019/06/08 更新內容：
1.調高對比限制，由10調高至20。
2.Enable G04 in grayscale.
3.增加Homeing 3:G28 X Y ,只歸零XY並移至預設位置XY。

2019/06/21 更新內容：
修正Homeing 3:「G28 X Y;」指令,為「G28 X; G28 Y;」。

2019/07/27 更新內容：
新增「指示雷射功率Power of indicator laser」設定功能，原本的功率固定為4，對部分機器而言太強，顯示工作範圍時，會在物件上雕出細痕，對部分機器卻又太小，以致於不能打開雷射光，無法顯示工作區範圍。

2019/09/29 更新內容：
1.顯示工作區範圍增加「顯示定位點10秒」選項。
2.優化灰階輸出圖形的計算方式。

2019/10/05 更新內容：
灰階以外的B/W模式時,本來預設是輸出最大功率255，修改成可以依照Laser Max Power的設定來輸出功率。

2019/10/20 更新內容：
將「顯示定位點10秒」的雷射光點改成閃爍雷射光點，以降低對待雕物件的損傷。
