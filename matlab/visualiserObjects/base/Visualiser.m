classdef Visualiser<handle
    properties
       title 
       isdraw=false;
       isanimate=false;
       pauseduration= 0.001;
       pathcolor='blue'
    end
    methods
        %%
        function drawposition(self,position)
            plot(position(2),position(1),'color','green');
            if self.isanimate
                pause(self.pauseduration)
            end
        end
        
        %% draw a global best
        function drawbest(self,position)
            plot(position(2), position(1), 'o','markersize',10, 'markerfacecolor','red', 'color','red','markeredgecolor', 'black');
            if self.isanimate
                pause(self.pauseduration)
            end
        end
        
        %%
        function drawpath(self,position1,position2,varargin)
            plot([position1(2) position2(2)], [position1(1) position2(1)],'-', 'color', self.pathcolor);
            if self.isanimate
                pause(self.pauseduration)
            end
        end
        
        %%
        function init(self)
            
            clf
            hold on
            colormap gray
            title(self.title)
        end
        
        %%
        function settitle(self,str)
            self.title = str;
            title(str);
        end
        
    end
    
end