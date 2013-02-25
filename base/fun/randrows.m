%%% produce a matrix that has rows with random numbers. Each row is same
%%% with other. cells of rows change.
function r=randrows(min,max,nrows,ncols,varargin)
if nargin>4 && isequal(varargin{1},'int')
    r = randi([min max], nrows, 1);
else
    r = min + (max - min) * rand(nrows,1);
end
r = repmat(r, 1, ncols);