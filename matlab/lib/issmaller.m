%%% returns true if all the fields of count are
%%% smaller than corresponding
%%% fields of maxes
function tf = issmaller(count,maxes)
tf = true;
fn = fields(maxes);
for i=1:numel(fn)
    name = fn{i};
    if count.(name) > maxes.(name)
        tf = false;
        break
    end
end
end %end function