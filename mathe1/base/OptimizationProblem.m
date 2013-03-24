

classdef OptimizationProblem < handle
    properties
        
        name='?'
        visualiser
        %visualisertitle
        isdraw=false;
        neighborcount = 8; %%% number of neighbors produced in neighbors function
        lb
        ub
        %hasrunner
        
    end
    
    
    methods     
        %%
        %this function is called for configurint the object when a new search/optimization is beginning by a new
        %algorithm.
        function reset(self,varargin)
            self = overwrite(self,varargin);
            
            if self.isdraw
                self.visualiser.title = self.visualisertitle;
                self.visualiser.init;
            end
        end
        
        %%
        %get random positions 
        function pos = randompositions(self,count)
%             pos = cell(count,1); %init cell array
%             %%% get random positions and add to cell array
%             for i = 1:count
%                 pos{i}= self.randomposition;
%             end

            
            %%% get random positions and add to cell array
            for i = 1:count
                pos(i,:)= self.randomposition;
            end
        end
    end
    
    methods(Abstract)
        %%
        % produce a random acceptable position in the search space
        r = randomposition(self)
        %%
        % return list of neighbors
        neighbors = expand(self,position)
        
        %%
        % height, or value , or fitness, or -cost of the position
        val =  height(self, position)
        
    end
end
