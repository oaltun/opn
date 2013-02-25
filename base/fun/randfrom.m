% function example
% 
% for i=1:10
%     a=fun(1:5)
% end

%random element from the array
function r=fun(array)
r=array(randi([1 numel(array)]));