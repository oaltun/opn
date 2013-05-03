%%% REFERENCES:
% [Yang 2010]: X.-S. Yang, S. Deb, Engineering optimization by cuckoo search,
%            Int. J. Mathematical Modelling and Numerical Optimisation,
%            Vol. 1, No. 4, 330-343 (2010).
%            http://arxiv.org/PS_cache/arxiv/pdf/1005/1005.2908v2.pdf
% [Fileexchance]: http://www.mathworks.com/matlabcentral/fileexchange/29809-cuckoo-search-cs-algorithm

%TODO: [Fileexchange]  differ from in that [Yang 2010] a) [Fileexchange]
%code changes the position of all nests in each iteration, as if they are
%all bad nests. pa parameter determines the amount of dimensions that are
%changed. Whereas the pseudocode in [Yang 2010] says pa determines the
%fraction of the bad nests. b) In obtaining a new nest for a bad nest, the
%[Fileexchange] code uses a "biased random walk" where the new nest
%position is obtained using old position, and two random other nest
%positions. Whereas the pseudocode in [Yang 2010] says the new position
%should be determined by levy flights. Here we follow [Fileexchange]
%TODO: when an out of bounds occurs, the maxstep should be revised. (per
%cuckoo? self.maxstep?

classdef CuckooSearch < OptimizationAlgorithm
    
    properties
        pa
        beta=3/2;        % value taken from Fileexchange
        stepfactor=0.01; % value taken from Fileexchange
        sigma;
        niter %number of iterations
        fixfun = @fixbound2bound;
    end
    
    methods
        %%
        % constructor.
        function self=CuckooSearch(varargin)
            %%% set default property values
            self.name = 'CS';
            self.npositions = 12;
            self.niter = 30;
            
            self.pa = .75; %probability of being discovered by host bird
            self.stepfactor=.1;
            
            % Levy exponent and coefficient
            % For details, see equation (2.21), Page 16 (chapter 2) of the book
            % X. S. Yang, Nature-Inspired Metaheuristic Algorithms, 2nd
            % Edition, Luniver Press, (2010). [Fileexchange]
            self.sigma= (gamma(1+self.beta)*sin(pi*self.beta/2)/(gamma((1+self.beta)/2)*self.beta*2^((self.beta-1)/2)))^(1/self.beta);
            
            %%% set user property values
            self = overwrite(self,varargin);
            
            %%% other necessary property configuration
            
        end
        
        %%
        % actual algorithm is implemented in this function. change it.
        function [bestpos bestheight] = search(self, varargin)
            
            %%% easier names
            vis = self.problem.visualiser; %visualiser object
            x   = self.positions; %initial positions (of nests)
            
            %%% number of host nests
            n = size(self.positions,1);
            
            %%% heights of initial positions
            f = rowfun(@(row) self.problem.height(row), x);
            
            %%% note best positions
            [m ind]=max(f);
            [bestpos bestheight] = self.bookkeep(x(ind,:), m);
            
            %%%draw initial positions
            if self.isdraw 
                vis.pathcolor ='green';
                for i=1:size(x,1)
                    vis.drawposition(x(i,:));
                end
            end
            
            
            %%%TODO: instead of fixed number of iterations, stop the search
            %%%when the average or maximum distance to the global best
            %%%becomes too little. TODO: stop when the points start
            %%%to move too little. E.g. their total velocity becomes 1/100
            %%%of first iteration?
            
            
            %%% main loop
            while iscontinue(self.count, self.stop)
                %%% a new breeding year!
                
                %%%find the best nest. needed for self.fly
                [~, order]=sort(f);
                best=x(order(end),:);
                order = order(:)';
                
                for i=order %for each cuckoo, starting from worst one
                    %%% cuckoo finds and targets an alternative host nest
                    xnew = self.fly(x(i,:), best); %TODO: we can try to find the best nest after each bird move.
                    fnew = self.problem.height(xnew);
                    
                    %if the cuckoo likes the new nest more, she lays egg to
                    %this one, abandoning her previus target host nest
                    if f(i)<=fnew
                        
                        if self.isdraw %do visualisation if necessary
                            vis.pathcolor = 'green';
                            vis.drawpath(xnew,x(i,:));
                        end
                        
                        %%% move to new nest
                        x(i,:)=xnew;
                        f(i)=fnew;
                        
                        if fnew>bestheight
                            [bestpos bestheight] = self.bookkeep(xnew, fnew);
                        end
                        
                    end
                end
                
                %%%% eggs in the worst self.pa percent of nests fail. for
                %%%% those, the cuckoos find new hosts and lay eggs there.
                nbad = round(self.pa *n);
                
                %%%% cuckoo lays egg to somewhere else for each bad nest
                [~, order]=sort(f);
                best = x(order(end), :); %best is in the bottom
                for i=1:nbad
                    ni=order(nbad); %index of the bad nest
                    xold=x(ni,:); %cache old position for visualisation
                    
                    %%% do a levy flight as [Yang 2010] says:
                    x(ni,:) = self.fly(xold, best); %TODO: we can try to find the best nest after each bird move.
                    f(ni)   = self.problem.height(x(ni,:));
                    
                    if f(ni)>bestheight
                        [bestpos bestheight] = self.bookkeep(x(ni,:), f(ni));
                    end
                    
                    if self.isdraw %do visualisation if necessary
                        vis.pathcolor ='red';
                        vis.drawpath(xold,x(ni,:));
                        %vis.drawposition(x(ni,:));
                    end
                end
                
                
                %%% important: update the
                %%% iteration count after each
                %%% iteration.
                self.iteration=self.iteration+1;
                [bestpos bestheight] = self.bookkeep(bestpos, bestheight);

            end
            
            
            if self.isdraw
                vis.pathcolor='blue';
                vis.drawbest(bestpos);
            end
            
        end
        
        %%
        %cuckoo flys to a new host nest
        %TODO: produce neighbor with Levy Flights. currently just using
        %      self.problem.randomvelocity
        function posnew = fly(self,s, best)
            %%%" This is a simple way of implementing Levy flights
            %%% For standard random walks, use step=1;
            %%% Levy flights by Mantegna's algorithm"[Fileexchange]
            %%% "Here the [self.stepfactor] comes from the fact that L/100
            %%% should the typical step size of walks/flights where L is
            %%% the typical lenghtscale;
            % otherwise, Levy flights may become too aggresive/efficient,
            % which makes new solutions (even) jump out side of the design domain
            % (and thus wasting evaluations)." [Fileexchange]
            u=randn(size(s))*self.sigma;
            v=randn(size(s));
            step=u./abs(v).^(1/self.beta);
            posnew = self.fixfun(self.problem.lb, self.problem.ub, s + self.stepfactor*step.*(s-best).*randn(size(s)));
            
            
        end
        
    end
end
