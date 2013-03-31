function a = fixbound2bound(lb,ub,a)
a(a>ub)=ub(a>ub);
a(a<lb)=lb(a<lb);