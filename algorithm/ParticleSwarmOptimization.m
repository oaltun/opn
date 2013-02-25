%ref: wikipedia.com/Particle_swarm_optimization
classdef ParticleSwarmOptimization < OptimizationAlgorithm
    
    properties
        w
        psip
        psig
        niter %number of iterations
    end
    
    methods
        %%
        % constructor.
        function self=ParticleSwarmOptimization(varargin)
            %%% set default property values
            self.name = 'PSO';
            self.w = 0.34;
            self.psip = 0.33;
            self.psig = 0.33;
            self.niter = 30;
            self.npositions = 30;
            
            %%% set user property values
            self = overwrite(self,varargin);
            
            %%% other necessary property configuration
            
        end
                
        %%
        % actual algorithm is implemented in this function. change it.
        function [position height] = search(self, varargin)
            % check property values before we start algorithm
            self.checkproperties;
            
            %%% in this function, change below this line:
            if self.isdraw
                %line color
                self.problem.visualiser.pathcolor = [rand rand rand];
            end
            
            %%number of particles in the swarm
            S = size(self.positions,1);
            
            %%the name x was used in the reference article. so we use that too.
            x = self.positions;
            
            %%initial velocities of the particles
            v=zeros(size(x)); %allocate memory
            for i=1:S;
                v(i,:)=self.problem.randomvelocity;
            end
            
            %%best known position of each particle. at the beginning just
            %%the place they are.
            p = x;
            
            %%heights of best positions. apply self.problem.height function
            %%to each element of p, and return all results in a cell array
            fp=zeros(S,1); %allocate memory
            for i=1:S
                fp(i)=self.problem.height(p(i,:));
            end
            
            
            %%global best position
            g  = argmax_random_tie(x, @(pos) self.problem.height(pos)); %TODO: no need to call self.problem.height on each again. just use fp.
            
            %%height of the global best
            fg = self.problem.height(g);
            
            %%%TODO: instead of fixed number of iterations, stop the search
            %%%when the average or maximum distance to the global best
            %%%becomes too little. ALTERNATIVE: stop when the points start
            %%%to move too little. E.g. their total velocity becomes 1/100
            %%%of first iteration?
           
            %%%iterations
            for iter=1:self.niter
                %%%for each particle
                for i=1:S
                    xi = x(i,:);
                    vi = v(i,:);
                    pi = p(i,:);
                    
                    %%update the particle velocity
                    dpx = pi-xi;
                    dpg = g -xi;
                    
                    %produce a new velocity
                    rp = rand(size(xi));
                    rg = rand(size(xi));
                    vnew = vi*self.w  +  dpx .* rp * self.psip  +  dpg.*rg * self.psig;
                    
                    %%set the new position
                    x(i,:) = self.problem.fixposition(xi +vnew);
                    
                    %%visualise the path the particle is moving
                    if self.isdraw
                        %%% draw a path between the old and new position of
                        %%% the particle
                        self.problem.visualiser.drawpath(xi, x(i,:));
                        
                        %%% draw a point on new position
                        self.problem.visualiser.drawposition(x(i,:)); 
                    end
                    
                    %%correct velocity
                    v(i,:)=x(i,:) - xi;
                    
                    fxi = self.problem.height(x(i,:));
                    if fxi>fp(i)
                        %update the particles best known position
                        p(i,:)  = x(i,:);
                        fp(i) = fxi;
                        
                        if fp(i) > fg
                            %update the swarms best known position
                            g  = p(i,:);
                            fg = fp(i);
                        end
                    end
                    
                end
            end
            
            if self.isdraw
                self.problem.visualiser.drawbest(g);
            end
            
            height=fg;
            position = g;
        end
        
        %%
        % change this function if needed. It is called from the search
        % function, and gives error if there are missing properties, or if
        % there are any other problems.
        function checkproperties(self)
            dbstop if error
            if isempty(self.positions)
                error('self.position is empty');
            end
            if isempty(self.problem)
                error('self.problem is empty');
            end
        end
    end
end
