import random
class Env:
    def __init__(self, d, n):
        self.d = d
        self.n = n
        data = [0]*(d*d-n)+[1]*(n)
        random.shuffle(data)
        self.board = [ [data.pop() for j in range(d)] for i in range(d)] # 0 is clear
        #TODO: randomly fill n 1s in board
    def query(self,r,c):
        """ returns -1 if MINE, else num of mined neighbors"""
        if self.board[r][c]:
            return -1
        else:
            counter = 0
            for dx in [-1,0,1]:
                for dy in [-1,0,1]:
                    if dx or dy:
                        x,y=r+dx,c+dy
                        if x>=0 and x<self.d and y>=0 and y<self.d:
                            counter += self.board[x][y]
            return counter
    def __repr__(s):
        res=''
        for i in range(s.d):
            for j in range(s.d):
                res+='{:<3}'.format(s.board[i][j])
            res+='\n'
        return res

class Agent:
    def __init__(self, d, n):
        self.d = d
        self.n = n
        self.board = [ [0 for j in range(d)] for i in range(d)]
        # -1 is MINE
        # 0 is UNKNOWN
        # 1 is CLEAR
        self.qh = []
        self.score = 0
        self.hits = 0
        self.prob= [ [0 for j in range(d)] for i in range(d)] # probability of seeing a mine here
        self.visited = [ [0 for j in range(d)] for i in range(d)] # 0 is unvisited, 1 is known.
        self.numsides=None
    
    def boxit(self,box,pad=3,fmt=''):
        res=''
        if fmt:
            template='{{: {}{}}}'.format(pad,fmt)
        else:
            template='{{:>{}}}'.format(pad)
        for i in range(len(box)):
            for j in range(len(box[i])):
                res+=template.format(box[i][j])
            res+='\n'
        return res
    def joinboxes(self,boxesstr,pad='\t'):
        return '\n'.join(pad.join(line) for line in zip(*[boxstr.strip('\n').split('\n') for boxstr in boxesstr]))
    def getboard(self):
        board=[ ["?" for j in range(self.d)] for i in range(self.d)]
        for r in range(self.d):
            for c in range(self.d):
                try:
                    o=next(o for x,y,o in self.qh if x==r and y==c)
                    if o==-1:
                        board[r][c]='M' #mine stepped on
                    else:
                        board[r][c]=o
                except StopIteration:
                    if self.board[r][c]==-1:
                        board[r][c]='m' #mine discovered
                    elif self.board[r][c]==1:
                        board[r][c]='c' #clear but unvisited
        return board
        
    def __repr__(s):
        return s.plotprogress()
        head=' BOARD  VISITED\t\tPROBABILITY\n'
        return head+s.joinboxes([s.boxit(s.getboard(),2),s.boxit(s.visited,2),s.boxit(s.prob,9,'.2f')])
    def getnumsides(self,X,Y):
        if self.numsides!=None:
            return self.numsides[X][Y]
        self.numsides = [ [0 for j in range(self.d)] for i in range(self.d)]
        for r in range(self.d):
            for c in range(self.d):
                for dx in [-1,0,1]:
                    for dy in [-1,0,1]:
                        if dx or dy:
                            x,y=r+dx,c+dy
                            if x>=0 and x<self.d and y>=0 and y<self.d:
                                self.numsides[x][y]+=1
        return self.numsides[X][Y]
    
    def any_unknown(self):
        return any(0 in row for row in self.board) and sum(row.count(-1) for row in self.board)<self.n
    
    def getprob(s,x,y):
        # prob=-1 if already cleared
        if s.board[x][y]==1:
            return -1000
        return s.prob[x][y]#*8/s.getnumsides(x,y)
    
    def addprob(self,r,c,v):
        v=v/self.getnumsides(r,c)
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                if dx or dy:
                    x,y=r+dx,c+dy
                    if x>=0 and x<self.d and y>=0 and y<self.d:
                        self.prob[x][y]+= (v/self.getnumsides(x,y)) if v<1 else v
                        # Improvement: Rather than bluntly adding prob. of 1/8 per direction, consider to remove all the neighbors that are already CLEAR.
    
    def my_8_clear(self,r,c):
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                if dx or dy:
                    x,y=r+dx,c+dy
                    if x>=0 and x<self.d and y>=0 and y<self.d:
                        self.board[x][y]=1
                        self.prob[x][y]=-999
    def discovermines(self):
        earned=0
        poses=[]
        for r in range(self.d):
            for c in range(self.d):
                if self.getprob(r,c)>=1:
                    if self.board[r][c]==0:
                        earned+=1
                        self.board[r][c]=-1
                        poses.append([r,c,self.getprob(r,c)])
                        
        # TODO: Re-write below check.
        unknownmines=self.n-sum(row.count(-1) for row in self.board)
        visited=sum(row.count(1) for row in self.visited)
        unvisited=sum(row.count(0) for row in self.visited)
        #if self.d**2==visited+unknownmines:  # all unvisited are mines
        if unvisited<=unknownmines:  # all unvisited are mines
            earned+=unknownmines
            add_poses=[[i,j,999] for i in range(self.d) for j in range(self.d) if self.visited[i][j]==0] # unvisited ones.
            poses+=add_poses
            for ii,jj,_ in add_poses: # declaring them as mines
                self.board[ii][jj]=-1
        
        self.score+=earned
        pos=' '.join('[{},{} = {}]'.format(i,j,k) for i,j,k in poses)
        return 'Discovered {} ({}) new mines without steping on it. Score={}'.format(earned, pos,self.score) if earned else ''

    def move1(self, env, show_logs=True):
        if not show_logs:
            def pass_through(*_,**__):return True
            myprint=pass_through
        else:
            myprint=print
        if not self.any_unknown():  # check if all is done.
            mined=sum([ [ (i,j) for j in range(self.d) if self.board[i][j]==-1] for i in range(self.d)],[])
            myprint("\nAll mines are revealed.",mined,"Score=",self.score,"Hits=",self.hits)
            raise StopIteration
        consider_visiting = []
        
        for i in range(self.d):
            for j in range(self.d):
                # skip if mine
                if self.board[i][j]==-1:
                    continue
                # skip if visited
                elif self.visited[i][j]==1:
                    continue
                # CLEAR/UNKNOWN, UNVISITED:
                consider_visiting.append([i,j,self.getprob(i,j)])
        assert len(consider_visiting), "Nothing to visit :("
        # pick with lowest prob.
        qx,qy,_p=sorted(consider_visiting,key=lambda v:v[-1])[0]
        
        # Agent queries Env.
        myprint("\nWill query: {},{} with prob={:.3f}".format(qx,qy,_p),end='. ')
        ans = env.query(qx,qy)
        self.visited[qx][qy]=1
        self.qh.append([qx,qy,ans])
        
        # agent processes result
        if ans == -1:
            myprint('\n',"--"*15,"\tOops, stepped on a mine!")
            self.board[qx][qy]=-1
            self.hits+=1
        else:
            myprint("Env says", ans)
            self.board[qx][qy]=1
            if ans == 0:
                # set all neighbors as clear
                self.my_8_clear(qx,qy)
            else:
                #add probs of all neighbors:
                self.addprob(qx,qy,ans)
            # check we are determined with a mine position:
            myprint("--"*15,self.discovermines())
        return self


    def colors(self,mode):
        if mode=='board':
            cmap,cdef={"M":"red","m":"tomato","c":"lime",0:"white","?":"silver"},"white"
            return [[cmap.get(c,cdef) for c in row] for row in self.getboard()]
        if mode=='visits':
            cmap,cdef={0:"grey",1:"greenyellow"},"salmon"
            return [[cmap.get(c,cdef) for c in row] for row in self.visited]
        if mode=='prob':
            sprob=[i for i in sorted(set(sum(self.prob,[]))) if i>=0 and i<=100]
            t=len(sprob)
            cmap1=lambda v:(lambda r:(r,1-r,.001))(sprob.index(v)/(t))
            cmap=lambda v:('lime' if v<0 else ('red' if v>100 else cmap1(v)))
            return [[cmap(c) for c in row] for row in self.prob]
    
    def plotprogress(self):
        import matplotlib.pyplot as plt 
        fig=plt.figure(linewidth=0,
                   edgecolor='#96ABA0',
                   facecolor='#FFFFFF',
                   #tight_layout={'pad':1},
                    figsize=(20,1.5)
                  )
        plt1,plt2,plt3=fig.subplots(1,3)
        #ax = plt.gca()
        plt1.set_axis_off() 
        plt2.set_axis_off() 
        plt3.set_axis_off()
        plt1.set_title("Board")
        plt1.table(cellText=self.getboard(),loc='best',cellLoc='center',cellColours=self.colors('board')).scale(0.7,1.5)
        plt2.set_title("Visited")
        plt2.table(cellText=self.visited,loc='best',cellLoc='center',cellColours=self.colors('visits')).scale(.7, 1.5)
        plt3.set_title("PROBABILITY")
        probstr=[[f"{c:.4f}" for c in r]for r in self.prob]
        plt3.table(cellText=probstr,loc='best',cellLoc='center',cellColours=self.colors('prob')).scale(1, 1.7)
        plt.box(on=None)
        plt.show()
        return ''

