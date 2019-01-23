# -*- coding: utf-8 -*-
# 模擬人擺放箱子的習慣,計算後車箱可擺放的箱子
import numpy as np
import copy 
from operator import itemgetter, attrgetter
from itertools import permutations
import random
import MyMath as jm #MyMath.py

class Box:  #箱子
    name='container'
    # r=[0,0,0]
    def __init__(self,name,length,width,height,color):
        self.name=name
        self.l=length
        self.w=width
        self.h=height
        self.b=[length,width,height] #箱子的長寬高
        self.r=[length,width,height] #箱子擺放不同方向所對應的長寬高
        self.pos=[0.0,0.0,0.0] #箱子放置點
        self.color=color
    def set_box_dir(self,i): # 箱子不同擺放方向
        if i==0:
            self.r=[self.l,self.w,self.h]
        if i==1:
            self.r=[self.l,self.h,self.w]
        if i==2:
            self.r=[self.w,self.l,self.h]
        if i==3:
            self.r=[self.w,self.h,self.l]
        if i==4:
            self.r=[self.h,self.l,self.w]
        if i==5:
            self.r=[self.h,self.w,self.l]
        if i==6:
            self.r=[self.l,-self.w,self.h]
        if i==7:
            self.r=[self.l,-self.h,self.w]
        if i==8:
            self.r=[self.w,-self.l,self.h]
        if i==9:
            self.r=[self.w,-self.h,self.l]
        if i==10:
            self.r=[self.h,-self.l,self.w]
        if i==11:
            self.r=[self.h,-self.w,self.l]
        if i==12:
            self.r=[-self.l,self.w,self.h]
        if i==13:
            self.r=[-self.l,self.h,self.w]
        if i==14:
            self.r=[-self.w,self.l,self.h]
        if i==15:
            self.r=[-self.w,self.h,self.l]
        if i==16:
            self.r=[-self.h,self.l,self.w]
        if i==17:
            self.r=[-self.h,self.w,self.l]  
        if i==18:
            self.r=[-self.l,-self.w,self.h]
        if i==19:
            self.r=[-self.l,-self.h,self.w]
        if i==20:
            self.r=[-self.w,-self.l,self.h]
        if i==21:
            self.r=[-self.w,-self.h,self.l]
        if i==22:
            self.r=[-self.h,-self.l,self.w]
        if i==23:
            self.r=[-self.h,-self.w,self.l]                                  
    def set_verts(self): # 箱子目前放置,其八頂點的座標
        self.verts=np.zeros((8,3))
        self.verts[0]=[self.pos[0],self.pos[1],self.pos[2]]
        self.verts[1]=[self.pos[0]+self.r[0],self.pos[1],self.pos[2]]
        self.verts[2]=[self.pos[0]+self.r[0],self.pos[1]+self.r[1],self.pos[2]]
        self.verts[3]=[self.pos[0],self.pos[1]+self.r[1],self.pos[2]]
        self.verts[4]=[self.pos[0],self.pos[1],self.pos[2]+self.r[2]]
        self.verts[5]=[self.pos[0]+self.r[0],self.pos[1],self.pos[2]+self.r[2]]
        self.verts[6]=[self.pos[0]+self.r[0],self.pos[1]+self.r[1],self.pos[2]+self.r[2]]
        self.verts[7]=[self.pos[0],self.pos[1]+self.r[1],self.pos[2]+self.r[2]]
        # print(self.verts)
    def set_max(self): #擺放後X,Y,Z的最大值,用以計算是否大於後車箱
        self.max_xyz=[0.0,0.0,0.0]
        self.max_xyz[0]=self.pos[0]+self.r[0]
        self.max_xyz[1]=self.pos[1]+self.r[1]
        self.max_xyz[2]=self.pos[2]+self.r[2]      
        
class Luggage(Box): # 後車箱空間
    Lx=0.0   # 基準線位置
    Lz=0.0
    # TLx=0.0
    # TLz=0.0
# class end

# 主變數
inP=[[0.0,0.0,0.0]] # 可放置點
boxs=[] #箱子的種類: XXL, XL, L, M, S...

Ly=0.0
Lz=0.0
exbox=[] # 已置入的行李箱
n=0 # 箱子種類數
outbox=Luggage('wireframe',502.0,252.0,102.0,'red') # 劃外框用,無意義

