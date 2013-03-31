function r = cellmap(C,fun)
r = cellfun(fun,C,'uniformoutput',false);