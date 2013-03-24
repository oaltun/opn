% % this function returns an array with random elements between the elements of lb and ub.
% % example usage:
% function example
% for i=1:10
%     fun([2 3], [3 4])
% end
% end

function r = fun(lb,ub)
r = (ub-lb).*rand(size(lb)) + lb;
end