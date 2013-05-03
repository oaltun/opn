function r = matmap(C,fun)
r = cellfun(fun,C,'uniformoutput',true);
