import rhinoscriptsyntax as rs
import math

def anaSite(site_crv,a,b,d,h,t):
    d=d/2
    #OFFSET SITE_CURVE OUTSIDE
    site_crv_pts=rs.CurvePoints(site_crv)
    crvPt1=site_crv_pts[0]
    pt_off=[crvPt1[0],crvPt1[0],0]
    pt=rs.AddPoint(pt_off)
    crv=rs.OffsetCurve(site_crv, pt_off, d)
    rs.DeleteObject(pt)
    
    bb=rs.BoundingBox(crv)
    bb_pl=rs.AddPolyline([bb[0],bb[1],bb[2],bb[3],bb[0]])
    bb_srf=rs.AddPlanarSrf(bb_pl)

    side_modU=a+2*d
    side_modV=b+2*d
    srfUdom=rs.SurfaceDomain(bb_srf,0)
    srfVdom=rs.SurfaceDomain(bb_srf,1)
    umax=srfUdom[1]
    umin=srfUdom[0]
    ustep=side_modU
    vmin=srfVdom[0]
    vmax=srfVdom[1]
    vstep=side_modV
    tower_crv=[]
    setback_crv=[]
    i=umin
    while(i<umax):
        j=vmin
        while(j<vmax):
            pt0=rs.EvaluateSurface(bb_srf,i,j)
            pt1=rs.EvaluateSurface(bb_srf,i+ustep,j)
            pt2=rs.EvaluateSurface(bb_srf,i+ustep,j+vstep)
            pt3=rs.EvaluateSurface(bb_srf,i,j+vstep)
            
            pl_crv=rs.AddPolyline([pt0,pt1,pt2,pt3,pt0])
            
            c0=rs.CurveAreaCentroid(pl_crv)[0]
            tpl_pt0=[c0[0]-a/2, c0[1]-b/2, 0]
            tpl_pt1=[c0[0]+a/2, c0[1]-b/2, 0]
            tpl_pt2=[c0[0]+a/2, c0[1]+b/2, 0]
            tpl_pt3=[c0[0]-a/2, c0[1]+b/2, 0]
            temp_tower_crv=rs.AddPolyline([tpl_pt0,tpl_pt1,tpl_pt2,tpl_pt3,tpl_pt0])
            temp_tower_crv_cen=rs.CurveAreaCentroid(temp_tower_crv)[0]
            mcen=rs.PointInPlanarClosedCurve(temp_tower_crv_cen, site_crv)
            m0=rs.PointInPlanarClosedCurve(tpl_pt0,site_crv)
            m1=rs.PointInPlanarClosedCurve(tpl_pt1,site_crv)
            m2=rs.PointInPlanarClosedCurve(tpl_pt2,site_crv)
            m3=rs.PointInPlanarClosedCurve(tpl_pt3,site_crv)
            if(mcen==1 or mcen==2):
                if(m0==0):
                    param0=rs.CurveClosestPoint(site_crv,tpl_pt0)
                    pt0X=rs.EvaluateCurve(site_crv,param0)
                    fpt=rs.AddPoint(pt0X)
                    dx=rs.Distance(fpt,tpl_pt0)
                    if( ((dx)<(a/t)) and ((dx)<(b/t)) ):
                        tower_crv.append(temp_tower_crv)
                        setback_crv.append(pl_crv)
                    else:
                        #print("m0 failed")
                        #rs.AddTextDot("x0",tpl_pt0)
                        allcurves.append(temp_tower_crv)
                        allcurves.append(pl_crv)
                    rs.DeleteObject(fpt)
                elif(m1==0):
                    param1=rs.CurveClosestPoint(site_crv,tpl_pt1)
                    pt1X=rs.EvaluateCurve(site_crv,param1)
                    fpt=rs.AddPoint(pt1X)
                    dx=rs.Distance(fpt,tpl_pt1)
                    if( ((dx)<(a/t)) and ((dx)<(b/t)) ):
                        tower_crv.append(temp_tower_crv)
                        setback_crv.append(pl_crv)
                    else:
                        #print("m1 failed")
                        #rs.AddTextDot("x1",tpl_pt1)
                        allcurves.append(temp_tower_crv)
                        allcurves.append(pl_crv)
                    rs.DeleteObject(fpt)
                elif(m2==0):
                    param2=rs.CurveClosestPoint(site_crv,tpl_pt2)
                    pt2X=rs.EvaluateCurve(site_crv,param2)
                    fpt=rs.AddPoint(pt2X)
                    dx=rs.Distance(fpt,tpl_pt2)
                    if( (dx<(a/t)) and (dx<(b/t)) ):
                        tower_crv.append(temp_tower_crv)
                        setback_crv.append(pl_crv)
                    else:
                        #print("m2 failed")
                        #rs.AddTextDot("x2",tpl_pt2)
                        allcurves.append(temp_tower_crv)
                        allcurves.append(pl_crv)
                    rs.DeleteObject(fpt)
                elif(m3==0):
                    param3=rs.CurveClosestPoint(site_crv,tpl_pt3)
                    pt3X=rs.EvaluateCurve(site_crv,param3)
                    fpt=rs.AddPoint(pt3X)
                    dx=rs.Distance(fpt,tpl_pt3)
                    if( ((dx)<(a/t)) and ((dx)<(b/t)) ):
                        tower_crv.append(temp_tower_crv)
                        setback_crv.append(pl_crv)
                    else:
                        #print("m3 failed")
                        #rs.AddTextDot("x3",tpl_pt3)
                        allcurves.append(temp_tower_crv)
                        allcurves.append(pl_crv)
                    rs.DeleteObject(fpt)
                else:
                    tower_crv.append(temp_tower_crv)
                    setback_crv.append(pl_crv)
            else:
                rs.DeleteObject(pl_crv)
                rs.DeleteObject(temp_tower_crv)
                
            j+=vstep
        i+=ustep

    for c in tower_crv:
        srf=rs.AddPlanarSrf(c)
        lext=rs.AddLine([0,0,0],[0,0,h])
        xsrf=rs.ExtrudeSurface(srf,lext)
        rs.DeleteObject(srf)
        rs.DeleteObject(lext)
        allcurves.append(xsrf)

    for c in setback_crv:
        #rs.DeleteObject(c)
        pass
        
    rs.DeleteObject(bb_pl)
    rs.DeleteObject(bb_srf)
    rs.DeleteObject(crv)
    
    for crv in tower_crv:
        allcurves.append(crv)
        
    for crv in setback_crv:
        allcurves.append(crv)
        
    sol.append(tower_crv)
    sol.append(setback_crv)
    return sol



