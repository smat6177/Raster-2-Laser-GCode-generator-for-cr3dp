'''
# ----------------------------------------------------------------------------
# Copyright (C) 2014 305engineering <305engineering@gmail.com>
# Original concept by 305engineering.
#
# "THE MODIFIED BEER-WARE LICENSE" (Revision: my own :P):
# <305engineering@gmail.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff (except sell). If we meet some day, 
# and you think this stuff is worth it, you can buy me a beer in return.
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ----------------------------------------------------------------------------
'''


import sys
import os
import re

sys.path.append('/usr/share/inkscape/extensions')
sys.path.append('/Applications/Inkscape.app/Contents/Resources/extensions') 

import subprocess
import math

import inkex
import png
import array


class GcodeExport(inkex.Effect):

######## 	Richiamata da _main()
	def __init__(self):
		"""init the effetc library and get options from gui"""
		inkex.Effect.__init__(self)
		
		# Opzioni di esportazione dell'immagine
		self.OptionParser.add_option("-d", "--directory",action="store", type="string", dest="directory", default="",help="Directory for files") ####check_dir
		self.OptionParser.add_option("-f", "--filename", action="store", type="string", dest="filename", default="-1.0", help="File name")            
		self.OptionParser.add_option("","--add-numeric-suffix-to-filename", action="store", type="inkbool", dest="add_numeric_suffix_to_filename", default=True,help="Add numeric suffix to filename")            
		self.OptionParser.add_option("","--bg_color",action="store",type="string",dest="bg_color",default="",help="")
		self.OptionParser.add_option("","--resolution",action="store", type="int", dest="resolution", default="1",help="") #Usare il valore su float(xy)/resolution e un case per i DPI dell export
		
		
		# Come convertire in scala di grigi
		self.OptionParser.add_option("","--grayscale_type",action="store", type="int", dest="grayscale_type", default="1",help="") 
		
		# Modalita di conversione in Bianco e Nero 
		self.OptionParser.add_option("","--conversion_type",action="store", type="int", dest="conversion_type", default="1",help="") 
		
		# Opzioni modalita 
		self.OptionParser.add_option("","--BW_threshold",action="store", type="int", dest="BW_threshold", default="128",help="") 
		self.OptionParser.add_option("","--grayscale_resolution",action="store", type="int", dest="grayscale_resolution", default="1",help="") 
		
		#Velocita Nero e spostamento
		self.OptionParser.add_option("","--speed_OFF",action="store", type="int", dest="speed_OFF", default="2000",help="") 
		self.OptionParser.add_option("","--speed_ON",action="store", type="int", dest="speed_ON", default="500",help="") 

		# Mirror Y
		self.OptionParser.add_option("","--flip_y",action="store", type="inkbool", dest="flip_y", default=False,help="")
		
		# Homing
		self.OptionParser.add_option("","--homing",action="store", type="int", dest="homing", default="1",help="")

		#add by smat
		self.OptionParser.add_option("","--active-tab",action="store", type="string",dest="active_tab", default='title', help="Active tab.")# use a legitmate default
		self.OptionParser.add_option("","--x_adjust",action="store", type="string", dest="x_adjust", default="45",help="") 
		self.OptionParser.add_option("","--y_adjust",action="store", type="string", dest="y_adjust", default="10",help="") 
		self.OptionParser.add_option("","--z_adjust",action="store", type="string", dest="z_focus", default="50",help="") 
		self.OptionParser.add_option("","--laser_contrast",action="store", type="int", dest="laser_contrast", default="3",help="set 1 to the lightest effect.") 
		#self.OptionParser.add_option("","--low_laser_dot",action="store", type="inkbool", dest="low_laser_dot", default=True,help="")
		#self.OptionParser.add_option("","--low_laser_square",action="store", type="inkbool", dest="low_laser_square", default=False,help="")
		self.OptionParser.add_option("","--low_laser_square",action="store", type="int", dest="low_laser_square", default="0",help="")
		self.OptionParser.add_option("","--low_laser_power", action="store", type="int", dest="low_laser_power", default="1", help="Indicator light") # add by smat 20190727

		# Commands
		self.OptionParser.add_option("","--laseron", action="store", type="string", dest="laseron", default="M106", help="")
		self.OptionParser.add_option("","--laseroff", action="store", type="string", dest="laseroff", default="M107", help="")

		self.OptionParser.add_option("","--laseron_delay", action="store", type="int", dest="laseron_delay", default="0", help="")
		self.OptionParser.add_option("","--laser_mini_power", action="store", type="int", dest="laser_mini_power", default="50", help="")
		self.OptionParser.add_option("","--laser_max_power", action="store", type="int", dest="laser_max_power", default="255", help="")
		
		
		# Anteprima = Solo immagine BN 
		self.OptionParser.add_option("","--preview_only",action="store", type="inkbool", dest="preview_only", default=False,help="") 

		#inkex.errormsg("BLA BLA BLA Messaggio da visualizzare") #DEBUG


		
		