##  設定箱子(貪心法,最長邊為X,其次為Y,再其次為Z向, 箱子由大至小排列)
cbox=Luggage('container',500.0,250.0,100.0,'red') # 後車箱
xxlbox=Box('XXL',320.0,85.0,35.0,'blue') # 超超大行李箱
boxs.append(xxlbox)
n+=1
xlbox=Box('XL',170.0,75.0,50.0,'black')    # 超大行李箱
boxs.append(xlbox)
n+=1
lbox=Box('L',80.0,40.0,20.0,'green')      # 大行李箱
boxs.append(lbox)
n+=1
mbox=Box('M',60.0,50.0,15.0,'brown')      # 中行李箱
boxs.append(mbox)
n+=1
sbox=Box('S',60.0,25.0,20.0,'white')      # 小行李箱
boxs.append(sbox)
n+=1
##

#
def check_col(verts,curbox,exbox): # 檢查放置的箱子是否和已放置的箱子有干涉
    # print('*** check_col')
    flag=False # 若干涉返回 True
    if len(exbox) > 0: #檢查所有已放置的箱子
        for i in range(0,len(exbox)):
            # exbox[i].set_box_dir()
            # exbox[i].set_verts() #依方向計算八點頂座標
            # flag=edge_plane_int(verts, exbox[i].verts) #邊線與對手平面是否有兩個交點
            # if flag:
            #     # print('edge_plane intersection')
            #     return flag #有干涉
                
            # flag=jm.face_face_int(curbox.verts, exbox[i].verts) #兩表面是否相交
            # if flag:
            #     return flag #有干涉
            # flag=jm.face_face_int(exbox[i].verts, curbox.verts) #兩表面是否相交
            # if flag:
            #     return flag #有干涉   
            flag=jm.coboid_coboid_int(exbox[i].verts, curbox.verts) #兩方體是否相交
            if flag:
                return flag #有干涉    
            # flag=jm.coboid_coboid_int(curbox.verts,exbox[i].verts ) #兩方體是否相交
            # if flag:
            #     return flag #有干涉                                   
            # for p in verts: # 檢查欲放置箱子的所有檢查點
            #     flag=jm.point_in_box(p,exbox[i].verts)
            #     # print(exbox[i]) 
            #     if flag:
            #         return flag
            # if flag==False:
            #     tmp_verts=[]
            #     tmp_verts.extend(exbox[i].verts) #加入對手件頂點
            #     tmp_verts.extend(edge_midPt(exbox[i].verts)) #加入對手件邊線中點
            #     tmp_verts.extend(face_midPt(exbox[i].verts)) #加入對手件表面中點
            #     tmp_verts.extend(solid_midPt(exbox[i].verts))#加入對手件體積中點
            #     for p in tmp_verts : # 檢查對手的頂點
            #         flag=jm.point_in_box(p,curbox.verts)
            #         # print('exbox verts has inside curbox')
            #         if flag:
            #             return flag
    else :
        flag=False #無干涉
    return flag


def greaterC(max_xyz,cboxb): # 是否大於後車箱
    # print('*** greaterC')
    flag=False # 若没超過後車箱, 返回 False
    for i in range(0,3):
        if max_xyz[i]>cbox.b[i]:
            return True
    for i in range(0,3):
        if max_xyz[i]<0:
            return True
    return flag

