%reference:J. KWIECIE? and B. FILIPOWICZ
%AGH University of Science and Technology, Department of Automatics, 30 Mickiewicza Ave., 30-059 Krakow, Poland
classdef FireFlyAlgorithm < OptimizationAlgorithm
    
    properties
        gamma
        alpha
        beta0
        niter %number of iterations
        neg2pos
        fixfun

    end
    
    methods
        %%
        % constructor.
        function self=FireFlyAlgorithm(varargin)
            %%% set default property values
            self.name = 'FA';
           % self.beta0 =1000; %beta0=1(attractiveness coefficient) in original algorithm which depends on search area,
            ...10000 is taken to increase attractiveness in our search area.
                self.alpha =0.001;  % alpha(random motion coefficient) between 0-1,
            ...0.001 is taken to decrease rand walk
                self.gamma = 0.5;   % gamma(light absorption coefficient) between 0,1-10,
            ...0.1 is taken to decrease light absorption,to increase attractiveness
                self.niter = 2;%after 2nd iteration takes much time.
            self.npositions =10;%solutions, after 20 takes much time.
            %initial reserved positions of fireflies
            self.neg2pos=@neg2posbymin;
            
            %%% set user property values
            self = overwrite(self,varargin);
            %user may change above values
            % for each object we may use different field values
            %like name island or name island problem
            
            %%% other necessary property configuration
            self.fixfun=@fixbound2bound;
            
        end
        
        %%
        % actual algorithm is implemented in this function. change it.
        function [position height] = search(self, varargin)
            %%number of fireflies in the swarm
            n = size(self.positions,1);%1 is rows
            pathcolors=rand(n,3);
            %%initial position of fireflies.
            x = self.positions; %copy by value(2 dimension like x and y)
            %npositions...preferred number of positions by firefly object
            %positions...actual firefly positions which is given by user(testall)
            %position ...the best position this algorithm finds at the end
            %height ... the best height/quality/fitness we get after
            %running algorithm,it is the height of position.
            %   h=0;

            for iter=1:self.niter
                
                %calculate new Intensities
                
                for i=1:size(x,1) %for each row of positions
                    
                    I(i)=self.problem.height(x(i,:));%i.row s height is i.intensity.
                    
                end
                I=self.neg2pos(I);%Convert initial I s from negative to pozitive.
                %%% rank according to intensity
                [Isorted,rank]=sort(I);
                rank = rank(:)';
                xi=x(i,:);
                %x=x(rank,:);%sort x  %TODO: dont sort x. but just use the rank.
                %I=I(rank); %sort I
                %    stp=zeros(size(n));
                for j=rank
                    for i=rank
                        xi=x(i,:);
                        xj=x(j,:);
                        %move fireflies
                        if I(j)>I(i)
                            r=sqrt(sum ((xi-xj).^2));%calculate distance
                            % I=self.beta0*exp(-self.gamma*r^2);%attractiveness
                            %self.beta0 can be taken as initial I which
                            ...comes from objective function.But make sure for positive initial Is.
                            attpar1=-self.gamma*(r^2);
                            attpar2=exp(attpar1);
                            %calculate attractiveness parameters
                            betar=I(j)*attpar2;%attractiveness
                            betamot=betar*attpar2.*(xj-xi);%motion depended attractiveness
                            randmot=self.alpha*(rand(size(xj))-0.5);%random motion depended alpha
                            %calculate motion parameters
                            step=betamot+randmot;
                            %step=beta*exp(-self.gamma*r^2).*(xj-xi)+self.alpha*(rand(size(xj))-0.5);
                            xold=x(i,:);
                            xcont=xi+step;
                            xnew=self.fixfun(self.problem.lb,self.problem.ub,xcont);
                            %                             while  isequal (xnew,xold)
                            %                                 step=step*100;
                            %                                 xcont=xold+step;
                            %                                 xnew=self.problem.fixposition(xcont);
                            %
                            %                             end
                            x(i,:)=xnew;
                            if self.isdraw
                                self.problem.visualiser.pathcolor = pathcolors(i,:);
                                self.problem.visualiser.drawposition(x(i,:));
                                self.problem.visualiser.drawpath(xold,x(i,:));
                                %                               if not(h==0)
                                %                                clear h;
                                %                               end
                                %                                %h=self.problem.visualiser.drawposition(x(i,:));
                                %                                 h= self.problem.visualiser.drawpath(xold,x(i,:));
                                %                            end
                            end
                            
                        end
                        
                    end
                end
                
            end
            position  = argmax_random_tie(x, @(e) self.problem.height(e));
            height = self.problem.height(position);
            self.problem.visualiser.drawbest(position);
            
            %to forward all other fireflies to the best point
            %             for i=1:n
            %                 xi=x(i,:);
            %                 r=sqrt(sum ((xi-position).^2));%calculate distance
            %                 x(i,:)=self.problem.fixposition(xi+beta*exp(-self.gamma*r^2).*(position-xi)+self.alpha*(rand(size(position))-0.5));
            %             end
            %             for i=1:n
            %                 self.problem.visualiser.pathcolor =pathcolors(i,:);
            %                 self.problem.visualiser.drawpath(position,x(i,:));
            %                 self.problem.visualiser.drawposition(position);
            %             end
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
