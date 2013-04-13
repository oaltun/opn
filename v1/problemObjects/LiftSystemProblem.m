function problem = LiftSystemProblem(varargin)
    
    
    
    %10 floor building. 18 request possibility.
    self.request = [1 0 1 1 0 1 1 1 0 1 1 1 1 0 1 1 1 0 ];
    
    
    
    
    self = overwrite(self,varargin);
    
    %%get/set floor information from the request
    nfloors = (numel(request)+2)/2;
    floorswr = find(request); %floors with requests:
    upreq = floorswr(floorswr<nfloors);
    downreq = floorswr(floorswr>=nfloors)-(nfloors-1);
    
    
    
    
    fun= @(a) -rastriginsFunction(a);
    lb = [-5.12 -5.12];
    ub = -lb;
    vis= TwoDFunVisualiser('fun',fun, 'lb', lb, 'ub', ub, 'step',.1);
    problem=GenericOptimizationProblem(...
        'heightfun', fun, ...
        'lb', lb,...
        'ub', ub,...
        'visualiser', vis,...
        'name','NegativeRastrigin');
    
end