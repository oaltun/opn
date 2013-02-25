%reference:
classdef FireFlyAlgorithm < OptimizationAlgorithm
    
    properties
        gamma
        alpha
        beta0
        niter %number of iterations
    end
    
    methods
        %%
        % constructor.
        function self=FireFlyAlgorithm(varargin)
            %%% set default property values
            self.name = 'FA';
            self.beta0 = 1;
            self.alpha = 0.2;
            self.gamma = 1;
            self.niter = 30;
            self.npositions = 30;
            
            %%% set user property values
            self = overwrite(self,varargin);
            %user may change above values
            % for each object we may use different field values
            %like name island or name island problem
            
            %%% other necessary property configuration
            
        end
        
        %%
        % actual algorithm is implemented in this function. change it.
        function [position height] = search(self, varargin)
            % check property values before we start algorithm
            self.checkproperties;
            
            %%% in this function, change below this line:
            
            
            
            %%number of fireflies in the swarm
            n = numel(self.positions);
            
            %%initial position of fireflies.
            x = self.positions; %copy by value
            
            
            for iter=1:self.niter
                
                %calculate new Intensities
                for i=1:size(x,1) %for each row of positions
                    I(i)=self.problem.height(x(i,:));
                end
                
                %%% rank according to intensity
                [Isorted,rank]=sort(I);
                rank = rank(:)';
                
                %x=x(rank,:);%sort x  %TODO: dont sort x. but just use the rank.
                %I=I(rank); %sort I 
  
                
                for i=rank
                    for j=rank
                        xi=x(i,:);
                        xj=x(j,:);
                        
                        %move fireflies
                        if I(j)>I(i)
                            r=sqrt(sum ((xi-xj).^2));%calculate distance
                            beta=self.beta0*exp(-self.gamma*r^2);
                            
                            x(i,:)=self.problem.fixposition(xi+beta*exp(-self.gamma*r^2).*(xj-xi)+self.alpha*(rand(size(xj))-0.5));
                        end
                       
                        
                    end
                end
                
             
            end
       
          position  = argmax_random_tie(x, @(e) self.problem.height(e));
          height = self.problem.height(position);
       
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
