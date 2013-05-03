%     """Return an element with lowest fn(seq[i]) score; tie goes to first one.
%     >>> argmin(['one', 'to', 'three'], len)
%     'to'
%     """

function best = argmin(seq,fn)
best = seq(1);
best_score=fn(best);
for i=2:numel(seq)
   x=seq(i=;
   x_score=fn(x);
   if x_score < best_score
       best = x;
       best_score = x_score;
       
   end
end