% function example
% 
% o.a=5
% o.c=[]
% 
% oo=fun(o,'a',3,'c',1,'d',2)

function opts = fun(opts,varargin)
for i=1:2:numel(varargin)
    name = varargin{i};
    value= varargin{i+1};
    if isempty(opts.(name))
        opts.(name)=value;
    end
end