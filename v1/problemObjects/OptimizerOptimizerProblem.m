function oop = fun(varargin)
self.problem = [];
self.algorithm = [];
self = overwrite(self, varargin);
algofun = self.algorithm; %do not call the anonymous function

rng('default');
problem = self.problem(); %construct a problem
tmpalgo=algofun();%construct a temporary algorithm to get npositions
positions = rowfun(@(a) randin(problem.lb, problem.ub), vert(1:tmpalgo.npositions));
tic
    function height = heightfun(sol)
        algorithm = algofun(); %construct a new algorithm
        algorithm.problem = problem;
        algorithm.positions = positions;
        algorithm.isdraw = self.isdraw;
        algorithm.stop = self.algorithmStop;
        
        %%% assign parameters
        for i=1:numel(self.parameters)
            algorithm.(self.parameters{i})=sol(i);
        end
        
        %%%run the algorithm
        [position, height, other] = algorithm.run;
%         disp(self.parameters)
%         disp(num2str(sol))
%         disp(num2str(height))
%         toc
    end
%%%

%vis= TwoDFunVisualiser('fun',fun, 'lb', lb, 'ub', ub, 'step',.1);
%vis= TwoDFunSplineVisualiser('fun',fun, 'lb', lb, 'ub', ub, 'step',.1);
oop=GenericOptimizationProblem('heightfun', @heightfun, ...
    'lb', self.lb , 'ub', self.ub,...
    'visualiser', DummyVisualiser,...
    'name',['optimizing ' tmpalgo.name]);

end
