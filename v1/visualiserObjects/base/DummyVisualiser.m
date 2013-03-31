classdef DummyVisualiser<Visualiser
    properties
        
    end
    
    methods
        %%
        function self = DummyVisualiser(varargin)
            for i=1:2:numel(varargin)
                self.(varargin{i})=varargin{i+1};
            end
        end
        
        %%
        function h = init(self)
            h = [];
        end
        
        %%
        function drawposition(self,position,varargin)
        end
        
        %%
        function drawpath(self,position1,position2,varargin)
        end
        
        %%
        function settitle(self, str)
        end
        
        %%
        function drawbest(self,best)
        end
        
    end
    
end
