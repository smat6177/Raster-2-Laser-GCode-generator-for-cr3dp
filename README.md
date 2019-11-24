# Various Inkscape extensions
 - Raster 2 Laser GCode for cr8
 
#Descriptions
- Raster 2 Laser GCode generator is an extension to generate Gcode for a laser cutter/engraver (or pen plotter), it can generate various type of outputs from a simple B&W (on/off) to a more detailed Grayscale (pwm)
- Raster 2 Laser GCode for cr8 is an extension revision from Raster 2 Laser GCode generator to suit for 3d print cr-8


#Installing:

Simply copy all the files in the folder "Extensions" of Inkscape

>Windows ) "C:\<...>\Inkscape\share\extensions"

>Linux ) "/usr/share/inkscape/extensions"

>Mac ) "/Applications/Inkscape.app/Contents/Resources/extensions"


for unix (& mac maybe) change the permission on the file:

>>chmod 755 for all the *.py files

>>chmod 644 for all the *.inx files



#Usage of "Raster 2 Laser GCode generator":

[Required file: png.py / raster2laser_gcode.inx / raster2laser_gcode.py]

- Step 1) Resize the inkscape document to match the dimension of your working area on the laser cutter/engraver (Shift+Ctrl+D) 

- Step 2) Draw or import the image

- Step 3) To run the extension go to: Extension > 305 Engineering > Raster 2 Laser GCode generator / Raster 2 Laser GCode for cr8

- Step 4) Play!




#Note
I have created all the file except for png.py , see that file for details on the license

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

