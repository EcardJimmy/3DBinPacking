# -*- coding: utf-8 -*-
import numpy as np
import copy
from math import sin, cos, acos, sqrt

# quaternions 四元數
def normalize(v, tolerance=0.00001): #向量單位長
    mag2 = sum(n * n for n in v)
    if mag2 ==0: #向量長度為零
        v = tuple(n / 1 for n in v)
        return v
    if abs(mag2 - 1.0) > tolerance:
        mag = sqrt(mag2)
        v = tuple(n / mag for n in v)
    return v

def q_mult(q1, q2): #兩個四元數相乘
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
    z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2
    return w, x, y, z

def q_conjugate(q): #共軛四元數(四元數倒數)
    w, x, y, z = q
    return (w, -x, -y, -z)

def qv_mult(q1, v1): #旋轉後新的四元數v'=qvq-1
    q2 = (0.0,) + tuple(v1)
    return q_mult(q_mult(q1, q2), q_conjugate(q1))[1:]

def axisangle_to_q(v, theta): #軸角轉為四元數
    v = normalize(v)
    x, y, z = v
    theta /= 2
    w = cos(theta)
    x = x * sin(theta)
    y = y * sin(theta)
    z = z * sin(theta)
    return w, x, y, z

def q_to_axisangle(q): #四元數轉為軸角
    w, v = q[0], q[1:]
    theta = acos(w) * 2.0
    return normalize(v), theta
    
## Example
# x_axis_unit = (1, 0, 0)
# y_axis_unit = (0, 1, 0)
# z_axis_unit = (0, 0, 1)
# r1 = axisangle_to_q(x_axis_unit, numpy.pi / 2)
# r2 = axisangle_to_q(y_axis_unit, numpy.pi / 2)
# r3 = axisangle_to_q(z_axis_unit, numpy.pi / 2)
# v = qv_mult(r1, y_axis_unit)
# v = qv_mult(r2, v)
# v = qv_mult(r3, v)
# print v
# # output: (0.0, 1.0, 2.220446049250313e-16)

def angle_between(v1, v2): #Returns the angle in radians between vectors 'v1' and 'v2'
    v1_u = normalize(v1)
    v2_u = normalize(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)) #向量點積性質 a.b = |a|*|b|*cos(th)



def coboid_coboid_int(eb, cb) : # 一方體若不落在另一方體內,則不相交
    flag=False
    cxmin=min(cb[0][0],cb[1][0],cb[2][0],cb[3][0],cb[4][0],cb[5][0],cb[6][0],cb[7][0])
    cxmax=max(cb[0][0],cb[1][0],cb[2][0],cb[3][0],cb[4][0],cb[5][0],cb[6][0],cb[7][0])
    cymin=min(cb[0][1],cb[1][1],cb[2][1],cb[3][1],cb[4][1],cb[5][1],cb[6][1],cb[7][1])
    cymax=max(cb[0][1],cb[1][1],cb[2][1],cb[3][1],cb[4][1],cb[5][1],cb[6][1],cb[7][1])
    czmin=min(cb[0][2],cb[1][2],cb[2][2],cb[3][2],cb[4][2],cb[5][2],cb[6][2],cb[7][2])
    czmax=max(cb[0][2],cb[1][2],cb[2][2],cb[3][2],cb[4][2],cb[5][2],cb[6][2],cb[7][2])

    exmin=min(eb[0][0],eb[1][0],eb[2][0],eb[3][0],eb[4][0],eb[5][0],eb[6][0],eb[7][0])
    exmax=max(eb[0][0],eb[1][0],eb[2][0],eb[3][0],eb[4][0],eb[5][0],eb[6][0],eb[7][0])
    eymin=min(eb[0][1],eb[1][1],eb[2][1],eb[3][1],eb[4][1],eb[5][1],eb[6][1],eb[7][1])
    eymax=max(eb[0][1],eb[1][1],eb[2][1],eb[3][1],eb[4][1],eb[5][1],eb[6][1],eb[7][1])
    ezmin=min(eb[0][2],eb[1][2],eb[2][2],eb[3][2],eb[4][2],eb[5][2],eb[6][2],eb[7][2])
    ezmax=max(eb[0][2],eb[1][2],eb[2][2],eb[3][2],eb[4][2],eb[5][2],eb[6][2],eb[7][2])

    if (cxmin<=exmin and cxmax<=exmin) or (cxmin>=exmax and cxmax >=exmax) \
       or (cymin<=eymin and cymax<=eymin) or (cymin>=eymax and cymax >=eymax) \
       or (czmin<=ezmin and czmax<=ezmin) or (czmin>=ezmax and czmax >=ezmax) :
       flag=False
    else:
        flag=True
        return flag
    return flag

