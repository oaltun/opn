function main
clc
clf
addpath(genpath('..')) % arrange path so that other classes, etc found.
% rng('default') %reset random number generator to get same results always

%% prepare arguments related to the problem
problem=Island;

qualityfun=@(a) problem.height(a);

lb = problem.lb;

ub = problem.ub;

vis = problem.visualiser;
vis.isdraw = true;
vis.isanimate = true;
vis.title = 'island with cuckoosearch blue:search for better green:expelled';
vis.init;

rng('shuffle')

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
maxval       = qualityfun(bestposition)
end

