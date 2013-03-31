classdef HillClimbing < OptimizationAlgorithm
    properties
        nneighbor = 100;
        maxstepdivisor=100;
    end
    
    methods
        %% constructor
        function self=HillClimbing(varargin)
        %%% set default property values
        
        self.name = 'HC';
        
        %%% set user property values
        self = overwrite(self,varargin);
        
        %%% other necessary property configuration
        
        end %function constructor
        
        
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
        %%
        % hill climbing algorithm implementation
        function [position height]=search(self,varargin)
        %last check of properties before running the algorithm
        self.checkproperties;
        
        maxstep=(self.problem.ub-self.problem.lb)/self.maxstepdivisor;
        
        %get the starting position. if there are more than one
        %positions, we do not care. we just use the first one.
        current = self.positions(1,:);
        while true
            
            %%%get a list of neighbors
            %                neighborsold = self.problem.expand(current);
            
            
            neighbors=rowfun(@(a) current + randin(-maxstep,maxstep), vert(1:self.nneighbor));
            
            
            %check all neighbors, get best neighbor
            neighbor = argmax_random_tie(neighbors, @(x) self.problem.height(x));
            
            if self.problem.height(neighbor)<=self.problem.height(current)
                break
            end
            
            if self.isdraw
                self.problem.visualiser.drawpath(current,neighbor)
                self.problem.visualiser.drawposition(current)
            end
            
            current = neighbor;
            
        end
        
        if self.isdraw
            self.problem.visualiser.drawbest(current)
        end
        
        %%% set output arguments
        position = current;
        height = self.problem.height(position);
        
        end
    end
end