def boxin(curbox,exbox,cbox,inP): #是否可放入位置?
    # print('*** boxin')
    global Ly
    global Lz
    flag=True
    # print(inP[0])
    
    new_put_point=[0,0,0] #新增可放置點,初始化
    for p in inP: #檢查所有可放置點
        flag=True
        curbox.pos=p
        # if curbox.name=='L' and p==[100.0,0.0,60.0]:
        #     # print('LLL')
        #     pass
        for i in range(0,24): # 檢查不同擺設方向
            curbox.set_box_dir(i) #設定不同擺設方向
            tmp_verts=[] #計算點清空
            curbox.set_verts() #依方向計算八點頂座標
            tmp_verts.extend(curbox.verts) #加入頂點
            # print(len(tmp_verts))
            # print(curbox.name,i,p)
            #
            curbox.set_max() #擺放後X,Y,Z的最大值,用以計算是否大於後車箱
            if (Ly<curbox.max_xyz[1] or Lz<curbox.max_xyz[2]): #以基線限制無法擺入(砌磚法)
                flag=True
                continue
            else :
                flag=greaterC(curbox.max_xyz,cbox.b) # 是否大於後車箱
                if flag==False : #不大於後車箱, 再檢查其他...
                    # 干涉條件: 1.頂點插入對方 2.邊線中點插入對方 3.表面中點插入對方 4.邊線與對方面內兩交點的中點插入對方
                    #          4. 邊線與對方面共有兩個交點 5. 長方體中心於對方體內(完全重疊) 6. 表面相交
                    #          = 長方體相交
                    # tmp_verts.extend(edge_midPt(curbox.verts)) #加入邊線中點
                    # tmp_verts.extend(face_midPt(curbox.verts)) #加入表面中點
                    # tmp_verts.extend(solid_midPt(curbox.verts))#加入體積中點
                    # print(len(tmp_verts))
                    flag=check_col(tmp_verts,curbox,exbox) # 檢查放置的箱子是否和已放置的箱子有干涉
                    if flag==False : #無干涉
                        # inP 減少目前位置
                        # inP 新增可擺設位置
                        curbox.name=curbox.name+'_'+str(id(curbox))
                        exbox.append(curbox) #可擺放,所以將目前箱子加入已擺放箱子
                        #
                        print(' ')
                        print('Bin Name       : ', curbox.name)
                        print('Bin Postion    : ', curbox.pos)
                        print('Bin orientation: ', curbox.r)
                        # print(inP)
                        print('put in amound  : ', len(exbox)) #已擺入數
                        # print('Ly=newLy, Lz=newLz')
                        # 基線Ly新值
                        Ly=curbox.max_xyz[1]
                        # 基線LZ新值
                        Lz=curbox.max_xyz[2]

                        inP.remove(p) #可放置點中,移除目前箱子佔用點
                        for np in range(0,3): #新增三個可放置點
                            for nv in range(0,3):
                                new_put_point[nv]=curbox.pos[nv]
                            new_put_point[np]=new_put_point[np]+curbox.r[np]
                            inP.append(copy.deepcopy(new_put_point))
                        inP.sort(key=lambda x: x[1])
                        inP.sort(key=lambda x: x[0])
                        inP.sort(key=itemgetter(2,0)) #置放點排序,先Z->X->Y,如人放箱子時會靠邊放置
                        return flag 
                
    # flag=True
    return flag


def box_packing(n,inP,boxs,exbox,cbox): # 裝箱演算
    global Ly, Lz
    # list_num = [1, 1, 1, -1, -1, -1]
    # per = list(permutations(list_num, 3)) #排列
    cbox.set_verts()
    i=0
    while i < n: #測試所有n種類的箱子
        flag=True
        # inP.sort(key=lambda x: x[2])
        flag=boxin(copy.deepcopy(boxs[i]),exbox,cbox,inP) #是否有干涉, 若有Flag=True
        if flag==True:
            if Ly<cbox.r[1]: #無法置入,若其線Ly未放至最大則將其放大
                Ly=cbox.r[1]
                # print('Ly=MaxY')
                # i-=1
            else:
                if Lz<cbox.r[2]: #無法置入,若其線Lz未放至最大則將其放大
                    Lz=cbox.r[2]
                    # print('Lz=MaxZ')
                else:
                    i+=1 # calculate the next box,基線已加大若無法置入,此種箱子不再計算(已經放不下了!!)

        else:
            # print('add cbox to exbox.')
            # print('add new point to inP ')
            # print('Ly=newLy, Lz=newLz')
            pass
        # i+=1
    exV=0.0
    cV=cbox.b[0]*cbox.b[1]*cbox.b[2]
    for i in range(0,len(exbox)):
        exV=exV+exbox[i].b[0]*exbox[i].b[1]*exbox[i].b[2]
    print('fill rate: ', exV/cV) #填充率
    print('finished packing!!!') 

def opt_packing(n,inP,boxs,exbox,cbox): #調整條件,再作裝箱演算
    inP=[[0.0,0.0,0.0]] # 可放置點
    exbox=[]
    global Ly
    global Lz
    Ly=0.0
    Lz=0.0
    x=[0,1] #亂數改變箱子擺放順序或初始方位
    a=range(0,n)
    if x[0]==0:
        random.shuffle(boxs) #箱子順序改變
    else:
        random.shuffle(a) #取出第n個箱子
        li=boxs[a[0]]
        random.shuffle(li.b) #改變箱子的初始方位(l.w.h, l,h,w...)
    box_packing(n,inP,boxs,exbox,cbox) #裝箱演算

# 執行
# box_packing(n,inP,boxs,exbox,cbox)
# opt_packing(n,inP,boxs,exbox,cbox)

