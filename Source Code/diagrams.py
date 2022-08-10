from graphviz import Digraph
class Diagrams:
    def __init__(self,inp_size,out_size,inp_width,out_width,r,w):
        self.inp_size=inp_size
        self.out_size=out_size
        self.inp_width=inp_width
        self.out_width=out_width
        self.r=r
        self.w=w
        self.s=int(self.out_size//self.inp_size)
        self.width=int(self.out_width//self.inp_width)
    def __mid(self,M):
        if M<2:
            m=1
        elif M%2==1:
            m=(M+1)/2
        else:
            m=M/2
        return m
    def OLDrw(self):
        s=self.s
        m=self.__mid(self.s)
        rw='1RW'
        bname='SRAM'
        g=Digraph('G',format='png')
        g.attr(rankdir='LR',compound='true',)
        g.attr('node',shape='box')
        g.node('ACG','',shape='none',width='0',height='0')
        g.node('A2','',shape='none',width='0',height='0')
        g.node('A3','',shape='none',width='0',height='0')

        with g.subgraph(name='cluster0') as c:
            c.attr(label=f"{rw} {str(self.out_size)}Kb",style='filled',fillcolor='#4daff0')
            for i in range(1,s+1):
                c.node('B'+str(i),label=f'{bname}\n{rw} {str(self.inp_size)}Kb',style='filled',fillcolor='#FFFFFF')
                if i == m:
                    c.node('mid','',shape='none',width='0',height='0')
        g.edge('ACG',('B'+str(int(m))),lhead='cluster0',label='Write')
        g.edge('A2',('B'+str(int(m+1))),lhead='cluster0',label='Addr')
        g.edge('mid','A3',ltail='cluster0',label='Read')
        g.view()
        #g.render(filename=f'{self.out_size}Kb1RW')
    def __rw(self):
        s=self.s
        m=self.__mid(self.s)
        rw='1RW'
        bname='Block Ram'
        g=Digraph('G',format='png')
        g.attr(rankdir='LR',compound='true',)
        g.attr('node',shape='box')
        g.node('ACG','',shape='none',width='0',height='0')
        g.node('A2','',shape='none',width='0',height='0')
        g.node('A3','',shape='none',width='0',height='0')

        with g.subgraph(name='cluster0') as c:
            c.attr(label=f"{rw} {str(self.out_size)}Kb",style='filled',fillcolor='#4daff0')
            c.node('B',label=f'{bname}\n{s}x{self.width}',style='filled',fillcolor='#FFFFFF')
            c.node('mid','',shape='none',width='0',height='0')
        g.edge('ACG','B',lhead='cluster0',label='Write')
        g.edge('A2',"mid",lhead='cluster0',label='Addr')
        g.edge('B','A3',ltail='cluster0',label='Read')
        g.view()
        #g.render(filename=f'{self.out_size}Kb1RW')
    def __nr1w(self):
        s=self.s
        m=self.__mid(self.s)
        r=self.r
        g=Digraph("G",format='png')
        g.attr(rankdir='LR',compound='true')
        g.node('ACG','',shape='none',width='0',height='0')
        with g.subgraph(name='cluster0') as c: 
            c.attr('node',shape='rect')
            c.node('m',f"{self.out_size}Kb {r}r1W",height=str(r+1),shape='box',style='filled',fillcolor=' #D8D8D8',textcolor='#FFFFFF')
            for i in range(0,r):
                b='b'+str(i)
                c.node(b,'Generic\n1RW',height='1',style='filled',fillcolor=' #D8D8D8')
                c.edge('m',b)
                with c.subgraph(name='cluster'+str(i+1)) as c1: 
                    c1.attr(style='filled',fillcolor='#A6D7F7')
                    c1.node('b1'+str(i),f'Base Block {s}x{self.width}',style='filled',fillcolor='#FFFFFF')
                c.edge(b,'b1'+str(i),lhead='cluster'+str(i+1))
            for i in range(0,r+1):
                c.node('in'+str(i),'',shape='none',width='0',height='0.8')
                c.edge('in'+str(i),'m',style='invis')
                
        g.edge('ACG','in0',lhead='cluster0',label='Write')
        for z in range(1,r+1):
            b='in'+str(z)
            g.node('ACG'+str(z),'',shape='none',width='0',height='0')
            g.edge('ACG'+str(z),b,label='Addr',lhead='cluster0')
        for i in range(0,r):
            b='b1'+str(i)
            a="A"+str(i)
            g.node(a,'',shape='none',width='0',height='0')
            g.edge(b,a,ltail='cluster0',label='Read')

        g.view()
        #g.render(filename=f'{self.out_size}Kb{r}R1W Temp')
    def OLDnr1w(self):
        s=self.s
        m=self.__mid(self.s)
        r=self.r
        g=Digraph("G",format='png')
        g.attr(rankdir='LR',compound='true')
        g.node('ACG','',shape='none',width='0',height='0')
        with g.subgraph(name='cluster0') as c: 
            c.attr('node',shape='rect')
            c.node('m',f"{self.out_size}Kb {r}r1W",height=str(r+1),shape='box',style='filled',fillcolor=' #D8D8D8',textcolor='#FFFFFF')
            for i in range(0,r):
                b='b'+str(i)
                c.node(b,'Generic\n1RW',height='1',style='filled',fillcolor=' #D8D8D8')
                c.edge('m',b)
                with c.subgraph(name='cluster'+str(i+1)) as c1: 
                    c1.attr(style='filled',fillcolor='#A6D7F7')
                    for j in range(0,s):
                        b1='b1'+str(j)+str(i)
                        c1.node(b1,'Base Block',style='filled',fillcolor='#FFFFFF')
                c.edge(b,'b1'+str(int(m-1))+str(i),lhead='cluster'+str(i+1))
            for i in range(0,r+1):
                c.node('in'+str(i),'',shape='none',width='0',height='0.8')
                c.edge('in'+str(i),'m',style='invis')
                
        g.edge('ACG','in0',lhead='cluster0',label='Write')
        for z in range(1,r+1):
            b='in'+str(z)
            g.node('ACG'+str(z),'',shape='none',width='0',height='0')
            g.edge('ACG'+str(z),b,label='Addr',lhead='cluster0')
        for i in range(0,r):
            b='b1'+'0'+str(i)
            a="A"+str(i)
            g.node(a,'',shape='none',width='0',height='0')
            g.edge(b,a,ltail='cluster0',label='Read')

        g.view()
        #g.render(filename=f'{self.out_size}Kb{r}R1W')
    def OLDnrnw(self):
        #g=Digraph("G")
        g=Digraph("G",format='png')
        g.attr(rankdir='LR',compound='true')
        g.node('ACG','',shape='none',width='0',height='0')
        with g.subgraph(name='cluster0') as c: 
            c.attr('node',shape='rect')
            s=self.s
            r=self.r
            w=self.w
            if r>=w:
                addr=r
            else:
                addr=w
            c.node('m',f"{self.out_size}Kb {r}R{w}W",height=f'{w+1+addr}',style='filled',fillcolor=' #D8D8D8',textcolor='#FFFFFF')
            if w%2==0:
                midE=True
            else:
                midE=False
            for i in range(1,w+1):
                b='b'+str(i)
                
                c.node(b,'Feedback\nBlock',height='1.5',style='filled',fillcolor=' #D8D8D8')
                c.edge('m',b)
                if i == self.__mid(w):
                    c.node('acts','',shape='none',width='0',height='0')
                    c.node('acts1','',shape='none',width='0',height='0')
                    c.node('act','',shape='none',width='0',height='0')
                    c.edge('m','acts1',arrowhead='none')
                    c.edge('acts1','acts',arrowhead='none')
                    c.edge('acts','act',arrowhead='none')
                    for k in range(1,w+1):
                        c.node('act'+str(k),'Actual\nBlock',height='1.5',style='filled',fillcolor=' #D8D8D8')
                        c.edge('act','act'+str(k))
                        if midE == True and k==self.__mid(w):
                            c.node('out','',shape='none',width='0',height='0')
                            c.node('outs','',shape='none',width='0',height='0')
                            c.edge('act','outs',style='invis')
                            c.edge('outs','out',style='invis')
                            for o in range(0,r):
                                c.node('out'+str(o),'',shape='none',width='0',height='0.8')
                                c.edge('out','out'+str(o),style='invis')
                                g.node('read'+str(o),'',shape='none',width='0',height='0')
                                g.edge('out'+str(o),'read'+str(o),ltail='cluster0',label='Read')
                        for l in range(1,r+1):
                            if midE == False and k == self.__mid(w) and  l == self.__mid(r+1) :
                                c.node('out','',shape='none',width='0',height='0')
                                c.edge('act'+str(k),'out',style='invis')
                                for o in range(0,r):
                                    c.node('out'+str(o),'',shape='none',width='0',height='0.8')
                                    c.edge('out','out'+str(o),style='invis')
                                    g.node('read'+str(o),'',shape='none',width='0',height='0')
                                    g.edge('out'+str(o),'read'+str(o),ltail='cluster0',label='Read')
                            with c.subgraph(name='clusterR'+str(i)+str(l)+str(k)) as c1:
                                c1.attr(style='filled',fillcolor='#A6D7F7')
                                c1.attr('node',style='filled',fillcolor='#FFFFFF') 
                                for j in range(1,s+1):
                                    b1='b1'+str(l)+str(j)+str(i)+str(k)
                                    c1.node(b1,'Base Block')
                            c.edge('act'+str(k),'b1'+str(l)+str(int(self.__mid(s)))+str(i)+str(k),lhead='clusterR'+str(i)+str(l)+str(k))  

                
                for j in range(1,w):
                    with c.subgraph(name='clusterR_feedback'+str(j)+str(i)) as c1:
                        c1.attr(style='filled',fillcolor='#A6D7F7')
                        c1.attr('node',style='filled',fillcolor='#FFFFFF') 
                        for k in range(1,s+1):
                            b1='fb1'+str(j)+str(i)+str(k)
                            c1.node(b1,'Base Block')
                    c.edge(b,'fb1'+str(j)+str(i)+str(1),lhead='clusterR_feedback'+str(j)+str(i))
            for i in range(1,w+1+addr):
                c.node('in'+str(i),'',shape='none',width='0',height='0.8')
                c.edge('in'+str(i),'m',style='invis')

        for z in range(1,w+1):
            b='in'+str(z)
            g.node('ACG'+str(z),'',shape='none',width='0',height='0')
            g.edge('ACG'+str(z),b,label='Write',lhead='cluster0')

        for z in range(w+1,w+addr+1):
            b='in'+str(z)
            g.node('ACG'+str(z),'',shape='none',width='0',height='0')
            g.edge('ACG'+str(z),b,label='Addr',lhead='cluster0')

        g.view()
        #g.render(filename=f'{self.out_size}Kb{r}R{w}W')

    def __nrnw(self):
        #g=Digraph("G")
        g=Digraph("G",format='png')
        g.attr(rankdir='LR',compound='true')
        g.node('ACG','',shape='none',width='0',height='0')
        with g.subgraph(name='cluster0') as c: 
            c.attr('node',shape='rect')
            s=self.s
            r=self.r
            w=self.w
            if r>=w:
                addr=r
            else:
                addr=w
            c.node('m',f"{self.out_size}Kb {r}R{w}W",height=f'{w+1+addr}',style='filled',fillcolor=' #D8D8D8',textcolor='#FFFFFF')
            if w%2==0:
                midE=True
            else:
                midE=False
            for i in range(1,w+1):
                b='b'+str(i)
                
                c.node(b,'Feedback\nBlock',height='1.5',style='filled',fillcolor=' #D8D8D8')
                c.edge('m',b)
                if i == self.__mid(w):
                    c.node('acts','',shape='none',width='0',height='0')
                    c.node('acts1','',shape='none',width='0',height='0')
                    c.node('act','',shape='none',width='0',height='0')
                    c.edge('m','acts1',arrowhead='none')
                    c.edge('acts1','acts',arrowhead='none')
                    c.edge('acts','act',arrowhead='none')
                    for k in range(1,w+1):
                        c.node('act'+str(k),'Actual\nBlock',height='1.5',style='filled',fillcolor=' #D8D8D8')
                        c.edge('act','act'+str(k))
                        if midE == True and k==self.__mid(w):
                            c.node('out','',shape='none',width='0',height='0')
                            c.node('outs','',shape='none',width='0',height='0')
                            c.edge('act','outs',style='invis')
                            c.edge('outs','out',style='invis')
                            for o in range(0,r):
                                c.node('out'+str(o),'',shape='none',width='0',height='0.8')
                                c.edge('out','out'+str(o),style='invis')
                                g.node('read'+str(o),'',shape='none',width='0',height='0')
                                g.edge('out'+str(o),'read'+str(o),ltail='cluster0',label='Read')
                        for l in range(1,r+1):
                            if midE == False and k == self.__mid(w) and  l == self.__mid(r+1) :
                                c.node('out','',shape='none',width='0',height='0')
                                c.edge('act'+str(k),'out',style='invis')
                                for o in range(0,r):
                                    c.node('out'+str(o),'',shape='none',width='0',height='0.8')
                                    c.edge('out','out'+str(o),style='invis')
                                    g.node('read'+str(o),'',shape='none',width='0',height='0')
                                    g.edge('out'+str(o),'read'+str(o),ltail='cluster0',label='Read')
                        with c.subgraph(name='clusterR'+str(i)+str(k)) as c1:
                            c1.attr(style='filled',fillcolor='#A6D7F7')
                            c1.attr('node',style='filled',fillcolor='#FFFFFF') 
                            b1='b1'+str(i)+str(k)
                            c1.node(b1,f'{r}x Base Block {s}x{self.width}')
                        c.edge('act'+str(k),'b1'+str(i)+str(k),lhead='clusterR'+str(i)+str(k))  

                
                with c.subgraph(name='clusterR_feedback'+str(i)) as c1:
                    c1.attr(style='filled',fillcolor='#A6D7F7')
                    c1.attr('node',style='filled',fillcolor='#FFFFFF') 
                    b1='fb1'+str(i)
                    c1.node(b1,f'{w-1}x Base Block {s}x{self.width}')
                c.edge(b,'fb1'+str(i),lhead='clusterR_feedback'+str(i))
            for i in range(1,w+1+addr):
                c.node('in'+str(i),'',shape='none',width='0',height='0.8')
                c.edge('in'+str(i),'m',style='invis')

        for z in range(1,w+1):
            b='in'+str(z)
            g.node('ACG'+str(z),'',shape='none',width='0',height='0')
            g.edge('ACG'+str(z),b,label='Write',lhead='cluster0')

        for z in range(w+1,w+addr+1):
            b='in'+str(z)
            g.node('ACG'+str(z),'',shape='none',width='0',height='0')
            g.edge('ACG'+str(z),b,label='Addr',lhead='cluster0')

        g.view()
        #g.render(filename=f'{self.out_size}Kb{r}R{w}W')

    def showDiag(self):
        if self.r == 1 and self.w == 1:
            self.__rw()
        elif self.r>1 and self.w == 1:
            self.__nr1w()
        elif self.r>=1 and self.w > 1:
            self.__nrnw()
        
#diag1=Diagrams(2,12,2,8,1,1)
#diag1.showDiag()
#diag1.Tempnrnw()
