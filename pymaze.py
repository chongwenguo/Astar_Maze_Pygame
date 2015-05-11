from pygame import*
quit
import random
import Queue

class labyrinthe(list):
	''
	def __init__(self,size):
		self.size = size
		labx,laby = size
		lx,ly = labx+2,laby+2
		ref = [1,lx,-1,-lx]
		l=[[random.randrange(lx+1,lx*(ly-1),lx)+random.randint(0,labx),random.choice(ref)]]
		L = list((0,0,0,0)*lx+((0,0,0,0)+(1,1,1,1)*labx+(0,0,0,0))*laby+(0,0,0,0)*lx)
		L = [L[i:i+4] for i in range(0,lx*ly*4,4)]
		self.extend(L)
		while l:
			for i in l:
				a = sum(i)
				b  = (1 if abs(i[1])==lx else lx)*random.choice((1,-1))
				if all(self[a]):
					c = ref.index(i[1])
					self[i[0]][c] = 0
					i[0] = a
					self[i[0]][c-2] = 0
					if not random.randint(0,1): l.append([i[0],b])
					if not random.randint(0,3): l.append([i[0],-b])
				else :
					if all(self[i[0]+b]): l.append([i[0],b])
					if all(self[i[0]-b]): l.append([i[0],-b])
					l.remove(i)
		del(self[:lx])
		del(self[-lx:])
		del(self[::lx])
		del(self[lx-2::lx-1])

		
	def get_path(self,start,exit):
		dis = {} # h_n(), pair of {pos: distance to exit }
		path = [] 
		# calculate the h_n() values for each position
		eX, eY = exit % 50, exit / 50
		for i in range(0, 2500):
			dis[i] = abs((i%50)-eX) + abs((i/50)-eY) 
			#print i, dis[i], i%50, i/50
		closedSet = [start]
		q = Queue.PriorityQueue() # contains tuple of (g_n() + h_n(), pos)
		came_from = {}
		g_score = {} # cost to go to a pos
		g_score[start] = 0
		current = start
		q.put((dis[start], start)) 
		distance_traveled = 0 # the actual distance
		while not q.empty():
			(a,current) = q.get() # get the first pos in the priority queue
			
			if current == exit: # found the path to exit
				while current in came_from: # construct the path
					distance_traveled += 1 # count the actual distance
					path.append(current)
					current = came_from[current]
				path.append(current)
				distance_traveled += 1
				path.reverse()
				print distance_traveled, dis[start], float(distance_traveled) / float (dis[start])
				return path
			closedSet.append(current)
			tentative_g_score = g_score[current] + 1
			
			openSet = []
			for j in range(q.qsize()): # build the open set from the priority queue
				(a1,b1) = q.queue[j]
				openSet.append(b1)
				
			if self[current][0] == 0 and (current+1) not in closedSet :
				if current + 1 not in openSet or tentative_g_score < g_score[current + 1]: # right
					came_from[current + 1] = current
					g_score[current + 1] = tentative_g_score
					q.put((g_score[current + 1] + dis[current + 1], current + 1))
			if self[current][1] == 0 and (current + 50) not in closedSet:
				 if current + 50 not in openSet or tentative_g_score < g_score[current + 50]: # down
					came_from[current + 50] = current
					g_score[current + 50] = tentative_g_score
					q.put((g_score[current + 50] + dis[current + 50], current + 50))
					
			if self[current][2] == 0 and (current - 1) not in closedSet:
				if current -1 not in openSet or tentative_g_score < g_score[current -1]: # left
					came_from[current -1] = current
					g_score[current -1]  = tentative_g_score
					q.put((g_score[current -1] + dis[current-1], current -1))
					
			if self[current][3] == 0 and (current -50 ) not in closedSet:
				 if current -50 not in openSet or tentative_g_score < g_score[current -50]: #top
					came_from[current -50] = current
					g_score[current -50]  = tentative_g_score
					q.put((g_score[current -50] + dis[current-50],current - 50))
		return None
		# pos = start
	# 	d = 1
	# 	path = [pos]
	# 	ref = [1,self.size[0],-1,-self.size[0]]
	# 	while pos != exit:
	# 		if self[pos][ref.index(d)-1] == 0: d = ref[ref.index(d)-1]
	# 		if self[pos][ref.index(d)] == 0:
	# 			pos = pos+d
	# 			path.append(pos)
	# 			i = path.index(pos)
	# 			if i != len(path)-1:
	# 				del(path[i:-1])
	# 		else: d = ref[ref.index(d)-3]
	# 	return path
	

	def get_image_and_rects(self,cellulesize,wallcolor=(0,0,0),celcolor=(255,255,255)):
		x,y = cellulesize
		image = Surface((x*(self.size[0]),y*self.size[1]))
		image.fill(wallcolor)
		rects = []
		for e,i in enumerate(self):
			rects.append(image.fill(celcolor,(e%(self.size[0])*cellulesize[0]+1-(not i[2]),e/(self.size[0])*cellulesize[1]+1-(not i[3]),cellulesize[0]-2+(not i[2])+(not i[0]),cellulesize[1]-2+(not i[1])+(not i[3]))))
		return image,rects

#****************************************************************************************
#****************************************************************************************
if __name__ == '__main__':
	
	me = Surface((5,5))
	me.fill(0xff0000)
	L = labyrinthe((50,50))
	labx,laby = 50,50
	screen = display.set_mode((L.size[0]*10,L.size[1]*10))
	image,rectslist = L.get_image_and_rects((10,10),wallcolor=0,celcolor=0xffffff)
	screen.blit(image,(0,0))
	start = random.randrange(len(L))
	exit = random.randrange(len(L))
	screen.fill(0x00ff00,rectslist[exit])
	screen.blit(me,rectslist[start])
	display.flip()
	while event.wait().type != QUIT:
		screen.fill(-1,rectslist[start])
		#print start, start %50, start /50
		if key.get_pressed()[K_RIGHT] and not L[start][0]:
			start += 1
		if key.get_pressed()[K_LEFT] and not L[start][2]:
			start += -1
		if key.get_pressed()[K_UP] and not L[start][3]:
			start += -L.size[1]
		if key.get_pressed()[K_DOWN] and not L[start][1]:
			start += L.size[0]
		screen.fill(0xff0000,rectslist[start])
		display.flip()
		if start == exit : print 'YOU WIN'; break
		if key.get_pressed()[K_ESCAPE]:
			for i in L.get_path(start,exit)[1:-1]:
				screen.fill(0x0000ff,rectslist[i])
				display.update(rectslist[i])
				time.wait(20)
