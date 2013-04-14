function main
clc %clear command line
close all %close all figures
disp('start')
%% add the directories for the classes and functions used to the matlab search path
addpath(genpath('..'))
%% options is collected in the struct called self
self.isdraw = false; %should the paths and other visualisations be drawn
self.isanimate = false; %should the drawing be slow, like an animation?

self.time = 25;

%% initialization
rng('default') %reset random number generator. We want to get the same result on each run.

%% prepare list of problems
problemlist = {};

% problemlist{end+1} = Island('name','Island');
% problemlist{end+1} = SupplyChainCost4;
% problemlist{end+1} = NegativeRastriginProblem;
 problemlist{end+1} = LiftSystemProblem;
 
%% prepare list of algorithms
algorithmlist = {};

% algorithmlist{end+1} = SerialHillClimbing('nneighbor', 10, 'npositions', 3);
% 
% algorithmlist{end+1} = HillClimbing('nneighbor', 20);
% 
algorithmlist{end+1} = CuckooSearch;
% 
% algorithmlist{end+1} = ParticleSwarmOptimization('niter',3);
%  
% %algorithmlist{end+1} = FireFlyAlgorithm;
% 
% algorithmlist{end+1} = MultiRunnerAlgorithm(...
%     'algorithm',HillClimbing,...
%     'name','multiHcMaxrun', ...
%     'maxruns',100);
% 
% algorithmlist{end+1} = MultiRunnerAlgorithm(...
%     'algorithm',HillClimbing,...
%     'name','multiHcMaxtime',...
%     'terminationcriteria','maxtime',...
%     'maxtime',5 ...
%     );
% 
% algorithmlist{end+1} = MultiRunnerAlgorithm(...
%     'algorithm', ParticleSwarmOptimization('niter',10), ...
%     'name', 'MultiPSO',...
%     'terminationcriteria', 'maxruns',...
%     'maxruns', 2);

%% run algorithmlist on problemlist
result = struct([]); %for holding results of algorithm runs.
resultOther = struct([]);%#ok<NASGU> %for other stuff algorithmlist return
r=0; %result idx
for p=1:numel(problemlist)
    problem = problemlist{p}; %for each problem
    for a=1:numel(algorithmlist)
        algorithm = algorithmlist{a}; %for each algorithm
        graphtitle=[problem.name ' with ' algorithm.name];
        disp(graphtitle)
        
        %%prepare the visualiser
        if self.isdraw
%             problem.isdraw = self.isdraw;
            problem.visualiser.title = graphtitle;
            problem.visualiser.init;
            problem.visualiser.isanimate = self.isanimate;
        end
        
        %prepare algorithm. set initial starting
        %"positions". 
        algorithm.isdraw = self.isdraw;
        algorithm.problem = problem;
        
        algorithm.positions = rowfun(@(a) randin(problem.lb, problem.ub), vert(1:algorithm.npositions));
        algorithm.stop.time = self.time;
        %%% run the algorithm on the problem. the
        %%% algorithm.run calls 
        %%% algorithm.search
        %position: best position found
        %height: maximum height
        %other: any other stuff that the algorithm
        %wants to return. 
        [position, height, other] = algorithm.run; %run f
        
        
        
        %%note results to a struct array
        r=r+1;
        result(r).algorithm = algorithm.name;
        result(r).problem = problem.name;
        result(r).height = height;
        result(r).position = problem.pos2str(...
            problem.fixposition(position));
        result(r).runcnt=other.runcnt;
        result(r).timecnt=other.timecnt;
        result(r).timeavg=other.timeavg;
        result(r).algolog = algorithm.log;
        result(r).graphtitle=graphtitle;
        
        %%uncomment if other stuff is needed.
        %resultOther(r).other = other;
    end
end


%% draw height-time grapth
figure
hold on
legends={};

%%% prepare some styles to use
ls = {'-','--', ':', '-.'}';
lw = {2,3,4,5}';
[lsi,lwi]=ndgrid(1:numel(ls),1:numel(lw));
%markers = {'+','o','*','.','x','s','d','^','v','>','<','p','h'}';

%styles=styles(randperm(numel(styles)));

for r=1:numel(result)
    log = result(r).algolog;
    
    times=[log.time];
    iterations=[log.iteration];
    heights=[log.maxheight];
    
    
    hplot = plot(times,heights,'linestyle',ls{lsi(r)},'linewidth',lw{lwi(r)});
    
    legends{r,1} = result(r).graphtitle;
    %TODO: make the graph better.
end
xlabel('time')
ylabel('height')
legend(legends)

%% save and review results

result = nestedSortStruct(result,{'problem'},-1);  %sort struct as you wish
datacell = structToCellArrayWithHeaders(result); %convert struct to a cellarray with headers

% %%open results in excel. Remember: close excel file each time.
% cell2csv('results.csv', datacell, ';', '.',true)
% !start results.csv

%%open results in html file
cell2html(datacell,'results.html');
!start results.html

disp('end')
end