class DummyAgent(Agent):
    def __init__(self, d, n):
        super().__init__(d,n)
    def move1(self, env, show_logs=True):
        if not show_logs:
            def pass_through(*_,**__):return True
            myprint=pass_through
        else:
            myprint=print
        if not self.any_unknown():  # check if all is done.
            mined=sum([ [ (i,j) for j in range(self.d) if self.board[i][j]==-1] for i in range(self.d)],[])
            myprint("\nAll mines are revealed.",mined,"Score=",self.score,"Hits=",self.hits)
            raise StopIteration
        consider_visiting = []
        
        for i in range(self.d):
            for j in range(self.d):
                # skip if mine
                if self.board[i][j]==-1:
                    continue
                # skip if visited
                elif self.visited[i][j]==1:
                    continue
                # CLEAR/UNKNOWN, UNVISITED:
                consider_visiting.append([i,j,0])
        assert len(consider_visiting), "Nothing to visit :("
        # pick Any
        random.shuffle(consider_visiting)
        qx,qy,_p=consider_visiting[0]
        
        # Agent queries Env.
        myprint("\nWill query: {},{} with prob={:.3f}".format(qx,qy,_p),end='. ')
        ans = env.query(qx,qy)
        self.visited[qx][qy]=1
        self.qh.append([qx,qy,ans])
        
        # agent processes result
        if ans == -1:
            myprint('\n',"--"*15,"\tOops, stepped on a mine!")
            self.board[qx][qy]=-1
            self.hits+=1
        else:
            myprint("Env says", ans)
            self.board[qx][qy]=1
            # check if we are left with only mines:
            #left+discovered=total
            if len(consider_visiting)>1 and len(consider_visiting)-1+self.hits==self.n:
                for i,j,_ in consider_visiting[1:]:self.board[i][j]=-1
        return self

