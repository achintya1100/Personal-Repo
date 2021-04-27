import random
#from multiprocessing import Pool
from concurrent.futures import ProcessPoolExecutor as Pool

terrain_types="FL H FR C".split()
terrain_diff=dict(zip(terrain_types,[0.1,0.3,0.7,0.9]))


class Board:
    def __init__(self,dim=50,base=None):
        self.dim=dim
        self.board=base and base.board or tuple(tuple(random.choice(terrain_types) for __ in range(dim)) for _ in range(dim))
        self.__target = (random.randint(0,dim-1),random.randint(0,dim-1))
        self.spawn = (random.randint(0,dim-1),random.randint(0,dim-1))
    def query(self,r,c):
        if self.__target==(r,c) and random.random()>terrain_diff[self.board[r][c]]:
            return True
        return False
    def display(self,highlight=False):
        import matplotlib.pyplot as plt
        fig=plt.figure(linewidth=0,
                   edgecolor='#96ABA0',
                   facecolor='#FFFFFF',
                   #tight_layout={'pad':1},
                    figsize=(20,10)
                  )
        plt2=fig.subplots(1,1)
        plt2.set_title("Board")
        plt2.set_axis_off()
        cmap,cdef={"FL":"white","H":"lightgray","FR":"dimgrey","C":"darkseagreen"},"white"
        colored=[[cmap.get(c,cdef) for c in row] for row in self.board]
        boarded=[[" " for c in row] for row in self.board]
        boarded[self.__target[0]][self.__target[1]]='X'
        table=plt.table(cellText=boarded,loc='best',cellLoc='center',cellColours=colored)#,fontsize=100)
        table._cells[self.__target]._text.set_color("red")
        if highlight:
            table._cells[self.__target]._text.set_color(colored[self.__target[0]][self.__target[1]])
            table._cells[self.__target]._text.set_text(chr(9607))
            #table._cells[self.__target]._text.set_size(50)
            C=list(table._cells[self.__target]._facecolor)
            C=1,0,0,1
            table._cells[self.__target]._facecolor=tuple(C)
        plt.box(on=None)
        plt.show()

class Agent:
    def __init__(self,board,probReset=True,logic="ba1"):
        self.board=board
        self.dim=board.dim
        self.belief=[[self.dim**-2 for __ in range(self.dim)] for _ in range(self.dim)]
        self.moveCount=0
        self.target=None
        self.probReset=probReset
        self.agent_version=logic
        self.current_pos=board.spawn
        self.travelCount=0
    def bestMove(self):
        manha=lambda ir,ic:abs(self.current_pos[0]-ir)+abs(self.current_pos[1]-ic)
        if self.agent_version=="ba1":
            getprob=lambda ir,ic:self.belief[ir][ic]
        elif self.agent_version=="ba2":
            getprob_=lambda ir,ic:self.belief[ir][ic]*(1-terrain_diff[self.board.board[ir][ic]])
            inner=[[getprob_(ir,ic) for ic,v in enumerate(r)] for ir,r in enumerate(self.belief)]
            innertotal=sum(sum(inner,[]))
            inner=[[v/innertotal for v in r] for r in inner]
            getprob=lambda ir,ic:inner[ir][ic]
        elif self.agent_version=="ba2+manha":
            getprob_=lambda ir,ic:self.belief[ir][ic]*(1-terrain_diff[self.board.board[ir][ic]])/(1+manha(ir,ic))
            inner=[[getprob_(ir,ic) for ic,v in enumerate(r)] for ir,r in enumerate(self.belief)]
            innertotal=sum(sum(inner,[]))
            inner=[[v/innertotal for v in r] for r in inner]
            getprob=lambda ir,ic:inner[ir][ic]
        else:
            raise ValueError(f"Invalid agent logic:{self.agent_version}")
        getprobs=lambda ir,ic:[getprob(ir,ic),-manha(ir,ic),random.random()]
        r,c,v=max([(ir,ic,getprobs(ir,ic)) for ir,r in enumerate(self.belief) for ic,v in enumerate(r)],key=lambda rcv:rcv[2])
        return r,c
    def updateBelief(self,r,c):
        tt=self.board.board[r][c]
        self.belief[r][c]*=terrain_diff[tt]
        if self.probReset:  # rescale whole prob. matrix
            total=sum(sum(self.belief,[]))
            self.belief=[[c/total for c in r] for r in self.belief]
    def move1(self):
        # determine best next move
        tr,tc=self.bestMove()
        # update counters
        self.travelCount+=abs(self.current_pos[0]-tr)+abs(self.current_pos[1]-tc)
        self.moveCount+=1
        ans=self.board.query(tr,tc)  # actual query to Board
        # move to new pos
        self.current_pos=(tr,tc)
        # update belief matrix
        if not ans:
            self.updateBelief(tr,tc)
        else:
            self.target=(tr,tc)
        # return if we found the target or not.
        return ans
    
    def main(self,allow_print=True):
        while not self.move1():
            pass
        if allow_print:
            self.board.display()
            print(f"Target found at {self.target} after {self.moveCount} searchs and {self.travelCount} moves.")
        return (self.moveCount+self.travelCount)
        
def driver_helper_inner(mpdata):
    b,ac,allow_print=mpdata  # extract received data
    return Agent(b,**ac).main(allow_print)

def driver_helper(mpdata):
    ac,default_agent,bs,allow_print=mpdata  # extract received data
    ac=dict(default_agent,**ac)
    ac["logic"]=ac.pop("agent_logic")  # argument rename
    result_sum=sum(map(driver_helper_inner,[(X,ac,allow_print) for X in bs]))
    return ac["logic"],result_sum/len(bs)  # result k/v pair

def driver(dim=50,probReset=True,allow_print=True,agent_logic="ba2+manha",exps=1,agents=[{}]):
    baseB=Board(dim=dim)
    bs=[Board(dim=dim,base=baseB) for _ in range(exps)]
    default_agent={"probReset":probReset,"agent_logic":agent_logic}
    return dict(map(driver_helper,[(X,default_agent,bs,allow_print) for X in agents]))

def tester_helper(mpdata):
    agents,defaults=mpdata
    return driver(agents=agents,**defaults)
def tester(dim=50,boards=10,per_board_exps=10):
    exps={"agent_logic": ["ba1","ba2","ba2+manha"]}
    defaults={"allow_print":False,"probReset":True,"dim":dim,"agent_logic":"ba1","exps":per_board_exps}
    
    agents=[{}]
    for k,vs in exps.items():
        agents=[dict({k:v},**a) for a in agents for v in vs]

    avg=lambda G:(lambda L:sum(L)/len(L))(list(G))
    avg_dict=lambda G:(lambda dls:{k:avg(d[k] for d in dls) for k in dls[0]})(list(G))

    return avg_dict(map(tester_helper,[(agents,defaults)]*boards))

def plotter(dims=[5,10,25,50],boards=10,per_board_exps=10):
    import pandas as pd
    from matplotlib import pyplot as plt
    pd.DataFrame([dict(tester(d,boards,per_board_exps),dim=d) for d in dims]).set_index("dim").plot()
    plt.title("Performance of different Agents")
    plt.xlabel("Dimension of Board")
    plt.ylabel("Steps+Searches done by Agent")
    plt.show()
    
if __name__=="__main__":
    driver(50)