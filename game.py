import cv2
import time
import pickle
import numpy as np
from mss import mss
import pyautogui


pickle_out = open("model/model.pkl","rb")
model = pickle.load(pickle_out)
mon = {'top': 350, 'left': 652, 'width': 600, 'height': 500}
sct = mss()

class board :

	def __init__(self):
		self.players_board = []

	def start_game(self,w,h):
		for i in range(w):
			for j in range(h):
				self.players_board.append(8)
				
	def read_the_board(self):
		image = sct.grab(mon)
		img = np.array(image)
		x = 0
		x1=0
		while(x<mon["height"]):
			y = 0
			y1=0
			while(y<mon["width"]):
				cv2.imwrite('img.png', img[x:x+25,y:y+25])
				feat = cv2.imread("img.png")
				feat = feat.flatten()
				lab = model.predict(feat.reshape(1,-1))[0]
				try:
					self.setlab(x1,y1,lab)
				except:
					pass
				y+=25
				y1+=1
			x+=25
			x1+=1
		cv2.waitKey(1)
		cv2.destroyAllWindows()

	def setlab(self,x,y,label):
		self.players_board[x,y] = label

	def reshape(self):
		self.players_board = np.asarray(self.players_board).reshape(20,24)


	def play(self,w,h):
		self.start_game(w,h)
		self.reshape()
		self.read_the_board()
		x =652+ (0)*25+10
		y =350+ (0)*25+10
		pyautogui.click(x,y)
		while(1):
			time.sleep(2)
			self.read_the_board()
			for i in range(1,23):
				for j in range(1,19):
					center_nbr = self.players_board[j,i]
					if(center_nbr in  [1,2,3,4,5,6,7]):
						conv = (self.players_board[j-1:j+2,i-1:i+2])
						if(np.count_nonzero(conv == 9)+np.count_nonzero(conv == 8) == center_nbr):
							conv  = np.where(conv==8, 9, conv)
							self.players_board[j-1:j+2,i-1:i+2]=conv
							

			for i in range(1,23):
				for j in range(1,19):
					center_nbr = self.players_board[j,i]
					if(center_nbr in  [1,2,3,4,5,6,7]):
						conv = (self.players_board[j-1:j+2,i-1:i+2])
						if(np.count_nonzero(conv == 9) == center_nbr):
							for k in range(j-1,j+2):
								for l in range(i-1,i+2) : 
									if(self.players_board[k,l] == 8):
										x =652+ (l)*25+10
										y =350+ (k)*25+10
										pyautogui.click(x,y)
										
								
if __name__ == "__main__":
	b = board()
	b.play(24,20)