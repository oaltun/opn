% function example
%     opt.skipempty = true;
%     opt.def='lj';
%     
%     args=struct('skipempty',false,'abc',3);
%     
%     opt=fun(opt,args)
%     
%     args2 = {'skipempty',false,'abc',1};
%     opt2=fun(opt,args2)
%     opt3 = fun(opt,struct('tkd',4),2)
% end

function r=fun(argStruct,arg2,varargin)
idx=1;
if nargin>2
    idx = varargin{1};
end

r=argStruct;

if isstruct(arg2)
    fnames=fieldnames(arg2);
    for i=1:numel(fnames)
        r(idx).(fnames{i})=arg2.(fnames{i});
    end
elseif iscell(arg2)
    if numel(arg2)==1
        r=overwrite(argStruct,arg2{1});
    else
        for i=1:2:numel(arg2)
            r(idx).(arg2{i})=arg2{i+1};
        end
    end
end

end