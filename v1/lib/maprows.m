% function examples
% clc
% a=[1 2
%     3 4]
% quads=maprows_(@(x) [x x; x x], a)
% end

function mapped=maprows_(fun, matrix)
mapped=[];
for i=1:size(matrix,1)
    mapped = [mapped; fun(matrix(i,:))];
end
end