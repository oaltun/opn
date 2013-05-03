function r=randmat(min,max,nrows,ncols,varargin)

if nargin>4 && isequal(varargin{1},'int')
    r = randi([min, max], nrows,ncols);
else
    r = min+ (max-min)*rand(nrows,ncols);
end

end