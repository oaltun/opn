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
        
        count = struct('time', 0, 'bestheight', -inf,'iteration', 0  );
        stop  = struct('time', 5, 'bestheight',  inf,'iteration', inf); %TODO: also add minaveragestep
        
        log
        tstart = cputime;
        iteration = 0;
        bestheight=-inf;
        
        debug=false
    end
    
    methods
        
        
        %%
        function [position, height, others] = run(self, varargin)
            tstartt = tic;
            
            %%% call the search function
            [position height]= self.search(varargin{:});
            
            %%% book keeping
            others.algorithm = self;
            others.runcnt=1;
            others.timecnt=toc(tstartt);
            others.timeavg=others.timecnt;
            
            %update first position in the input positions.
            self.positions(1,:) = position;
        end %function run
        
        %%
        function [bestpos bestheight] = bookkeep(self,bestpos,bestheight)
            if bestheight>=self.bestheight
                self.bestheight=bestheight;

                %%%update count
                self.count.time = cputime-self.tstart;
                self.count.iteration=self.iteration;
                self.count.bestheight=bestheight;
                self.count.bestpos = bestpos;
                
                %%%append it to log.count list
                if isfield(self.log,'count')
                    self.log.count(end+1)=self.count;
                else
                    self.log.count=self.count;
                end
            end
            
            if self.debug
                disp('best:')
                self.count
            end
            
        end
    end
    
    
end