def orientCurvesHorizontal(crv, pt1, ang):    
    crvx=rs.RotateObject(crv, pt1, -ang)
    return crvx

def orientCurvesAligned(crv, pt1, ang):
    crvx=rs.RotateObject(crv, pt1, ang)
    return crvx




sites=rs.GetObjects("Pick all sites")
"""
a=rs.GetInteger("Enter side 1",27.5,5,200)
b=rs.GetInteger("Enter side 2",27.5,5,50)
d=rs.GetInteger("Enter distance from block edge",25,10,50)
h=rs.GetReal("Enter the height of the tower",50,5,200)
t=rs.GetReal("Enter the tolerance (t->a/t,b/t)",10,1,100)
"""
a=27.5
b=27.5
d=25
h=50
t=4
#"""

pt1=rs.GetPoint("pick orientation point 1")
pt2=rs.GetPoint("pick orientation point 2")
ang=rs.Angle(pt1,pt2)[0]    

sol=[]
allcurves=[]
for site in sites:
    allcurves.append(site)
    site=orientCurvesHorizontal(site, pt1, ang)
    anaSite(site,a,b,d,h,t)

for crv in allcurves:
    orientCurvesAligned(crv, pt1, ang)

for site in sites:
    rs.AddHatch(site,"Plus", 5.0,0.0)


