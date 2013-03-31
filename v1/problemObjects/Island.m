classdef Island < GenericOptimizationProblem
    
    properties
        island
        maxstep
        maxstepdivisor = 20;
        rowcount
        colcount

    end
    
    properties(SetAccess=private)
        ndims=2;
    end
    
    methods
        function self = Island(varargin)
            %%% default argument values
            
            %%% learn user supplied values
            self = overwrite(self,varargin);
            
            %%%% complete missing values
            if isempty(self.island)
                self.island = getIsland;
            end
            
            [self.rowcount self.colcount] = size(self.island);
            
            if isempty(self.lb)
                self.lb = ones(size(size(self.island)));
            end
            
            if isempty(self.ub)
                self.ub=size(self.island);
            end
            
            if isempty(self.maxstep)
                self.maxstep = ceil(size(self.island)/self.maxstepdivisor);
            end
            
            %             if isempty(self.positions)
            %                 %self.positions = ceil((self.ub + self.lb)/2);
            %                 self.positions = self.randomposition;
            %             end
            
            if isempty(self.visualiser)
                self.visualiser = ImageVisualiser('image',self.island,'title',self.name);
            end
            
        end %end function constructor
        
        

        
        %%
        %
        function val =  height(self, coord)
            coord=self.fixposition(coord);
            %position is the coordinate. so we can directly use it.
            val = self.island(coord(1),coord(2));
        end
        
        
        %%
        function ri = randomposition(self) %get a new random initial position for searching
            %gives random initial starting positions for re runing optimization
            %algorithms from different starting points.
            ri=[];
            for i=1:self.ndims
                ri(end+1)=randi([self.lb(i) self.ub(i)],1, 1);
            end
            
        end
        %%
        %%% you are given a possibly problematic position. Out of bounds, or violating some
        %%% constraints. fix it with the least possible change to it.
        function fixed = fixposition(self,position)
            fixed=round(position);%convert to int.
            
            ubviolator=position>self.ub;
            fixed(ubviolator)=self.ub(ubviolator);
            
            lbviolator=position<self.lb;
            fixed(lbviolator)=self.lb(lbviolator);
        end
        
        %%
        %give a random position change in search space
        function r = randomvelocity(self,varargin)
            r = randintin(-self.maxstep, self.maxstep);
        end
        
        %%
        function str=pos2str(self,pos)
            str = mat2str(pos);
        end
    end%methods
end
