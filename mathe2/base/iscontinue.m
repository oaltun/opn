function tf = iscontinue(count,maxes)
tf = true;
fn = fields(maxes);
for i=1:numel(fn)
    name = fn{i};
    if count.(name) > maxes.(name)
        tf = false;
        break
    end
end