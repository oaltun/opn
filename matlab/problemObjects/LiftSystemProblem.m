function problem = LiftSystemProblem(varargin)
    
    %%% default arguments
    %10 floor building. 18 request possibility.
    self.request = [1 0 1 1 0 1 1 1 0 1 1 1 1 0 1 1 1 0 ];
    self.nlifts  = 3;
    self.logtimes = false;
    
    %%% overwrite by user args
    self = overwrite(self,varargin);
    
    %%% shorter names
    request      = self.request;
    nlifts       = self.nlifts;
    
    %%% prepare arguments to constructor
    floorswr = find(request); %floors with requests:
    
    ub = nlifts* ones(size(floorswr));
    lb = ones(size(floorswr));
    visualiser= DummyVisualiser;
    fixpositionfun = @(a) fixposition2int(a);
    name = strcat('LiftSysProb', ...
        '(nlifts:', num2str(nlifts),...
        ' requests:',mat2str(request),')');
    
    %%% call the constructor
    problem=GenericOptimizationProblem(...
        'lb', lb,...
        'ub', ub,...
        'visualiser', visualiser,...
        'fixpositionfun', fixpositionfun,...
        'name',name);
    
    %%% we assign the heightfun after we
    %%% instantiate
    %%% the constructor, because we want to give
    %%% the problem as a parameter to the
    %%% heightfun.
    
    %%get/set floor information from the request
    nfloors  = (numel(request)+2)/2;
    upreq    = floorswr(floorswr<nfloors);
    downreq  = floorswr(floorswr>=nfloors)-(nfloors-1);
    
    problem.heightfun= @(solution) -liftsyscost(problem,solution,upreq,downreq,nlifts);
    
    %%% assign some preferences in problem.data
    problem.data.logtimes = self.logtimes;
end

