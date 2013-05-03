% 
% function test
% seq = [1, 1.2, 2.1, 2.2, 2.3, 1.3];
% fn = @floor;
% nrun = 30000;
% best =[];
% for i=1:nrun
%     best(end+1)=fun(seq,fn);
% end
% sum(best==2.1)
% sum(best==2.2)
% sum(best==2.3)
%     
% end
% 

function best = fun(seq,fn)
best = argmin_random_tie(seq,@(x) -fn(x));
end