def line_two_point(p0,p1): #兩點線, 返回線上一點,線向量
    # print('*** line_two_point')
    lp=p0
    lv=[p1[0]-p0[0],p1[1]-p0[1],p1[2]-p0[2]]
    return lp, lv #返回線上一點及線向量

def line_parameter(lp,lv): # 線上一點及線向量,計算返回直線參數方程式係數
    # 直線參數方程式
    # x = lp[0]+ lv[0] * t
    # y = lp[1]+ lv[1] * t 
    # z = lp[2]+ lv[2] * t
    return lp, lv

def plane_three_point(p0,p1,p2): #三點定義. 返回原點,平面法向
    # print('*** plane_three_point')
    op=p1 #設平面原點
    v0=[p0[0]-op[0],p0[1]-op[1],p0[2]-op[2]]
    v1=[p2[0]-op[0],p2[1]-op[1],p2[2]-op[2]]
    vn=np.cross(v1,v0)
    return op,vn #返回原點及平面法向

def plane_four_point(p0,p1,p2,p3): #平面四個頂點
    # print('*** plane_four_point')
    return [p0,p1,p2,p3]


def cal_plane_line_int_point(op,vn,lp,lv): # 計算平面與直線交點
    # 法向量平面方程式
    # vn[0]*(X-op[0])+vn[1]*(Y-op[1])+vn[2]*(Z-op[2])=0

    # 平面-直線交點 = 平面方程與直線方程 聯立
    # t = (op[0] – lp[0])*vn[0]+(op[1] – lp[1])*vn[1]+(op[2] – lp[2])*vn[2]) / (vn[0]* lv[0]+ vn[1]* lv[1]+ vn[2]* lv[2])
    # 若分母為零, 表示直線與面平行, 無交點
    # print('*** cal_plane_line_int_point')
    result=[0,0,0]
    chk=vn[0]* lv[0]+ vn[1]* lv[1]+ vn[2]* lv[2]
    if chk==0:
        result=None
    else:
        t = ((op[0] - lp[0]) * vn[0] + (op[1] - lp[1]) * vn[1] + (op[2] - lp[2]) * vn[2]) / chk
        result[0]=lp[0]+lv[0]*t
        result[1]=lp[1]+lv[1]*t
        result[2]=lp[2]+lv[2]*t
    return result #返回交點或None



