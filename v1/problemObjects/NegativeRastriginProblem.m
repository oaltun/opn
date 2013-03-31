function problem = NegativeRastriginProblem
fun= @(a) -rastriginsFunction(a);
lb = [-5.12 -5.12];
ub = -lb;
vis= TwoDFunVisualiser('fun',fun, 'lb', lb, 'ub', ub, 'step',.1);
problem=GenericOptimizationProblem('heightfun', fun, ...
    'lb', lb , 'ub', ub,...
    'visualiser', vis,...
    'name','NegativeRastrigin');

end