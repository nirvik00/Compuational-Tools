import rhinoscriptsyntax as rs
import math
import random
import operator



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


def crvAna(site_crv):
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
            r1=random.randrange(10,50)
            pt=[]
            pt.append(rs.EvaluateSurface(bb_srf,i,j))
            pt.append(rs.EvaluateSurface(bb_srf,i+ustep,j))
            pt.append(rs.EvaluateSurface(bb_srf,i+ustep,j+vstep))
            pt.append(rs.EvaluateSurface(bb_srf,i,j+vstep))
            pt.append(rs.EvaluateSurface(bb_srf,i,j))
            pt_crv=rs.AddPolyline(pt)
            pt_cen=rs.CurveAreaCentroid(pt_crv)[0]
            h=find_z(pt_cen,planeX)
            r=h/2+10
            crvX=rs.AddPolyline(getRegion(pt_cen,h))
            sum=0
            for p in pt:
                #m=rs.PointInPlanarClosedCurve(p,site_crv)
                m=checkToleranceSingle(pt_cen,p,site_crv)
                if(m>0):
                    rs.DeleteObject(crvX)
                    #pass
                else:
                    makeRect(pt[0],a,h)
                    crvY=rs.AddPolyline(getRegion(pt_cen,h))
                rs.DeleteObject(pt_crv)
                rs.DeleteObject(crvX)
                vstep=r
            j+=vstep
            ustep=r
        i+=ustep
    rs.DeleteObject(bb_srf)
    rs.DeleteObject(bb_poly)

def makeRect(pt,a,h):
    x=pt[0]
    y=pt[1]
    z=h
    ptx=[]
    
    ptx.append([x,y,0])
    ptx.append([x+a,y,0])
    ptx.append([x+a,y+a,0])
    ptx.append([x,y+a,0])
    ptx.append([x,y,0])
    crv=rs.AddPolyline(ptx)
    crv_cen=rs.CurveAreaCentroid(crv)[0]
    x=checkTolerance(crv_cen, ptx, site_crv)
    if(x>0):
        rs.DeleteObject(crv)
    else:
        le=rs.AddLine([0,0,0],[0,0,h])
        rs.ExtrudeCurve(crv,le)
        rs.DeleteObject(le)


def checkTolerance(cen_pt, pts, site_crv):
    mcen=rs.PointInPlanarClosedCurve(cen_pt, site_crv)
    sum=0
    if (mcen==1):
        for pt in pts:
            m=rs.PointInPlanarClosedCurve(pt,site_crv)
            if(m==0):
                param=rs.CurveClosestPoint(site_crv, pt)
                ptx=rs.EvaluateCurve(site_crv,param)
                fpt=rs.AddPoint(ptx)
                dx=rs.Distance(fpt,pt)
                if(dx<a*t):
                    sum=0
                else:
                    sum+=1
                rs.DeleteObject(fpt)
            else:
                sum=0
    else:
        sum+=1
    return sum

def checkToleranceSingle(cen_pt, pt, site_crv):
    mcen=rs.PointInPlanarClosedCurve(cen_pt, site_crv)
    sum=0
    if (mcen==1):
        m=rs.PointInPlanarClosedCurve(pt,site_crv)
        if(m==0):
            param=rs.CurveClosestPoint(site_crv, pt)
            ptx=rs.EvaluateCurve(site_crv,param)
            fpt=rs.AddPoint(ptx)
            dx=rs.Distance(fpt,pt)
            if(dx<a*t):
                sum=0
            else:
                sum+=1
            rs.DeleteObject(fpt)
        else:
            sum=0
    else:
        sum+=1
    return sum


def getRegion(pt_cen, r):
    x=pt_cen[0]
    y=pt_cen[1]
    pt0=[x-r/2,y-r/2,0]
    pt1=[x+r/2,y-r/2,0]
    pt2=[x+r/2,y+r/2,0]
    pt3=[x-r/2,y+r/2,0]
    arr=[pt0,pt1,pt2,pt3,pt0]
    return arr



setback_crv=[]
tower_crv=[]
a=20
t=10/1
guide_srf=rs.GetObject("pick guide surface")
planeX=srf_tri_func(guide_srf,a)
site_crvs=rs.GetObjects("pick all lots in the site")

for site_crv in site_crvs:
    crvAna(site_crv)
    le=rs.AddLine([0,0,0],[0,0,a/10])
    ext=rs.ExtrudeCurve(site_crv,le)
    rs.DeleteObject(le)


for site in site_crvs:
    rs.AddHatch(site,"Plus", 5.0,0.0)