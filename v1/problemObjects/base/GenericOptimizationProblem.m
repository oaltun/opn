classdef GenericOptimizationProblem < handle
    %%%user needs to supply all following:
    %%%(instead of supplying heightfun, user can
    %%%subclass this and overwrite height
    %%%function.)
    properties
        heightfun=[];
        lb=[];
        ub=[];
        name='?'
        visualiser=[];
    end
    
    
    properties
        isdraw=false;
    end
    methods
        %%
        %standart constructor. no need to change it. change setdefaults and
        %reset functions.
        function self = GenericOptimizationProblem(varargin)
            self.setdefaults;
            self = overwrite(self,varargin);
        end %end function constructor
        
        %%
        %set default values for class fields.
        function setdefaults(self)
            self.name = 'Generic Optimization Problem';
            %self.visualiser = DummyVisualiser;
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