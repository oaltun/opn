classdef OptimizationAlgorithm<handle
    properties
        name='?';
        problem
        isdraw=false;
        hasrunner=false;  %is this algorithm being run by a MultiRunnerAlgorithm instance?
        isrunner = false; %is this algo itself a a MultiRunnerAlgorithm

        positions     %positions (or solutions, or states, or chromozomes) that we start search.
        npositions=1; %natural number of positions this algorithm works with. E.g. hill climbing and simulated annealing has this only 1. PSO may have a default particle count.
    end
    
    methods

        
        %%
        function [position, height, others] = run(self, varargin)
            tstart = tic;
            
            [position height]= self.search(varargin{:});
            others.algorithm = self;
            others.runcnt=1;
            others.timecnt=toc(tstart);
            others.timeavg=others.timecnt;
            
            %update first position in the input positions.
            self.positions(1,:) = position;
        end %function run
        
    end
    

end