def point_in_face(ip,face_p,op,vn): # 點是否落在四頂點所圍成範圍內
    # print('*** point_in_face')
    nip=list(ip) #交點
    nface_p=copy.deepcopy(face_p) #面的四頂點
    flag_in=False
    
    #平移回原點
    for i in range(0,3):
        nip[i]=ip[i]-op[i]
        nface_p[0][i]=face_p[0][i]-op[i]
        nface_p[1][i]=face_p[1][i]-op[i]
        nface_p[2][i]=face_p[2][i]-op[i]
        nface_p[3][i]=face_p[3][i]-op[i]
    # print(nface_p)
    #旋轉成面與Z軸垂直
    agl=angle_between(vn,[0,0,1])
    # print(agl*180/np.pi)
    ax=np.cross(vn,[0,0,1])
    qax=axisangle_to_q(ax,agl)
    nip=qv_mult(qax,nip)
    nface_p[0]=qv_mult(qax,nface_p[0])
    nface_p[1]=qv_mult(qax,nface_p[1])
    nface_p[2]=qv_mult(qax,nface_p[2])
    nface_p[3]=qv_mult(qax,nface_p[3])
    vts_f=[nface_p[0],nface_p[1],nface_p[2],nface_p[3]] #面上的四頂點
    # print(vts_f) # 轉換完面的頂點座標

    #範圍
    xmin=min(vts_f[0][0],vts_f[1][0],vts_f[2][0],vts_f[3][0])
    xmax=max(vts_f[0][0],vts_f[1][0],vts_f[2][0],vts_f[3][0])
    ymin=min(vts_f[0][1],vts_f[1][1],vts_f[2][1],vts_f[3][1])
    ymax=max(vts_f[0][1],vts_f[1][1],vts_f[2][1],vts_f[3][1])

    if (nip[0]<= xmin or nip[0]>= xmax) or (nip[1] <= ymin or  nip[1] >= ymax):
        flag_in=False #不在範圍內
    else:
        flag_in=True #在範圍內
    return flag_in

def point_in_box(point,verts): # 點是否落在箱子所圍成範圍內
    # print('*** point_in_box')
    flag=False
    v=verts
    p=point
    #範圍
    xmin=min(v[0][0],v[1][0],v[2][0],v[3][0],v[4][0],v[5][0],v[6][0],v[7][0])
    xmax=max(v[0][0],v[1][0],v[2][0],v[3][0],v[4][0],v[5][0],v[6][0],v[7][0])
    ymin=min(v[0][1],v[1][1],v[2][1],v[3][1],v[4][1],v[5][1],v[6][1],v[7][1])
    ymax=max(v[0][1],v[1][1],v[2][1],v[3][1],v[4][1],v[5][1],v[6][1],v[7][1])
    zmin=min(v[0][2],v[1][2],v[2][2],v[3][2],v[4][2],v[5][2],v[6][2],v[7][2])
    zmax=max(v[0][2],v[1][2],v[2][2],v[3][2],v[4][2],v[5][2],v[6][2],v[7][2])
    if (p[0]<= xmin or p[0]>= xmax) or (p[1] <= ymin or p[1] >= ymax) or (p[2] <= zmin or p[2] >= zmax):
        flag=False #不在範圍內
    else:
        flag=True #在範圍內    
    return flag

    
def edge_midPt(verts): #邊線中點
    # print('*** edge_midPt')
    edge_mp=np.zeros((12,3))
    for i in range(0,7):
        edge_mp[i]=[(verts[i+1][0]+verts[i][0])/2.0,
                    (verts[i+1][1]+verts[i][1])/2.0,
                    (verts[i+1][2]+verts[i][2])/2.0]
        # print(i)
    edge_mp[7]=[(verts[7][0]+verts[0][0])/2.0,
                (verts[7][1]+verts[0][1])/2.0,
                (verts[7][2]+verts[0][2])/2.0]        
    for i in range(0,4):
        edge_mp[8+i]=[(verts[4+i][0]+verts[i][0])/2.0,
                    (verts[4+i][1]+verts[i][1])/2.0,
                    (verts[4+i][2]+verts[i][2])/2.0]
    # print(edge_mp)
    return edge_mp

