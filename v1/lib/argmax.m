%     """Return an element with highest fn(seq[i]) score; tie goes to first one.
%     >>> argmax(['one', 'to', 'three'], len)
%     'three'
%     """
function a= argmax(seq,fn)
a = argmin(seq, @(x) -fn(x));
