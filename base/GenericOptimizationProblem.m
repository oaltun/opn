classdef GenericOptimizationProblem < OptimizationProblem
    
    properties
        heightfun
        maxstepdivisor = 20;
        
        %%% ub and lb of continuous, binary and integer dimensions. They must
        %%% be in the order of continuous, integer, and binary in position arrays.
        ubcon;      %continuous upper bounds
        lbcon;      %continuous lowerbounds
        maxstepcon; %maximum allowable change in continuous dimensions.
        ubint;      %integer upperbounds
        lbint;      %integer lowerbounds
        maxstepint; %maximum allowable change in integer dimensions
    end
    
    methods
        %%
        %standart constructor. no need to change it. change setdefaults and
        %reset functions.
        function self = GenericOptimizationProblem(varargin)
            self.setdefaults;
            self = overwrite(self,varargin);
            self.reset;
        end %end function constructor
        
        %%
        %set default values for class fields.
        function setdefaults(self)
            self.name = 'Generic Optimization Problem';
            self.visualiser = DummyVisualiser;
        end
        %%
        %configure class fields.
        function reset(self,varargin)
            self = overwrite(self,varargin); %overwrite new field values.
            reset@OptimizationProblem(self); %call reset method of the super class OptimizationProblem
            
            if isempty(self.maxstepint)
                self.maxstepint = ceil((self.ubint - self.lbint)/self.maxstepdivisor);
            end
            
            if isempty(self.maxstepcon)
                self.maxstepcon = (self.ubcon - self.lbcon)/self.maxstepdivisor;
            end
            
            self.lb = [self.lbcon self.lbint];
            self.ub = [self.ubcon self.ubint];
        end
        
        %%
        % return a list of neighbors
        function list = expand(self,position)
            
            %list = arrayof(self.neighborcount, @self.randomneighborposition, position);
            for i=self.neighborcount:-1:1
                list(i,:)=self.randomneighborposition(position);
            end
        end
        
        
        %%
        function val =  height(self, position)
            val = self.heightfun(position);
        end
        
        %%
        function nbr=randomneighborposition(self,position)
            v=self.randomvelocity;
            nbr = self.fixposition(position+v);
        end
        
        %%
        %give a random position in search space
        function r = randomposition(self)
            r= self.fixposition([randcontin(self.lbcon,self.ubcon) randintin(self.lbint,self.ubint)]);
        end
        
        %%
        %give a random position change in search space
        function r = randomvelocity(self,varargin)
            r = [randcontin(-self.maxstepcon, self.maxstepcon) randintin(-self.maxstepint, self.maxstepint)];
        end
        
        %%
        %%% you are given a possibly problematic position: Out of bounds, or violating some
        %%% constraints. fix it with the least possible change to it.
        function fixed = fixposition(self,position)
            fixed=position;
            
            ubviolator=position>self.ub;
            fixed(ubviolator)=self.ub(ubviolator);
            
            lbviolator=position<self.lb;
            fixed(lbviolator)=self.lb(lbviolator);
        end
        
        %%
        function str=pos2str(self,pos)
            str=mat2str(pos);
        end
        
    end%methods
end
