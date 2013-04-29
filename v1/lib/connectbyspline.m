%%% connect 2 3d points by spline

% 
% function example
%     fun([1,2,3],[4,5,6],30)
%     
% end
function fun(point1,point2,alpha, varargin)
    
    %%%get z4. see get_z4.jpg    
    point3=(point1+point2)/2;
    [x1,y1,z1]=dealarray(point1);
    [x3,y3,z3]=dealarray(point3);
    [x4,y4]=dealarray([x3,y3]);
    
    h=sqrt(sum((point1-point3).^2));
    k=h/cos(alpha);
    dz2=k^2-(x1-x4)^2-(y1-y4)^2;
    z4plus=z1+sqrt(dz2);
    z4minus=z1-sqrt(dz2);
    z4=max(z4plus,z4minus);
    
    point4 = [x4,y4,z4];
    
    
    
    coord = [point1
        point4
        point2]';
    
    pts=fnplt(cscvn(coord));
    x=pts(1,:);
    y=pts(2,:);
    z=pts(3,:);
    
    plot3(x,y,z,varargin{:});
    
end