######## 	Richiamata da __init__()
########	Qui si svolge tutto
	def effect(self):
		

		current_file = self.args[-1]
		bg_color = self.options.bg_color
		
		
		##Implementare check_dir
		
		if (os.path.isdir(self.options.directory)) == True:					
			
			##CODICE SE ESISTE LA DIRECTORY
			#inkex.errormsg("OK") #DEBUG

			
			#Aggiungo un suffisso al nomefile per non sovrascrivere dei file
			temp_name,fileExtension = os.path.splitext(self.options.filename)	#modified by smat
			if self.options.add_numeric_suffix_to_filename :
				dir_list = os.listdir(self.options.directory) #List di tutti i file nella directory di lavoro
				#temp_name =  self.options.filename
				#modified by gsyan : split filename to root name and extension
				#temp_name,fileExtension = os.path.splitext(self.options.filename) #modified by gsyan
                
				max_n = 0
				for s in dir_list :
					r = re.match(r"^%s_0*(\d+)%s$"%(re.escape(temp_name),'.png' ), s)
					if r :
						max_n = max(max_n,int(r.group(1)))	
				self.options.filename = temp_name + "_" + ( "0"*(4-len(str(max_n+1))) + str(max_n+1) )

                

			#genero i percorsi file da usare
			
			suffix = ""
			if self.options.conversion_type == 1:
				suffix = "_BWfix_"+str(self.options.BW_threshold)+"_"
			elif self.options.conversion_type == 2:
				suffix = "_BWrnd_"
			elif self.options.conversion_type == 3:
				suffix = "_H_"
			elif self.options.conversion_type == 4:
				suffix = "_Hrow_"
			elif self.options.conversion_type == 5:
				suffix = "_Hcol_"
			else:
				if self.options.grayscale_resolution == 1:
					suffix = "_Gray_256_"
				elif self.options.grayscale_resolution == 2:
					suffix = "_Gray_128_"
				elif self.options.grayscale_resolution == 4:
					suffix = "_Gray_64_"
				elif self.options.grayscale_resolution == 8:
					suffix = "_Gray_32_"
				elif self.options.grayscale_resolution == 16:
					suffix = "_Gray_16_"
				elif self.options.grayscale_resolution == 32:
					suffix = "_Gray_8_"
				else:
					suffix = "_Gray_"
				
			
			pos_file_png_exported = os.path.join(self.options.directory,self.options.filename+".png") 
			pos_file_png_BW = os.path.join(self.options.directory,self.options.filename+suffix+"preview.png") 
			#pos_file_gcode = os.path.join(self.options.directory,self.options.filename+suffix+"gcode.txt") 
			#modified by gsyan : split filename then join root name , suffix and extension
			if fileExtension != '' :
				pos_file_gcode = os.path.join(self.options.directory,self.options.filename+suffix[:-1]+fileExtension)
			else:
				pos_file_gcode = os.path.join(self.options.directory,self.options.filename+suffix+"gcode.txt")
			
			

			#Esporto l'immagine in PNG
			self.exportPage(pos_file_png_exported,current_file,bg_color)


			
			#DA FARE
			#Manipolo l'immagine PNG per generare il file Gcode
			self.PNGtoGcode(pos_file_png_exported,pos_file_png_BW,pos_file_gcode)
						
			
		else:
			inkex.errormsg("Directory does not exist! Please specify existing directory!")
            

            
            
########	ESPORTA L IMMAGINE IN PNG		
######## 	Richiamata da effect()
		
	def exportPage(self,pos_file_png_exported,current_file,bg_color):		
		######## CREAZIONE DEL FILE PNG ########
		#Crea l'immagine dentro la cartella indicata  da "pos_file_png_exported"
		# -d 127 = risoluzione 127DPI  =>  5 pixel/mm  1pixel = 0.2mm
		###command="inkscape -C -e \"%s\" -b\"%s\" %s -d 127" % (pos_file_png_exported,bg_color,current_file) 

		if self.options.resolution == 1:
			DPI = 25.4
		elif self.options.resolution == 2:
			DPI = 50.8
		elif self.options.resolution == 5:
			DPI = 127
		elif self.options.resolution == 10:    
			DPI = 254
		else:
			DPI = 25.4*self.options.resolution

		command="inkscape -C -e \"%s\" -b\"%s\" %s -d %s" % (pos_file_png_exported,bg_color,current_file,DPI) #Comando da linea di comando per esportare in PNG
					
		p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		return_code = p.wait()
		f = p.stdout
		err = p.stderr


