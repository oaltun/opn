classdef OptimizationAlgorithm<handle
    properties
        name='?';
        problem
        isdraw=false;
        hasrunner=false;  %is this algorithm being run by a MultiRunnerAlgorithm instance?
        isrunner = false; %is this algo itself a a MultiRunnerAlgorithm

        positions     %positions (or solutions, or states, or chromozomes) that we start search.
        npositions=1; %natural number of positions this algorithm works with. E.g. hill climbing and simulated annealing has this only 1. PSO may have a default particle count.
    
        fixboundsfun = @fixbound2bound; %fixes the out of bounds positions
        selectfun      %function for selecting the parents that will have child. Or for selecting the positions that will be tweaked.
        neg2posfun 
        
        count = struct('iteration', 0,   'time', 0, 'maxheight', -inf);
        stop =  struct('iteration', inf, 'time', 5, 'maxheight',  inf); %TODO: also add minaveragestep
        
        log
        tstart
    end
    
    methods

        
        %%
        function [position, height, others] = run(self, varargin)
            tstartt = tic;
            
            self.count.iteration=0;
            self.count.time=0;
            self.count.maxheight=-inf;
            
            self.tstart = cputime;
            self.log = self.count;
            
            [position height]= self.search(varargin{:});
            
            others.algorithm = self;
            others.runcnt=1;
            others.timecnt=toc(tstartt);
            others.timeavg=others.timecnt;
            
            %update first position in the input positions.
            self.positions(1,:) = position;
        end %function run
        
    end
    

end