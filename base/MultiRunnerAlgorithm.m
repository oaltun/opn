classdef MultiRunnerAlgorithm<OptimizationAlgorithm
    properties
        algorithm %actual algorithm to be run
        terminationcriteria = 'maxruns'; %maxruns, TODO: time, targetheight
        maxruns = 30;
        maxtime = 10; %in whatever tic/toc unit is.
    end
    properties(SetAccess=private)
        runcnt = 0;
        timecnt=0;
    end
    
    methods
        function self = MultiRunnerAlgorithm(varargin)
            self.npositions = 30;
            
            self = overwrite(self,varargin);
            self.reset;
        end %end function MultiRunnerAlgorithm
        
        
        %%
        function reset(self,varargin)
            %%% update self fields from arguments
            self = overwrite(self,varargin);
            
            %%% do other configuration
            %self.problem.hasrunner = true;
            self.problem.isdraw = self.isdraw;
            self.algorithm.isdraw = self.isdraw;
            self.algorithm.problem = self.problem;
            self.algorithm.hasrunner = true;
            
            if isempty(self.name)
                self.name = ['Multi ' self.algorithm.name ' ' self.terminationcriteria];
            end
            
            self.runcnt =0;
            self.timecnt=0;
            self.isrunner=true;
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
        
        
        %%
        function [position, height, others]=run(self, varargin)
            
            %%% do some state checks.
            self.reset;
            self.checkproperties;
            
            %%% initialize empty output arguments
            height = -Inf;
            position=[];
            
            %%% starting main iteration.
            positionstouse  = self.positions; %input positions given to us
            outputpositions = self.positions; %good positions we will find
            while self.iscontinue %%% let us run the algorithm again.
                tstart = tic; %%restart time counter
                
                %TODO: move this paragraph to a function
                %%% prepare a positions list for the algorithm. normally,
                %%% as any other algorithm, multirunneralgorithm gets a
                %%% self.positions, too. but it may not be enough, since we
                %%% run the guest algorithm multiple times. for that, we
                %%% first exhaust the given self.positions, than produce
                %%% new positions.
                inputpositions = zeros(self.algorithm.npositions, size(self.positions,2));
                for i=1:self.algorithm.npositions
                    if isempty(positionstouse)
                        inputpositions(i,:)=self.problem.randomposition;
                    else
                        inputpositions(i,:)=positionstouse(1,:);
                        positionstouse(1,:)=[]; %we used this one. so delete it.
                    end
                end
                self.algorithm.positions = inputpositions;
                
                
                %%% actually run the guest algorithm!
                [aposition, aheight, ~] = self.algorithm.run;
                
                %%% if the algorithm run returns the best position we know
                %%% so far, do a bit book keeping:
                if height <= aheight
                    
                    %update best height
                    height=aheight;
                    
                    %update best position
                    position=aposition;
                    
                    %overwrite an unlucky position with this guy. 
                    %TODO: do something more clever
                    outputpositions(randi([1 size(outputpositions,1)]), :)=position;
                end
                
                %%% count the times we run the guest algorithm
                self.runcnt = self.runcnt+1;
                
                %%% count the total time used
                self.timecnt = self.timecnt + toc(tstart);
                
            end
            
            
            self.positions = outputpositions;
            self.positions(1,:)=position;
            others.algorithm = self;
            others.runcnt = self.runcnt;
            others.timecnt = self.timecnt;
            others.timeavg = self.timecnt/self.runcnt;
            
            %%% write on figure which one was the best
            if self.isdraw
                self.problem.visualiser.settitle([self.problem.name ' with ' self.name ': ' num2str(height) '(' mat2str(position) ')']);
            end
        end %end function run
        
        
        
        %% run the optimization algorithm one more time or not?
        function tf=iscontinue(self)
            tf=true;
            if self.terminationcriteria == 'maxruns'
                if self.runcnt >= self.maxruns
                    tf=false;
                end
            elseif self.terminationcriteria == 'maxtime'
                if self.timecnt >=self.maxtime
                    tf=false;
                end
            else
                error('no such termination criteria')
            end
        end
    end %methods
end
