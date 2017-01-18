import rhinoscriptsyntax as rs
import math
import random

def anaCrv(site_crv,a):
    bb=rs.BoundingBox(site_crv)
    bb_poly=rs.AddPolyline([bb[0],bb[1],bb[2],bb[3],bb[0]])
    bb_srf=rs.AddPlanarSrf(bb_poly)
    srfUdom=rs.SurfaceDomain(bb_srf,0)
    srfVdom=rs.SurfaceDomain(bb_srf,1)
    umin=srfUdom[0]
    umax=srfUdom[1]
    vmin=srfVdom[0]
    vmax=srfVdom[1]
    ustep=a
    vstep=a
    i=umin
    while(i<umax):
        j=vmin
        while(j<vmax):
            temp_setback_crv=[]
            pt0=rs.EvaluateSurface(bb_srf,i,j)
            pt1=rs.EvaluateSurface(bb_srf,i+ustep,j)
            pt2=rs.EvaluateSurface(bb_srf,i+ustep,j+vstep)
            pt3=rs.EvaluateSurface(bb_srf,i,j+vstep)
            pt_crv=rs.AddPolyline([pt0,pt1,pt2,pt3,pt0])
            pt_list=[pt0,pt1,pt2,pt3,pt0]
            loc_arr.append(pt_list)
            pt_cen=rs.CurveAreaCentroid(pt_crv)[0]
            h=find_z(pt_cen,planeX)
            r=h  # height and r ratio
            cirX=rs.AddPolyline(getRegion(pt_cen,r))
            nX=len(setback_crv) # setback_crv is a global list
            if(nX==0):
                sum_check_site1=0
                for ptlistpts in pt_list:
                    ####   create tolerance zone here       ####
                    m_site1=checkTolerance(pt_cen,ptlistpts,site_crv,a)
                    if(m_site1 == 0):
                        sum_check_site1+=1
                    if(sum_check_site1==0):
                        li=[]
                        li.append(pt_cen)
                        li.append(r)
                        setback_crv.append(li)
                        lix=[]
                        lix.append(pt_list)
                        lix.append(r)
                        tower_crv.append(lix)
            else:
                sum=0
                for c in setback_crv:
                    #####       add polyline        ####
                    cirY=rs.AddPolyline(getRegion(c[0],c[1]))
                    ####   create tolerance zone here       ####
                    m0=rs.PointInPlanarClosedCurve(pt0,cirY)
                    #m0=checkToleranceS(pt_cen,pt0,cirY,a)
                    m1=rs.PointInPlanarClosedCurve(pt1,cirY)
                    #m1=checkToleranceS(pt_cen,pt1,cirY,a)
                    m2=rs.PointInPlanarClosedCurve(pt2,cirY)
                    #m2=checkToleranceS(pt_cen,pt2,cirY,a)
                    m3=rs.PointInPlanarClosedCurve(pt3,cirY)
                    #m3=checkToleranceS(pt_cen,pt3,cirY,a)
                    if(m0==1 or m1==1 or m2==1 or m3==1):
                        sum+=1
                    c_pt_arr=rs.CurvePoints(cirY)
                    for p in c_pt_arr:
                        n=rs.PointInPlanarClosedCurve(p,cirX)
                        if(n==1):
                            sum+=1
                    rs.DeleteObject(cirY)
                    #rs.DeleteObject(cirX)
                if(sum==0):
                    sum_check_site2=0
                    for ptlistpts in pt_list:
                        ####   create tolerance zone here       ####
                        #msite2=rs.PointInPlanarClosedCurve(ptlistpts,site_crv)
                        msite2=checkTolerance(pt_cen,ptlistpts,site_crv,a)
                        if(msite2==0):
                            sum_check_site2+=1
                    if(sum_check_site2==0):
                        li1=[]
                        li1.append(pt_cen)
                        li1.append(r)
                        setback_crv.append(li1)
                        lix1=[]
                        lix1.append(pt_list)
                        lix1.append(h)
                        tower_crv.append(lix1)
            rs.DeleteObject(cirX)
            rs.DeleteObject(pt_crv)
            j+=vstep
        i+=ustep
    rs.DeleteObject(bb_srf)
    rs.DeleteObject(bb_poly)


def getRegion(pt_cen, r):
    x=pt_cen[0]
    y=pt_cen[1]
    pt0=[x-r/2,y-r/2,0]
    pt1=[x+r/2,y-r/2,0]
    pt2=[x+r/2,y+r/2,0]
    pt3=[x-r/2,y+r/2,0]
    arr=[pt0,pt1,pt2,pt3,pt0]
    return arr