class PartialAgent(Agent):
    def __init__(self, d, n):
        super().__init__(d,n)
    def discovermines(self):
        earned=0
        poses=[]
        for r in range(self.d):
            for c in range(self.d):
                if self.getprob(r,c)>=1:
                    if self.board[r][c]==0:
                        earned+=1
                        self.board[r][c]=-1
                        poses.append([r,c,self.getprob(r,c)])
                        
        """  # Removing ending logic.
        # TODO: Re-write below check.
        unknownmines=self.n-sum(row.count(-1) for row in self.board)
        visited=sum(row.count(1) for row in self.visited)
        unvisited=sum(row.count(0) for row in self.visited)
        #if self.d**2==visited+unknownmines:  # all unvisited are mines
        if unvisited<=unknownmines:  # all unvisited are mines
            earned+=unknownmines
            add_poses=[[i,j,999] for i in range(self.d) for j in range(self.d) if self.visited[i][j]==0] # unvisited ones.
            poses+=add_poses
            for ii,jj,_ in add_poses: # declaring them as mines
                self.board[ii][jj]=-1
        """        
        self.score+=earned
        pos=' '.join('[{},{} = {}]'.format(i,j,k) for i,j,k in poses)
        return 'Discovered {} ({}) new mines without steping on it. Score={}'.format(earned, pos,self.score) if earned else ''

d=3
n=3
env=Env(d,n)
print(env) #1 is mine, 0 is safe IN ENV.

ag=Agent(d,n)
print(ag)
for _ in range(1+d**2):
    try:
        print(ag.move1(env))
    except StopIteration:
        break
# Legend:
# ? - Unknown
# M - Mine we stepped on
# m - mine we discovererd
# c - Clear, not visited
# num - visited, number of mined neighbors


## Measuring:
def generate_1p(dim,dens,exps=None,is_dummy=False):
    #dens=n/d2
    d=dim
    n=dens*d*d
    assert int(n)==n
    n=int(n)
    exps=exps or d*d
    tscore=0
    for ei in range(exps):
        env=Env(d,n)
        try:
            ag=((PartialAgent if is_dummy=='partial' else DummyAgent) if is_dummy else Agent)(d,n)
            while True:
                #print("move")
                ag.move1(env,show_logs=False)
        except StopIteration:
            tscore+=ag.score
            #print("Exp",ei,"Score=",ag.score,"Final",tscore)
    return tscore/(exps*n)

def generate_all(dim,exps="**2"):
    import matplotlib.pyplot as plt 
    space=[round(x * 0.1, 1) for x in range(1, 10)]
    exps=eval("dim"+exps)
    
    #main agent
    data=[(dens,generate_1p(dim,dens,exps=exps)) for dens in space]
    plt.plot(*zip(*data),'--ro',label="Agent")
    #dummy agent
    data=[(dens,generate_1p(dim,dens,exps=exps,is_dummy=True)) for dens in space]
    plt.plot(*zip(*data),'--bo',label="Dummy")
    #PartialAgent agent
    data=[(dens,generate_1p(dim,dens,exps=exps,is_dummy='partial')) for dens in space]
    plt.plot(*zip(*data),'--go',label="Partial")
    
    #plotting
    plt.title(f"Board size={dim}x{dim}")
    plt.xlabel(f"Density (mines/board_size)")
    plt.ylabel(f"Avg. Score (found/total_mines)")
    plt.legend()
    plt.show()

# %%time
# generate_all(10,"**3")