def face_midPt(verts): #表面中點
    # print('*** face_midPt')
    face_mp=np.zeros((6,3))
    face_mp[0]=[(verts[2][0]+verts[0][0])/2.0,
                (verts[2][1]+verts[0][1])/2.0,
                (verts[2][2]+verts[0][2])/2.0] #底面中點
    face_mp[1]=[(verts[6][0]+verts[4][0])/2.0,
                (verts[6][1]+verts[4][1])/2.0,
                (verts[6][2]+verts[4][2])/2.0] #頂面中點
    face_mp[2]=[(verts[5][0]+verts[0][0])/2.0,
                (verts[5][1]+verts[0][1])/2.0,
                (verts[5][2]+verts[0][2])/2.0] #前面中點
    face_mp[3]=[(verts[7][0]+verts[2][0])/2.0,
                (verts[7][1]+verts[2][1])/2.0,
                (verts[7][2]+verts[2][2])/2.0] #後面中點
    face_mp[4]=[(verts[6][0]+verts[1][0])/2.0,
                (verts[6][1]+verts[1][1])/2.0,
                (verts[6][2]+verts[1][2])/2.0] #右面中點
    face_mp[5]=[(verts[7][0]+verts[0][0])/2.0,
                (verts[7][1]+verts[0][1])/2.0,
                (verts[7][2]+verts[0][2])/2.0] #左面中點 
    # print(face_mp)
    return face_mp

def solid_midPt(verts): #體積中點
    # print('*** edge_midPt')
    solid_mp=np.zeros((1,3))
    solid_mp[0]=[(verts[0][0]+verts[6][0])/2.0,
                (verts[0][1]+verts[6][1])/2.0,
                (verts[0][2]+verts[6][2])/2.0]
    # print(solid_mp)
    return solid_mp

def edge_plane_int(cur_vts, ex_vts): #邊線與存在箱子兩平面有相交
    # print('*** edge_plane_int')
    flag=False
    edges=[] #長方體12個邊線
    faces=[] #長方體6個面[op,vn]
    faces4p=[] #面用4個頂點表示[p0,p1,p2,p3]
    for i in range(0,3):
        edges.append(line_two_point(cur_vts[i+1],cur_vts[i]))
    for i in range(4,7):
        edges.append(line_two_point(cur_vts[i+1],cur_vts[i]))
        # print(i)
    edges.append(line_two_point(cur_vts[3],cur_vts[0]))   
    edges.append(line_two_point(cur_vts[7],cur_vts[4]))      
    for i in range(0,4):
        edges.append(line_two_point(cur_vts[4+i],cur_vts[i]))
    # print(len(edges))
    faces.append(plane_three_point(ex_vts[0],ex_vts[1],ex_vts[2]))
    faces.append(plane_three_point(ex_vts[4],ex_vts[5],ex_vts[6]))
    faces.append(plane_three_point(ex_vts[0],ex_vts[1],ex_vts[5]))
    faces.append(plane_three_point(ex_vts[3],ex_vts[2],ex_vts[6]))
    faces.append(plane_three_point(ex_vts[1],ex_vts[2],ex_vts[6]))
    faces.append(plane_three_point(ex_vts[0],ex_vts[3],ex_vts[7]))
    # axis=np.cross([faces[2][1]],[0,0,1])
    # print(axis)
    faces4p.append(plane_four_point(ex_vts[0],ex_vts[1],ex_vts[2],ex_vts[3]))
    faces4p.append(plane_four_point(ex_vts[4],ex_vts[5],ex_vts[6],ex_vts[7]))
    faces4p.append(plane_four_point(ex_vts[0],ex_vts[1],ex_vts[5],ex_vts[4]))
    faces4p.append(plane_four_point(ex_vts[3],ex_vts[2],ex_vts[6],ex_vts[7]))
    faces4p.append(plane_four_point(ex_vts[1],ex_vts[2],ex_vts[6],ex_vts[5]))
    faces4p.append(plane_four_point(ex_vts[0],ex_vts[3],ex_vts[7],ex_vts[4]))
    # print(faces4p)
    k=0
    result=[0,0,0]
    flag_in=True
    for i in range(0,12):
        for j in range(0,6):
             # 計算平面與直線交點
            result=cal_plane_line_int_point(faces[j][0],faces[j][1],edges[i][0],edges[i][1])
            if result != None:
                # 點是否落在四頂點所圍成範圍內
                # result=[50,40,0] #for test...
                flag_in=point_in_face(result,faces4p[j],faces[j][0],faces[j][1])
                if flag_in:
                    k+=1
    if k>=2:
        flag=True #干涉
    else :
        flag=False #無干涉
    return flag