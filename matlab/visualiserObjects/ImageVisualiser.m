classdef ImageVisualiser<Visualiser
    properties
        image
    end
    
    methods
        %%
        function self = ImageVisualiser(varargin)
            for i=1:2:numel(varargin)
                self.(varargin{i})=varargin{i+1};
            end
        end
        
        %%
        function h = init(self)
            h = figure;
            clf
            hold on
            imagesc(self.image);
            colormap gray
            title(self.title)
            impixelinfo
        end
        
        
    end
    
end
