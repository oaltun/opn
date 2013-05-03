% this function is for easy assigning default values. if the struct opt has the field
% name opt.(name) is returned. otherwise default is returned. 
function option = getoption(opt, name, default)
if isfield(opt,name)
    option = opt.(name);
else
    option = default;
end


    
    


end