def orientCurvesHorizontal(crv, pt1, ang):    
    crvx=rs.RotateObject(crv, pt1, -ang)
    return crvx


def orientCurvesAligned(crv, pt1, ang):
    crvx=rs.RotateObject(crv, pt1, ang)
    return crvx


def srf_tri_func(srf,a):
    srfUdom=rs.SurfaceDomain(srf,0)
    srfVdom=rs.SurfaceDomain(srf,1)
    umax=srfUdom[1]
    umin=srfUdom[0]
    m=30
    vmax=srfVdom[1]
    vmin=srfVdom[0]
    n=30
    ustep=a
    vstep=a
    planeX=[]
    i=umin
    while i<umax:
        j=vmin
        while j<vmax:
            pt0=rs.EvaluateSurface(srf, i, j)
            planeX.append([pt0, ustep, vstep])
            j+=vstep
        i+=ustep
    return planeX

def find_z(pt,planeX):
    fpt=[]
    h=0
    for arr in planeX:
        ptx=arr[0][0]
        pty=arr[0][1]
        ptz=arr[0][2]
        ustep=arr[1]
        vstep=arr[2]
        if(pt[0]>ptx and pt[0]<ptx+ustep):
            if(pt[1]>pty and pt[1]<pty+vstep):
                fpt.append([pt[0],pt[1],ptz])
                h=ptz
    return h

def checkTolerance(cen_pt, pt, site_crv,a):
    mcen=rs.PointInPlanarClosedCurve(cen_pt, site_crv)
    m0=rs.PointInPlanarClosedCurve(pt,site_crv)
    if(mcen==1 or mcen==2):
        if(m0==0):
            param0=rs.CurveClosestPoint(site_crv,pt)
            ptx=rs.EvaluateCurve(site_crv,param0)
            fpt=rs.AddPoint(ptx)
            dx=rs.Distance(fpt,pt)
            if(dx<a):
                ret=1
            else:
                ret=0
            rs.DeleteObject(fpt)
        else:
            ret=1
    else:
        ret=0
    return ret


def checkToleranceS(cen_pt, pt, site_crv,a):
    mcen=rs.PointInPlanarClosedCurve(cen_pt, site_crv)
    m0=rs.PointInPlanarClosedCurve(pt,site_crv)
    if(mcen==1 or mcen==2):
        if(m0==0):
            param0=rs.CurveClosestPoint(site_crv,pt)
            ptx=rs.EvaluateCurve(site_crv,param0)
            fpt=rs.AddPoint(ptx)
            dx=rs.Distance(fpt,pt)
            if(dx<a):
                ret=1
            else:
                ret=0
            rs.DeleteObject(fpt)
        else:
            ret=1
    else:
        ret=0
    return ret


############################
#        MAIN LOOP         #
############################



#pt1=rs.GetPoint("pick orientation point 1")
#pt2=rs.GetPoint("pick orientation point 2")
#ang=rs.Angle(pt1,pt2)[0]    


setback_crv=[]
tower_crv=[]
allcurves=[]
loc_arr=[]
site_crvs=rs.GetObjects("pick sites")
a=20
t=10
guide_srf=rs.GetObject("Select guide surface for height")
planeX=srf_tri_func(guide_srf,a)

for site in site_crvs:
    #allcurves.append(site)
    #site_crv=orientCurvesHorizontal(site, pt1, ang)
    anaCrv(site,a)


#anaCrv(site_crv)
del_crv=[]

############################
#      END MAIN LOOP       #
############################


f_setback_crv=[]

for c in setback_crv:
    if(c not in f_setback_crv):
        f_setback_crv.append(c)

for c in f_setback_crv:
    cx=getRegion(c[0],c[1])
    crv=rs.AddPolyline(cx)
    crv_cen=rs.CurveAreaCentroid(crv)[0]
    #crvx=rs.AddPolyline(getRegion(crv_cen,c[1]))


for c in tower_crv:
    crvx=rs.AddPolyline(c[0])
    l=rs.AddLine([0,0,0],[0,0,c[1]])
    rs.ExtrudeCurve(crvx,l)
    rs.DeleteObject(l)
    rs.DeleteObject(crvx)

"""
for c in loc_arr:
    cx=rs.AddPolyline(c)
    crv_pts=rs.CurvePoints(cx)
    sum=0
    for p in crv_pts:
        for site in site_crvs:
            m=rs.PointInPlanarClosedCurve(p,site)
            if(m==0):
                sum+=1
    if(sum==0):
        rs.AddPolyline(c)
"""
for site in site_crvs:
    rs.AddHatch(site,"Plus", 5.0,0.0)
