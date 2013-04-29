function cuckoosearchalgoritmproblem = fun(varargin)
self.problem = [];
self = overwrite(self, varargin);
    
rng('default');
algo=CuckooSearch;
positions = rowfun(@(a) randin(self.problem.lb, self.problem.ub), vert(1:algo.npositions));
    function height = heightfun(sol)
        pa=sol(1);
        stepfactor=sol(2);
        beta=sol(3);
        algo = CuckooSearch('pa',pa, 'stepfactor', stepfactor,'beta',beta,'problem', self.problem);
        algo.positions = positions;
        algo.isdraw = self.isdraw;
        algo.stop = self.algorithmStop;
        algo.name = 'cs in';
        [position, height, other] = algo.run;
    end
%%%
%pa 0.75 0-1
%stepfactor 0.1 0-100
%beta 3/2 0 100
lb = [0 0 0];
ub=[1 100 100];
%vis= TwoDFunVisualiser('fun',fun, 'lb', lb, 'ub', ub, 'step',.1);
%vis= TwoDFunSplineVisualiser('fun',fun, 'lb', lb, 'ub', ub, 'step',.1);
cuckoosearchalgoritmproblem=GenericOptimizationProblem('heightfun', @heightfun, ...
    'lb', lb , 'ub', ub,...
    'visualiser', DummyVisualiser,...
    'name','CuckooSearchAlgorithmProblem');

end