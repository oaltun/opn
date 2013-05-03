%%% connect by line:
%%% connects point1 and point1 with a line
%%% points can be 2 or 3 dimensional.
function connectbl(point1,point2, varargin)
mat = [point1
       point2];
   


x=mat(:,1);
y=mat(:,2);

n=size(mat,2);
if n>2
    z=mat(:,3);
    plot3(x,y,z,varargin{:});
else
    plot(x,y,varargin{:});
end


    