########	CREA IMMAGINE IN B/N E POI GENERA GCODE
######## 	Richiamata da effect()

	# by gsyan
	def getLaserPowerValue(self,oldValue) :
		#return ( self.options.laser_mini_power + (255 - self.options.laser_mini_power)*oldValue/255 )
		return ( self.options.laser_mini_power + (self.options.laser_max_power - self.options.laser_mini_power)*oldValue/255 ) #fix by smat 20190213


	def PNGtoGcode(self,pos_file_png_exported,pos_file_png_BW,pos_file_gcode):
		
		######## GENERO IMMAGINE IN SCALA DI GRIGI ########
		#Scorro l immagine e la faccio diventare una matrice composta da list


		reader = png.Reader(pos_file_png_exported)#File PNG generato
		
		w, h, pixels, metadata = reader.read_flat()
		
		
		matrice = [[255 for i in range(w)]for j in range(h)]  #List al posto di un array
		

		#Scrivo una nuova immagine in Scala di grigio 8bit
		#copia pixel per pixel 
		
		if self.options.grayscale_type == 1:
			#0.21R + 0.71G + 0.07B
			for y in range(h): # y varia da 0 a h-1
				for x in range(w): # x varia da 0 a w-1
					pixel_position = (x + y * w)*4 if metadata['alpha'] else (x + y * w)*3
					matrice[y][x] = int(pixels[pixel_position]*0.21 + pixels[(pixel_position+1)]*0.71 + pixels[(pixel_position+2)]*0.07)
		
		elif self.options.grayscale_type == 2:
			#(R+G+B)/3
			for y in range(h): # y varia da 0 a h-1
				for x in range(w): # x varia da 0 a w-1
					pixel_position = (x + y * w)*4 if metadata['alpha'] else (x + y * w)*3
					matrice[y][x] = int((pixels[pixel_position] + pixels[(pixel_position+1)]+ pixels[(pixel_position+2)]) / 3 )		

		elif self.options.grayscale_type == 3:
			#R
			for y in range(h): # y varia da 0 a h-1
				for x in range(w): # x varia da 0 a w-1
					pixel_position = (x + y * w)*4 if metadata['alpha'] else (x + y * w)*3
					matrice[y][x] = int(pixels[pixel_position])			

		elif self.options.grayscale_type == 4:
			#G
			for y in range(h): # y varia da 0 a h-1
				for x in range(w): # x varia da 0 a w-1
					pixel_position = (x + y * w)*4 if metadata['alpha'] else (x + y * w)*3
					matrice[y][x] = int(pixels[(pixel_position+1)])	
		
		elif self.options.grayscale_type == 5:
			#B
			for y in range(h): # y varia da 0 a h-1
				for x in range(w): # x varia da 0 a w-1
					pixel_position = (x + y * w)*4 if metadata['alpha'] else (x + y * w)*3
					matrice[y][x] = int(pixels[(pixel_position+2)])				
			
		elif self.options.grayscale_type == 6:
			#Max Color
			for y in range(h): # y varia da 0 a h-1
				for x in range(w): # x varia da 0 a w-1
					pixel_position = (x + y * w)*4 if metadata['alpha'] else (x + y * w)*3
					list_RGB = pixels[pixel_position] , pixels[(pixel_position+1)] , pixels[(pixel_position+2)]
					matrice[y][x] = int(max(list_RGB))				

		else:
			#Min Color
			for y in range(h): # y varia da 0 a h-1
				for x in range(w): # x varia da 0 a w-1
					pixel_position = (x + y * w)*4 if metadata['alpha'] else (x + y * w)*3
					list_RGB = pixels[pixel_position] , pixels[(pixel_position+1)] , pixels[(pixel_position+2)]
					matrice[y][x] = int(min(list_RGB))	
		

		####Ora matrice contiene l'immagine in scala di grigi


		######## GENERO IMMAGINE IN BIANCO E NERO ########
		#Scorro matrice e genero matrice_BN
		B=255
		N=0 
		
		matrice_BN = [[255 for i in range(w)]for j in range(h)]
		
		
		if self.options.conversion_type == 1:
			#B/W fixed threshold
			soglia = self.options.BW_threshold
			for y in range(h): 
				for x in range(w):
					if matrice[y][x] >= soglia :
						matrice_BN[y][x] = B
					else:
						matrice_BN[y][x] = N
	
			
		elif self.options.conversion_type == 2:
			#B/W random threshold
			from random import randint
			for y in range(h): 
				for x in range(w): 
					soglia = randint(20,235)
					if matrice[y][x] >= soglia :
						matrice_BN[y][x] = B
					else:
						matrice_BN[y][x] = N
			
			
		elif self.options.conversion_type == 3:
			#Halftone
			Step1 = [[B,B,B,B,B],[B,B,B,B,B],[B,B,N,B,B],[B,B,B,B,B],[B,B,B,B,B]]
			Step2 = [[B,B,B,B,B],[B,B,N,B,B],[B,N,N,N,B],[B,B,N,B,B],[B,B,B,B,B]]
			Step3 = [[B,B,N,B,B],[B,N,N,N,B],[N,N,N,N,N],[B,N,N,N,B],[B,B,N,B,B]]
			Step4 = [[B,N,N,N,B],[N,N,N,N,N],[N,N,N,N,N],[N,N,N,N,N],[B,N,N,N,B]]
			
			for y in range(h/5): 
				for x in range(w/5): 
					media = 0
					for y2 in range(5):
						for x2 in range(5):
							media +=  matrice[y*5+y2][x*5+x2]
					media = media /25
					for y3 in range(5):
						for x3 in range(5):
							if media >= 250 and media <= 255:
								matrice_BN[y*5+y3][x*5+x3] = 	B	
							if media >= 190 and media < 250:
								matrice_BN[y*5+y3][x*5+x3] =	Step1[y3][x3]
							if media >= 130 and media < 190:
								matrice_BN[y*5+y3][x*5+x3] =	Step2[y3][x3]
							if media >= 70 and media < 130:
								matrice_BN[y*5+y3][x*5+x3] =	Step3[y3][x3]
							if media >= 10 and media < 70:
								matrice_BN[y*5+y3][x*5+x3] =	Step4[y3][x3]		
							if media >= 0 and media < 10:
								matrice_BN[y*5+y3][x*5+x3] = N


		elif self.options.conversion_type == 4:
			#Halftone row
			Step1r = [B,B,N,B,B]
			Step2r = [B,N,N,B,B]
			Step3r = [B,N,N,N,B]
			Step4r = [N,N,N,N,B]

			for y in range(h): 
				for x in range(w/5): 
					media = 0
					for x2 in range(5):
						media +=  matrice[y][x*5+x2]
					media = media /5
					for x3 in range(5):
						if media >= 250 and media <= 255:
							matrice_BN[y][x*5+x3] = 	B
						if media >= 190 and media < 250:
							matrice_BN[y][x*5+x3] =	Step1r[x3]
						if media >= 130 and media < 190:
							matrice_BN[y][x*5+x3] =	Step2r[x3]
						if media >= 70 and media < 130:
							matrice_BN[y][x*5+x3] =	Step3r[x3]
						if media >= 10 and media < 70:
							matrice_BN[y][x*5+x3] =	Step4r[x3]		
						if media >= 0 and media < 10:
							matrice_BN[y][x*5+x3] = N			


		elif self.options.conversion_type == 5:
			#Halftone column
			Step1c = [B,B,N,B,B]
			Step2c = [B,N,N,B,B]
			Step3c = [B,N,N,N,B]
			Step4c = [N,N,N,N,B]

			for y in range(h/5):
				for x in range(w):
					media = 0
					for y2 in range(5):
						media +=  matrice[y*5+y2][x]
					media = media /5
					for y3 in range(5):
						if media >= 250 and media <= 255:
							matrice_BN[y*5+y3][x] = 	B
						if media >= 190 and media < 250:
							matrice_BN[y*5+y3][x] =	Step1c[y3]
						if media >= 130 and media < 190:
							matrice_BN[y*5+y3][x] =	Step2c[y3]
						if media >= 70 and media < 130:
							matrice_BN[y*5+y3][x] =	Step3c[y3]
						if media >= 10 and media < 70:
							matrice_BN[y*5+y3][x] =	Step4c[y3]		
						if media >= 0 and media < 10:
							matrice_BN[y*5+y3][x] = N			
			
		else:
			#Grayscale
			if self.options.grayscale_resolution == 1:
				matrice_BN = matrice
			else:
				for y in range(h): 
					for x in range(w): 
						if matrice[y][x] <= 1:
							matrice_BN[y][x] = 0 ;#Fixed by smat
							
						if matrice[y][x] >= 254:
							matrice_BN[y][x] = 255 # Fixed by smat
						
						if matrice[y][x] > 1 and matrice[y][x] <254:
							matrice_BN[y][x] = ( matrice[y][x] // self.options.grayscale_resolution ) * self.options.grayscale_resolution
						
			
			
		####Ora matrice_BN contiene l'immagine in Bianco (255) e Nero (0)


		#### SALVO IMMAGINE IN BIANCO E NERO ####
		file_img_BN = open(pos_file_png_BW, 'wb') #Creo il file
		Costruttore_img = png.Writer(w, h, greyscale=True, bitdepth=8) #Impostazione del file immagine
		Costruttore_img.write(file_img_BN, matrice_BN) #Costruttore del file immagine
		file_img_BN.close()	#Chiudo il file


		#### GENERO IL FILE GCODE ####
		if self.options.preview_only == False: #Genero Gcode solo se devo
		
			if self.options.flip_y == False: #Inverto asse Y solo se flip_y = False     
				#-> coordinate Cartesiane (False) Coordinate "informatiche" (True)
				matrice_BN.reverse()				

			### Replace \n to line feed of laseron & laseroff options . add by gsyan ###
			self.options.laseron = re.sub(r"\\n", '\n', self.options.laseron)
			self.options.laseroff = re.sub(r"\\n", '\n', self.options.laseroff)
			### by gsyan End ###
			
			Laser_ON = False
			F_G00 = self.options.speed_OFF  #add by gsyan
			F_G01 = self.options.speed_ON
			Scala = self.options.resolution

			file_gcode = open(pos_file_gcode, 'w')  #Creo il file
			
			#Configurazioni iniziali standard Gcode
			file_gcode.write('; Generated with:\n; "Raster 2 Laser Gcode generator for cr3dp"\n; by 305 Engineering\n; Ver:20190929\n;\n')
			file_gcode.write('; Resolution: ' + str(self.options.resolution) + 'pixel/mm\n' )
			if self.options.grayscale_type == 1:
				file_gcode.write('; Color to Grayscale conversion: 0.21R + 0.71G + 0.07B\n')
			elif self.options.grayscale_type == 2:
				file_gcode.write('; Color to Grayscale conversion: (R+G+B)/3\n')
			elif self.options.grayscale_type == 3:
				file_gcode.write('; Color to Grayscale conversion: R\n')
			elif self.options.grayscale_type == 4:
				file_gcode.write('; Color to Grayscale conversion: G\n')
			elif self.options.grayscale_type == 5:
				file_gcode.write('; Color to Grayscale conversion: B\n')
			elif self.options.grayscale_type == 6:
				file_gcode.write('; Color to Grayscale conversion: Max Color\n')
			else:
				file_gcode.write('; Color to Grayscale conversion: Min Color\n')

			if self.options.conversion_type == 1:
				file_gcode.write('; B/W conversion algorithm:  B/W fixed threshold\n')
			elif self.options.conversion_type == 2:
				file_gcode.write('; B/W conversion algorithm: B/W random threshold\n')
			elif self.options.conversion_type == 3:
				file_gcode.write('; B/W conversion algorithm: Halftone\n')
			elif self.options.conversion_type == 4:
				file_gcode.write('; B/W conversion algorithm: Halftone row\n')
			elif self.options.conversion_type == 5:
				file_gcode.write('; B/W conversion algorithm: Halftone column\n')
			else:
				file_gcode.write('; B/W conversion algorithm: Gray scale\n')

			#file_gcode.write('; Grayscale_resolution: ' + str(self.options.grayscale_resolution) + '\n' )
			if self.options.grayscale_resolution == 1:
				file_gcode.write('; Grayscale_resolution: Gray_256\n')
			elif self.options.grayscale_resolution == 2:
				file_gcode.write('; Grayscale_resolution: Gray_128\n')
			elif self.options.grayscale_resolution == 4:
				file_gcode.write('; Grayscale_resolution: Gray_64\n')
			elif self.options.grayscale_resolution == 8:
				file_gcode.write('; Grayscale_resolution: Gray_32\n')
			elif self.options.grayscale_resolution == 16:
				file_gcode.write('; Grayscale_resolution: Gray_16\n')
			elif self.options.grayscale_resolution == 32:
				file_gcode.write('; Grayscale_resolution: Gray_8\n')
			else:
				file_gcode.write('; Grayscale_resolution: Gray\n')
			file_gcode.write(';\n;\n')
			file_gcode.write(self.options.laseroff + '\n') # add by smat
			file_gcode.write('M107 ;Laser Off at the start\n') # add by smat 20190624
			
			
			file_gcode.write('G00 F' + str(F_G00) + '   ; Default Laser Off Speed\n')  # add by gsyan
			file_gcode.write('G01 F' + str(F_G01) + '   ; Default Laser On Speed\n')  # add by gsyan
			#HOMING
			if self.options.homing == 1:
				file_gcode.write('G28; home all axes\n')
				file_gcode.write('G00 Z' + self.options.z_focus + ' F' + str(F_G00) + '; Move Z to focus\n')
				file_gcode.write('G00 X' + self.options.x_adjust + ' F' + str(F_G00) + '; Adjust X Axis\n')
				file_gcode.write('G00 Y' + self.options.y_adjust + ' F' + str(F_G00) + '; Adjust Y Axis\n')
				file_gcode.write('G92 X0 Y0 Z0 ; Zero the X Y Z\n')
			elif self.options.homing == 2:
				file_gcode.write('G28; home all axes\n')
			elif self.options.homing == 3:
				file_gcode.write('G28 X; home X\n')
				file_gcode.write('G28 Y; home Y\n')
				file_gcode.write('G00 X' + self.options.x_adjust + ' F' + str(F_G00) + '; Adjust X Axis\n')
				file_gcode.write('G00 Y' + self.options.y_adjust + ' F' + str(F_G00) + '; Adjust Y Axis\n')
				file_gcode.write('G92 X0 Y0 Z0 ; Zero the X Y Z\n')				
			elif self.options.homing == 4: # add by smat
				file_gcode.write('G0 X0 Y0; Adjust X Axis and Y Axis \n')
				#file_gcode.write('M106 S4\nG4 S10; Pause\n') # add by smat
			else:
				pass
				
			file_gcode.write('G21; Set units to millimeters\n')			
			file_gcode.write('G90; Use absolute coordinates\n')				
			#file_gcode.write('G00 F' + str(F_G00) + '   ; Default Laser Off Speed\n')  # add by gsyan
			#file_gcode.write('G01 F' + str(F_G01) + '   ; Default Laser On Speed\n')  # add by gsyan

			#add by smat original position
			#if self.options.low_laser_dot == True:
				#file_gcode.write(';Low_laser_dot=True\n')
				#file_gcode.write('M106 S4\nG4 S10; Pause\n')
			#else:
				#file_gcode.write(';Low_laser_dot=False\n')
				
			if self.options.low_laser_square > 0:
				#file_gcode.write('\nM106 S4\nG4 S10; Pause\n')
				file_gcode.write('\nM106 S' + str(self.options.low_laser_power) + '\nG4 S10; Pause at anchor point\n') # add by smat 20190727
				
			#if self.options.low_laser_square == True:
				#file_gcode.write(';Low_laser_square=True\n')
				
			#squares = self.options.low_laser_square
			while self.options.low_laser_square > 1:
				file_gcode.write('\n;Low_laser_square='+ str(self.options.low_laser_square - 1) + '\n')
				file_gcode.write('; Max X=' + str(w/self.options.resolution) + ' Max Y=' + str(h/self.options.resolution) + '\n')
				file_gcode.write('G01 X' + str(w/self.options.resolution)+' Y0 F1000\n')
				file_gcode.write('G01 X' + str(w/self.options.resolution)+' Y'+str(h/self.options.resolution)+' F1000\n')
				file_gcode.write('G01 X0 Y'+str(h/self.options.resolution)+' F1000\n')
				file_gcode.write('G01 X0 Y0 F1000\n')
				file_gcode.write('G4 S3; Pause\n')
				self.options.low_laser_square -= 1
			#else:
				#file_gcode.write(';Low_laser_square=False\n')
			file_gcode.write(';\n')


			#Creazione del Gcode
			
			#allargo la matrice per lavorare su tutta l'immagine
			for y in range(h):
				matrice_BN[y].append(B)
			w = w+1
			
			if self.options.conversion_type != 6:
				for y in range(h):
					if y % 2 == 0 :
						for x in range(w):
							if matrice_BN[y][x] == N :
								if Laser_ON == False :
									file_gcode.write('G00 X' + str(float(x)/Scala) + ' Y' + str(float(y)/Scala) + ' F' + str(F_G00) + '\n')
									#file_gcode.write('G00 X' + str(float(x)/Scala) + ' Y' + str(float(y)/Scala) + '\n') #tolto il Feed sul G00
									if self.options.laseron_delay > 0:
										file_gcode.write('G04 P0\n')
									file_gcode.write(self.options.laseron + '\n')			
									if self.options.laseron_delay > 0:
										file_gcode.write('G04 P' + str(self.options.laseron_delay) + '\n')
									Laser_ON = True
								if  Laser_ON == True :   #DEVO evitare di uscire dalla matrice
									if x == w-1 :
										file_gcode.write('G01 X' + str(float(x)/Scala) + ' Y' + str(float(y)/Scala) +' F' + str(F_G01) + '\n')
										if self.options.laseron_delay > 0:
											file_gcode.write('G04 P0\n')
										file_gcode.write(self.options.laseroff + '\n')
										if self.options.laseron_delay > 0:	#add by smat 20190928
											file_gcode.write('G04 P' + str(self.options.laseron_delay) + '\n')	#add by smat 20190928
										Laser_ON = False
									else: 
										if matrice_BN[y][x+1] != N :
											file_gcode.write('G01 X' + str(float(x)/Scala) + ' Y' + str(float(y)/Scala) + ' F' + str(F_G01) +'\n')
											if self.options.laseron_delay > 0:
												file_gcode.write('G04 P0\n')
											file_gcode.write(self.options.laseroff + '\n')
											if self.options.laseron_delay > 0:	#add by smat 20190928
												file_gcode.write('G04 P' + str(self.options.laseron_delay) + '\n')	#add by smat 20190928
											Laser_ON = False
					else:
						for x in reversed(range(w)):
							if matrice_BN[y][x] == N :
								if Laser_ON == False :
									file_gcode.write('G00 X' + str(float(x)/Scala) + ' Y' + str(float(y)/Scala) + ' F' + str(F_G00) + '\n')
									#file_gcode.write('G00 X' + str(float(x)/Scala) + ' Y' + str(float(y)/Scala) + '\n') #tolto il Feed sul G00
									if self.options.laseron_delay > 0:
										file_gcode.write('G04 P0\n')
									file_gcode.write(self.options.laseron + '\n')			
									if self.options.laseron_delay > 0:
										file_gcode.write('G04 P' + str(self.options.laseron_delay) + '\n')
									Laser_ON = True
								if  Laser_ON == True :   #DEVO evitare di uscire dalla matrice
									if x == 0 :
										file_gcode.write('G01 X' + str(float(x)/Scala) + ' Y' + str(float(y)/Scala) +' F' + str(F_G01) + '\n')
										if self.options.laseron_delay > 0:
											file_gcode.write('G04 P0\n')
										file_gcode.write(self.options.laseroff + '\n')
										if self.options.laseron_delay > 0:	#add by smat 20190928
											file_gcode.write('G04 P' + str(self.options.laseron_delay) + '\n')	#add by smat 20190928
										Laser_ON = False
									else: 
										if matrice_BN[y][x-1] != N :
											file_gcode.write('G01 X' + str(float(x)/Scala) + ' Y' + str(float(y)/Scala) + ' F' + str(F_G01) +'\n')
											if self.options.laseron_delay > 0:
												file_gcode.write('G04 P0\n')
											file_gcode.write(self.options.laseroff + '\n')
											if self.options.laseron_delay > 0:	#add by smat 20190928
												file_gcode.write('G04 P' + str(self.options.laseron_delay) + '\n')	#add by smat 20190928
											Laser_ON = False				

			else: ##SCALA DI GRIGI GrayScale
				for y in range(h):
					if y % 2 == 0 :
						for x in range(w):
							if matrice_BN[y][x] != B :
								if Laser_ON == False :
									#file_gcode.write('G00 X' + str(float(x)/Scala) + ' Y' + str(float(y)/Scala) +'\n')
									file_gcode.write('G00 X' + str(float(x)/Scala) + ' Y' + str(float(y)/Scala) +' F' + str(F_G00) +'\n')	#add by smat for gray
									if self.options.laseron_delay > 0: # Add by smat to disable laseron_delay in crayscale mode. 2017.02.17 20190608
										file_gcode.write('G04 P0\n') # Add by smat to disable laseron_delay in crayscale mode. 2017.02.17 20190608
									#file_gcode.write(self.options.laseron + ' '+ ' S' + str(255 - matrice_BN[y][x]) +'\n')
									file_gcode.write(self.options.laseron + ' '+ ' S' + str( self.getLaserPowerValue(255 - matrice_BN[y][x]) ) +'\n')
									if self.options.laseron_delay > 0: # Add by smat to disable laseron_delay in crayscale mode. 2017.02.17 20190608
										file_gcode.write('G04 P' + str(self.options.laseron_delay) + '\n')	# Add by smat to disable laseron_delay in crayscale mode. 2017.02.17 20190608
									Laser_ON = True
									
								if  Laser_ON == True :   #DEVO evitare di uscire dalla matrice
									if x == w-1 : #controllo fine riga
										#if matrice_BN[y][x] < (255-self.options.grayscale_resolution):
										file_gcode.write('G01 X' + str(float(x)/Scala) + ' Y' + str(float(y)/Scala) +' F' + str(F_G01+self.options.laser_contrast*(256-self.getLaserPowerValue(255 - matrice_BN[y][x]))) + ';Break Point A1\n') #test by smat
										#else:
											#file_gcode.write('G01 X' + str(float(x)/Scala) + ' Y' + str(float(y)/Scala) +' F' + str(F_G00) + '\n') 

										if self.options.laseron_delay > 0:	#fixed by smat 20190608
											file_gcode.write('G04 P0; w\n')	#fixed by smat 20190608
										file_gcode.write(self.options.laseroff + '\n')
										if self.options.laseron_delay > 0:	#fixed by smat 20190928
											file_gcode.write('G04 P' + str(self.options.laseron_delay) + '\n')	#add by smat 20190928
										Laser_ON = False
										
									else: 
										if matrice_BN[y][x+1] == B :
											#if matrice_BN[y][x] < (255-self.options.grayscale_resolution):
											file_gcode.write('G01 X' + str(float(x+1)/Scala) + ' Y' + str(float(y)/Scala) + ' F' + str(F_G01+self.options.laser_contrast*(256-self.getLaserPowerValue(255 - matrice_BN[y][x]))) +'\n') #test by smat
											#else:
												#file_gcode.write('G01 X' + str(float(x)/Scala) + ' Y' + str(float(y)/Scala) +' F' + str(F_G00) + '\n') 
											if self.options.laseron_delay > 0:	#fixed by smat 20190608
												file_gcode.write('G04 P0; B1\n')	#fixed by smat 20190608
											file_gcode.write(self.options.laseroff + '\n')
											if self.options.laseron_delay > 0:	#fixed by smat 20190928
												file_gcode.write('G04 P' + str(self.options.laseron_delay) + '\n')	#add by smat 20190928
											Laser_ON = False
											
										elif matrice_BN[y][x] != matrice_BN[y][x+1] :
											#if matrice_BN[y][x] < (255-self.options.grayscale_resolution):
											file_gcode.write('G01 X' + str(float(x+1)/Scala) + ' Y' + str(float(y)/Scala) + ' F' + str(F_G01+self.options.laser_contrast*(256-self.getLaserPowerValue(255 - matrice_BN[y][x]))) +'\n') #test by smat
											#else:
												#file_gcode.write('G01 X' + str(float(x)/Scala) + ' Y' + str(float(y)/Scala) +' F' + str(F_G00) + '\n') 
											#if self.options.laseron_delay > 0:	#fixed by smat 20190608
												#file_gcode.write('G04 P0\n')	#fixed by smat 20190608
											# file_gcode.write(self.options.laseron + ' '+ ' S' + str(255 - matrice_BN[y][x+1]) +'\n')												
											file_gcode.write(self.options.laseron + ' '+ ' S' + str( self.getLaserPowerValue( 255 - matrice_BN[y][x+1]) ) +'\n')												
											#if self.options.laseron_delay > 0:	#fixed by smat 20190608
												#file_gcode.write('G04 P' + str(self.options.laseron_delay) + '\n')	#fixed by smat 20190608
                                            

					
					else:
						for x in reversed(range(w)):
							if matrice_BN[y][x] != B :
								if Laser_ON == False :
									#file_gcode.write('G00 X' + str(float(x+1)/Scala) + ' Y' + str(float(y)/Scala) +'\n')
									file_gcode.write('G00 X' + str(float(x+1)/Scala) + ' Y' + str(float(y)/Scala) +' F' + str(F_G00) +'\n') #add by smat for gray
									if self.options.laseron_delay > 0:	#fixed by smat 20190608
										file_gcode.write('G04 P0\n')	#fixed by smat 20190608
									#file_gcode.write(self.options.laseron + ' '+ ' S' + str(255 - matrice_BN[y][x]) +'\n') #fixed by smat 20170226
									file_gcode.write(self.options.laseron + ' '+ ' S' + str( self.getLaserPowerValue( 255 - matrice_BN[y][x] ) ) +'\n')
									if self.options.laseron_delay > 0:	#fixed by smat 20190608
										file_gcode.write('G04 P' + str(self.options.laseron_delay) + '\n')	#fixed by smat 20190608
									Laser_ON = True
									
								if  Laser_ON == True :   #DEVO evitare di uscire dalla matrice
									if x == 0 : #controllo fine riga ritorno
										#if matrice_BN[y][x] < (255-self.options.grayscale_resolution):
										file_gcode.write('G01 X' + str(float(x)/Scala) + ' Y' + str(float(y)/Scala) +' F' + str(F_G01+self.options.laser_contrast*(256-self.getLaserPowerValue(255 - matrice_BN[y][x]))) + '\n') #test by smat
										#else:
											#file_gcode.write('G01 X' + str(float(x)/Scala) + ' Y' + str(float(y)/Scala) +' F' + str(F_G00) + '\n') 
										if self.options.laseron_delay > 0:	#fixed by smat 20190608
											file_gcode.write('G04 P0; x==0\n')	#fixed by smat 20190608
										file_gcode.write(self.options.laseroff + '\n')
										if self.options.laseron_delay > 0:	#fixed by smat 20190928
											file_gcode.write('G04 P' + str(self.options.laseron_delay) + '\n')	#add by smat 20190928
										Laser_ON = False
										
									else: 
										if matrice_BN[y][x-1] == B :
											#if matrice_BN[y][x] < (255-self.options.grayscale_resolution):
											file_gcode.write('G01 X' + str(float(x)/Scala) + ' Y' + str(float(y)/Scala) + ' F' + str(F_G01+self.options.laser_contrast*(256-self.getLaserPowerValue(255 - matrice_BN[y][x]))) + '\n') #test by smat
											#else:
												#file_gcode.write('G01 X' + str(float(x)/Scala) + ' Y' + str(float(y)/Scala) +' F' + str(F_G00) + '\n') 
											if self.options.laseron_delay > 0:	#fixed by smat 20190608
												file_gcode.write('G04 P0; B2\n')	#fixed by smat 20190608
											file_gcode.write(self.options.laseroff + '\n')
											if self.options.laseron_delay > 0:	#fixed by smat 20190928
												file_gcode.write('G04 P' + str(self.options.laseron_delay) + '\n')	#add by smat 20190928
											Laser_ON = False
											
										elif  matrice_BN[y][x] != matrice_BN[y][x-1] :
											#if matrice_BN[y][x] < (255-self.options.grayscale_resolution):
											file_gcode.write('G01 X' + str(float(x)/Scala) + ' Y' + str(float(y)/Scala) + ' F' + str(F_G01+self.options.laser_contrast*(256-self.getLaserPowerValue(255 - matrice_BN[y][x]))) +'\n') #test by smat
											#else:
												#file_gcode.write('G01 X' + str(float(x)/Scala) + ' Y' + str(float(y)/Scala) +' F' + str(F_G00) + '\n') 
											#if self.options.laseron_delay > 0:	#fixed by smat 20190608
												#file_gcode.write('G04 P0\n')	#fixed by smat 20190608
											# file_gcode.write(self.options.laseron + ' '+ ' S' + str(255 - matrice_BN[y][x-1]) +'\n')
											file_gcode.write(self.options.laseron + ' '+ ' S' + str( self.getLaserPowerValue( 255 - matrice_BN[y][x-1]) ) +'\n')
											#if self.options.laseron_delay > 0:	#fixed by smat 20190608
												#file_gcode.write('G04 P' + str(self.options.laseron_delay) + '\n')	#fixed by smat 20190608

			
			
			#Configurazioni finali standard Gcode
			file_gcode.write('M107;Laser Off at the end\n')	#add by smat 20190624
			file_gcode.write('G00 X0 Y0; home\n')
			#HOMING
			if self.options.homing == 2:
				file_gcode.write('G28; home all axes\n')
			elif self.options.homing == 3:
				file_gcode.write(';G28 X; home x axes\n')
				file_gcode.write(';G28 Y; home y axes\n')
			else:
				pass
			
			file_gcode.close() #Chiudo il file




######## 	######## 	######## 	######## 	######## 	######## 	######## 	######## 	######## 	


def _main():
	e=GcodeExport()
	e.affect()
	
	exit()

if __name__=="__main__":
	_main()




