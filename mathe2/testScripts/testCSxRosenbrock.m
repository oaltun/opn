function main
clc

addpath(genpath('..')) % arrange path so that other classes, etc found.
% rng('default') %reset random number generator to get same results always

%% prepare arguments related to the problem

qualityfun=@(a) -rosenbrockFunction(a); %rosenbrock is minimization problem. we convert to maximization by multiplyin by -1.

expected = [1 1];

lb = [-2.048,-2.048];

ub = [2.048,2.048];

vis = [];


% prepare initial points
nx=10;
x0=[];
for i=1:nx
    x0(end+1,:) = randombetween(lb,ub);
end

fixfun = @fixbound2bound;

stop.iteration = 20;


%% maximize the qualityfun function
bestposition = cuckooSearch(qualityfun, x0, lb, ub, stop, fixfun, vis, [])
bestval      = rosenbrockFunction(bestposition)
end

