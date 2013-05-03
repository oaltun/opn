%ref: Essentials of Metaheuristic by Sean Luke
function height = rastriginsFunction(x)
n = numel(x);

height = 10*n + sum(x.^2 - 10 * cos(2*pi*x));

end