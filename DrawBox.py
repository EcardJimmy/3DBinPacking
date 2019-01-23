# -*- coding: utf-8 -*-
import numpy as np
import copy 
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import matplotlib.pyplot as plt
import Packing3D as pk #Packing3D.py

def fill_box_verts(verts): #繪著色方體
    v=verts
    tvs=[[v[0],v[1],v[2],v[3]],
        [v[4],v[5],v[6],v[7]], 
        [v[0],v[1],v[5],v[4]], 
        [v[2],v[3],v[7],v[6]], 
        [v[1],v[2],v[6],v[5]],
        [v[4],v[7],v[3],v[0]]]
    return tvs

def draw_cbox(ax): #劃外框線
        pk.outbox.pos=[-1.5,-1.5,-1.5]
        pk.outbox.set_verts()
        for i in range(0,3):
                wire_cbox=zip(pk.outbox.verts[i],pk.outbox.verts[i+1])
                ax.plot3D(wire_cbox[0],wire_cbox[1],wire_cbox[2],linewidth=3,color="y")
        for i in range(4,7):
                wire_cbox=zip(pk.outbox.verts[i],pk.outbox.verts[i+1])
                ax.plot3D(wire_cbox[0],wire_cbox[1],wire_cbox[2],linewidth=3,color="y")    
        wire_cbox=zip(pk.outbox.verts[0],pk.outbox.verts[3])
        ax.plot3D(wire_cbox[0],wire_cbox[1],wire_cbox[2],linewidth=3,color="y")   
        wire_cbox=zip(pk.outbox.verts[4],pk.outbox.verts[7])
        ax.plot3D(wire_cbox[0],wire_cbox[1],wire_cbox[2],linewidth=3,color="y")   
        wire_cbox=zip(pk.outbox.verts[0],pk.outbox.verts[4])
        ax.plot3D(wire_cbox[0],wire_cbox[1],wire_cbox[2],linewidth=3,color="y")  
        wire_cbox=zip(pk.outbox.verts[1],pk.outbox.verts[5])
        ax.plot3D(wire_cbox[0],wire_cbox[1],wire_cbox[2],linewidth=3,color="y")   
        wire_cbox=zip(pk.outbox.verts[2],pk.outbox.verts[6])
        ax.plot3D(wire_cbox[0],wire_cbox[1],wire_cbox[2],linewidth=3,color="y")  
        wire_cbox=zip(pk.outbox.verts[3],pk.outbox.verts[7])
        ax.plot3D(wire_cbox[0],wire_cbox[1],wire_cbox[2],linewidth=3,color="y") 

def run_plot():  # 執行圖形繪製
    pk.box_packing(pk.n,pk.inP,pk.boxs,pk.exbox,pk.cbox) #執行Packing3D.py中box_packing()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # ax=Axes3D(fig)
    ax.set_aspect("equal")
    ax.set_xlabel('X')
    ax.set_xlim3d(-10, 520)
    ax.set_ylabel('Y')
    ax.set_ylim3d(-10, 270)
    ax.set_zlabel('Z')
    ax.set_zlim3d(-10, 120)
#     pk.exbox=[]
#     pk.xlbox.set_verts
#     pk.exbox.append(pk.xlbox)

#     draw_cbox(ax) #外框線
    fill_vts=np.zeros((6,4,3))
    for i in range(0,len(pk.exbox)): #繪製每一箱子
        pk.exbox[i].set_verts
        fill_vts=fill_box_verts(pk.exbox[i].verts)
        # plot sides
        ax.add_collection3d(Poly3DCollection(fill_vts, 
            facecolors=pk.exbox[i].color, linewidths=1, edgecolors='r', alpha=0.5))
    plt.show()
    print('end')

def run_optplot():  # 執行圖形繪製
#     pk.box_packing(pk.n,pk.inP,pk.boxs,pk.exbox,pk.cbox) #執行Packing3D.py中box_packing()
    pk.opt_packing(pk.n,pk.inP,pk.boxs,pk.exbox,pk.cbox)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # ax=Axes3D(fig)
    ax.set_aspect("equal")
    ax.set_xlabel('X')
    ax.set_xlim3d(-10, 520)
    ax.set_ylabel('Y')
    ax.set_ylim3d(-10, 270)
    ax.set_zlabel('Z')
    ax.set_zlim3d(-10, 120)

    draw_cbox(ax) #外框線
    fill_vts=np.zeros((6,4,3))
    for i in range(0,len(pk.exbox)):
        pk.exbox[i].set_verts
        fill_vts=fill_box_verts(pk.exbox[i].verts)
        # plot sides
        ax.add_collection3d(Poly3DCollection(fill_vts, 
            facecolors=pk.exbox[i].color, linewidths=1, edgecolors='r', alpha=0.5))
    plt.show()
    print('end')



