%fancy 3d visualisation for 2d functions
%todo: make surface semitransparent
%todo: add vertical lines on the surface each 10
%   step
%todo (maybe): re draw everything at the end, with
%   new points calculated.
classdef TwoDFunVisualiser<Visualiser
    properties
        fun %function to visualise
        %x1 %the x range e.g. 0:.001:1
        %x2 %the y range e.g. linspace(0,1,1000)
        lb
        ub
        step
        maxval
    end
    
    properties(SetAccess=private)
        zz
        xx1
        xx2
        h %handle of the figure
    end
    
    methods
        %%
        function self = TwoDFunVisualiser(varargin)
        
        %%% overwrite
        for i=1:2:numel(varargin)
            self.(varargin{i})=varargin{i+1};
        end
        
        %%% argcheck
        if isempty(self.step)
            self.step = (self.ub-self.lb)/100;
        end
        if numel(self.step)<2
            self.step = [self.step self.step];
        end
        
        %%% init
        x1=self.lb(1):self.step(1):self.ub(1);
        x2=self.lb(2):self.step(2):self.ub(2);
        [self.xx1 self.xx2]=ndgrid(x1, x2);
        
        self.zz=arrayfun(@(a1,a2) self.fun([a1 a2]), self.xx1(:), self.xx2(:));
        self.maxval=max(self.zz);
        
        self.zz = reshape(self.zz,size(self.xx1));
        
        
        
        end
        
        %%
        function h = init(self)
        h = figure;
        clf
        hold on
        surf(self.xx1,self.xx2,self.zz,'linestyle','none','FaceColor','interp','FaceLighting', 'phong')
        colormap gray
        title(self.title)
        view(-45,85)
        xlabel('x1')
        ylabel('x2')
        zlabel('height')
        
        end
        
        %%
        function drawposition(self,p)
        f = self.fun(p);
        plot3(p(2), p(1), f, 'o','markersize',3, 'markerfacecolor','blue', 'color','blue','markeredgecolor', 'black');
        if self.isanimate
            pause(self.pauseduration)
        end
        end
        
        %% draw a global best
        function drawbest(self,p)
        f = self.fun(p);
        plot3(p(2), p(1), f, 'o','markersize',10, 'markerfacecolor','red', 'color','red','markeredgecolor', 'black');
        if self.isanimate
            pause(self.pauseduration)
        end
        end
        
        %%
        function drawpath(self,p1,p2,varargin)
        
        args = {'-', 'color', self.pathcolor};
        m=self.maxval;
        f1 = self.fun(p1);
        f2 = self.fun(p2);
        
        %draw line between old and new positions in air
        connectbl([p1 m],[p2 m],args{:});
        
        %draw vertical lines
        connectbl([p1 m],[p1 f1])
        connectbl([p2 m],[p2 f2])
        
        %draw points
        drawposition(self,p1)
        drawposition(self,p2)
        
        if self.isanimate
            pause(self.pauseduration)
        end
        end
        
    end
    
end
