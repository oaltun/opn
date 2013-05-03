% function examples
% clc
% a= [1 2
%     3 4]
% quads=rowfun_(@(x) [ rand(size(x)); x x], a)
% end

function mapped=rowfun_(fun, matrix)
mapped=[];
for i=1:size(matrix,1)
    mapped = [mapped; fun(matrix(i,:))];
end
end