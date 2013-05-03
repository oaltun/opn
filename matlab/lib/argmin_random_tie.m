% % """Return an element with lowest fn(seq{i}) score; break ties at random.
% % Thus, for all s,f: argmin_random_tie(s, f) in argmin_list(s, f)"""
% %

% function test
% seq = {5, 4, 2.1, 2.2, 2.3, 3};
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

function best = fun(seq, fn)
    best = seq(1,:);
    best_score = fn(best);
    n=1;
    for i=2:size(seq,1)
        x=seq(i,:);
        x_score = fn(x);
        if x_score < best_score
            best = x;
            best_score = x_score;
            n=1;
        elseif x_score == best_score
            n = n + 1;
            if randi(n,1) == 1
                best=x;
            end
        end
    end
end
