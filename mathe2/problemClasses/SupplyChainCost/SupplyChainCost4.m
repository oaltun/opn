classdef SupplyChainCost4 < GenericOptimizationProblem
    properties
        %%% capacities
        
        M %marketRequests
        W %warehouseCapacities
        P %plant capacities
        S %supplier capacities
        
        eche %echelon (transfer) related cached information.
        
        %%% plant - warehouse cost calculation related properties
        PlantC %cost of productions for plants
        PlantF %fixed costs of productions for plants
        
    end
    
    methods
        %% constructor
        function self = SupplyChainCost4(varargin)
            %%%TODO: construct the super class first.
            %self = self@GenericOptimizationProblem(varargin);
            
            %%% set default values
            self.visualiser = DummyVisualiser;
            self.name = 'SCC';
            
            %%%% prepare an example state.
            
            %%% supply and demand amounts of each layer.
            self.M=[100 100 200]; %market requests
            self.W=[400 300 500]; %warehouse capacities
            self.P=[150 350]; %plant capacities
            self.S=[300 100]; %supplier capacities
            
            %%% easier names:
            nS = numel(self.S);
            nP = numel(self.P);
            nW = numel(self.W);
            nM = numel(self.M);
            
            self.eche={};
            
            %%% cache information about echelons. (transfers)
            e=0;
            echelons = struct();
            
            
            e=e+1;
            echelons(e).supply=self.W;
            echelons(e).demand=self.M;
            echelons(e).cxrange = [10 120];
            echelons(e).lnrange = [5 15];
            echelons(e).lxrange = [16 25];
            echelons(e).rrange = [.8 .9]; %relaibility range
            echelons(e).errange = [.5 1.5]; %exchange rate range
            
            
            e=e+1;
            echelons(e).supply=self.P;
            echelons(e).demand=self.W;
            echelons(e).cxrange = [10 120];
            echelons(e).lnrange = [5 15];
            echelons(e).lxrange = [16 25];
            echelons(e).rrange = [.8 .9]; %relaibility range
            echelons(e).errange = [.5 1.5]; %exchange rate range
            
            e=e+1;
            echelons(e).supply=self.S;
            echelons(e).demand=self.P;
            echelons(e).cxrange = [10 120]; %max cost range
            echelons(e).lnrange = [5 15];   %min lead time range
            echelons(e).lxrange = [16 25];  %max lead time range
            echelons(e).rrange  = [.8 .9];  %reliability range
            echelons(e).errange = [.5 1.5]; %exchange rate range
            
            
            
            for e=1:numel(echelons) %%for each echelon
                ech = echelons(e);
                
                ech.ns = numel(ech.supply);  %number of suppliers
                ech.nd = numel(ech.demand);  %number of demanders
                ech.size = [ech.ns ech.nd]; %size of the supply - demand matrix.
                
                %
                ech.CX = randi(ech.cxrange, ech.size); %maximum unit cost that correspond to min lead time
                ech.CN = ech.CX/2;                      %we assume minimum unit costs are half of maximum unit costs.
                ech.LN = randi(ech.lnrange, ech.size); %minimum lead times
                ech.LX = randi(ech.lxrange, ech.size); %maximum lead times
                ech.LossCoef = rand(ech.size);
                ech.Reliability = randrows(ech.rrange(1),ech.rrange(2),ech.size(1), ech.size(2)); % supplier dependent material reliability
                ech.er = randrows(ech.errange(1),ech.rrange(2),ech.size(1),ech.size(2)); % exchange rates for the suppliers
                
                %%% mu and sigma for lead time distributions
                for i=1:ech.ns
                    for j=1:ech.nd
                        ech.mu(i,j) = randi([ech.LN(i,j) ech.LX(i,j)]); %TODO: this can be a contribution to the original study?
                        diff = ech.LX(i,j)-ech.LN(i,j);
                        ech.sigma(i,j) = randi([diff 2*diff]);
                    end
                end
                
                %%% prepare probability of all scenarios of not being able to deliver in time.
                success = zeros(ech.size);
                for i=1:ech.ns
                    for j=1:ech.nd
                        sum=0;
                        for t=1:ech.LX(i,j)
                            sum = sum + normpdf(t, ech.mu(i,j), ech.sigma(i,j));
                        end
                        success(i,j) = sum;
                    end
                end
                ech.Ploss = 1 - success;
                
                %%% prepare the cost total value when lead time is between
                %%% minleadtime and maxleadtime
                for i=1:ech.ns %for each supplier
                    for j=1:ech.nd %for each demander
                        sum=0;
                        for t=ech.LN(i,j):ech.LX(i,j) %from minimum valid lead time to maximum valid lead time
                            %lead time dependent cost. we assume
                            %a line between points (CX,LN) and
                            %(CN,LX). the equation below is get using
                            %this line equation.
                            c=(ech.CX(i,j) - ech.CN(i,j))*(ech.LX(i,j)- t )/(ech.LX(i,j) - ech.LN(i,j)) + ech.LN(i,j);
                            %lead time dependent probability
                            p=normpdf(t, ech.mu(i,j), ech.sigma(i,j));
                            sum=sum+c*p;
                        end
                        ech.CStPnt(i,j)=sum;
                    end
                end
                
                
                %write the echelons now.
                self.eche{e}=ech;
                
            end %end prepare echelons
            
            
            %%% plant - warehouse specific costs
            self.PlantF = 1000*randrows(10,30,nP,nW,'int'); % plant fixed costs
            self.PlantC = randrows(10,50,nP,nW,'int');      % plant production costs
            
            
            
            
            
            %%%% properties necessary for superclass. these would be needed
            %%%% in any problem.
            
            %%%make sure ubcon ubint lbcon lbint maxstepint maxstepcon are prepared nicely.
            self.ubcon = [];
            self.lbcon = [];
            self.maxstepcon = [];
            
            %%determine integer upper bounds for supply demands
            %%ubint
            %inner function to determine supply demand upper bound
            function maxi=sdub(supply,demand)
                dd=repmat(vert(demand)',numel(supply),1); %market demand
                ss=repmat(vert(supply),1,numel(demand));  %supplier supply
                maxi=min(ss,dd); %maximum shipment can not exceed the minimum of ss and dd
            end
            myub = SupplyChainCostState;
            myub.dists{1} = sdub(self.W,self.M);
            myub.dists{2} = sdub(self.P,self.W);
            myub.dists{3} = sdub(self.S,self.P);
            self.ubint=self.struct2vec(myub);
            
            %%lbint
            self.lbint=zeros(size(self.ubint));
            
            %%maxstepint
            if isempty(self.maxstepint)
                self.maxstepint = ceil((self.ubint - self.lbint)/self.maxstepdivisor);
            end
            
            
            self.lb = [self.lbcon self.lbint];
            self.ub = [self.ubcon self.ubint];
            
            
            
            
            
            %%% overwrite default values with user supplied values
            self = overwrite(self,varargin);
            
            %%% Let the reset method do argchecking/configuring
            self.reset;
            
            
        end %end function constructor
        
        %%
        %This function re-configures the object. It is called just before
        %calling a problem solution run.
        function reset(self,varargin)
            %%% overwrite default values by NEW user arguments
            self = overwrite(self,varargin);
            
            %call reset method of the super class OptimizationProblem
            reset@GenericOptimizationProblem(self);
        end %end function
        
        
        %%
        %convert struct/object representation to one dimensional vector.
        function vec=struct2vec(self,s)
            %vec = [s.WM(:); s.PW(:); s.SP(:)];
            
            vec = [s.dists{1}(:); s.dists{2}(:); s.dists{3}(:)]';
        end
        
        %%
        function s = vec2struct(self,vec)
            s=SupplyChainCostState;
            
            nS=numel(self.S);
            nP=numel(self.P);
            nW=numel(self.W);
            nM=numel(self.M);
            
            nWM = nW*nM;
            nPW = nP*nW;
            nSP = nS*nP;
            
            s.dists{1} = reshape(vec(1:nWM),[nW nM]);
            s.dists{2} = reshape(vec(nWM+1:nWM+nPW), [nP nW]);
            s.dists{3} = reshape(vec(nWM+nPW+1:nWM+nPW+nSP), [nS nP]);
        end
        
        %%
        function str = pos2str(self,pos)
            str = mat2str(self.vec2struct(pos));
        end
        
        %%
        % the search algorithms try to MAXIMIZE this function.
        % so height, or value, or fitness, or goodness, or -cost
        function val =  height(self, position)
            bounds check yapýp gerekirse hata versin.
            val  = - self.getcost(self.fixposition(position)); %%% height is the negative of cost.
        end
        
        %% cost of the supply chain
        function cost = getcost(self,position)
            cost=0;
            chain = self.vec2struct(position);
  
            %%% echelon (transfer) related supply costs
            for e=1:numel(self.eche)
                costmat=(chain.dists{e} .* self.eche{e}.CStPnt) ./ (self.eche{e}.Reliability .* self.eche{e}.er) ...
                    + self.eche{e}.Ploss .* (chain.dists{e} .* self.eche{e}.LossCoef) .* self.eche{e}.er; %equations 4, 9, and 10
                cost = cost + sum(sum(costmat));!!!!!
            end
            
            %%% Plant production cost (section 3.2.5)
            mat=(((chain.dists{2} .* self.PlantC) ./ self.eche{2}.Reliability) + self.PlantF) .* self.eche{2}.er; %equation 6
            cost = cost + sum(sum(mat));
            
        end
        
        
        
        
        %%
        %%% checks whether given position is "bad", e.g. out of bounds,
        %%% violating constraints, etc. and fixes it. It can populate an
        %%% empty position too.
        function [pos]=fixposition(self,aposition)
            posorg=self.vec2struct(aposition);
            pos = self.vec2struct(aposition);
            
            %             position.WM = fixdist(position.WM,self.W,self.M);
            %             warehousedemands = sum(position.WM,2);
            %             position.PW = fixdist(position.PW, self.P, warehousedemands);
            %             plantdemands = sum(position.PW, 2);
            %             position.SP = fixdist(position.SP, self.S, plantdemands);
            
            
            n=numel(pos.dists);
            demand = self.eche{1}.demand;
            for i=1:n
                pos.dists{i}=fixdist(pos.dists{i}, self.eche{i}.supply, demand);
                if not(i==n) %no need to calculate demand in last level
                    demand = sum(pos.dists{i},2); %demand is recalculated according to previous echelons supply.
                end
            end
            
            pos = self.struct2vec(pos);
            
            %%% fix if dist it is "bad", e.g. out of bounds,
            %%% violating constraints, etc.
            function dist=fixdist(dist,supply,demand)
                
                if sum(supply)<sum(demand)
                    error('supply is less than demand')
                end
                
                %%%--------------------------------------------
                %%% Constraint: shipmentsize: each shipment must be less
                %%% than or equal to capacity of the supplier and demand of the market.
                dd=repmat(vert(demand)',numel(supply),1); %market demand
                ss=repmat(vert(supply),1,numel(demand)); %supplier supply
                maxi=min(ss,dd); %maximum shipment can not exceed the minimum of ss and dd
                
                %%make too big values smaller.
                idx=dist>maxi;
                dist(idx)=maxi(idx)/numel(supply);%TODO: assign random value between zero and maxi
                
                
                %%%-------------------------------------------------
                %%% Constraint: integers: values must be integers.
                %%% round all values
                dist = floor(dist);
                
                %%%--------------------------------------------------
                %%% Constraint: shipments can not be negative
                dist(dist<0)=0;%TODO if possible: random increments should not be produced out of limits at all.
                
                
                
                %%%----------------------------------------
                %%%Constraint:  demand:  sum of all shipments cannot exceed market demand.
                for di=1:numel(demand) %check next demander
                    while true
                        shipped = sum(dist(:,di));
                        if shipped<=demand(di)
                            break
                        end
                        
                        %get a random supplier.
                        si=randi([1 numel(supply)]);%TODO: select the supplier with highest cost and assign zero in the code below.
                        
                        %remove some shipment supply it
                        returnback = randi([0 dist(si,di)]);
                        dist(si,di)=dist(si,di)-returnback;
                    end
                end
                
                %%%-------------------------------------
                %%% Constraint: capacity: shipments from a supplier can not exceed its capacity
                for si=1:numel(supply) %check next supplier
                    while true
                        shipped = sum(dist(si,:));
                        if shipped<=supply(si)
                            break
                        end
                        
                        %get a random market
                        di=randi([1 numel(demand)]);%TODO: look for cost
                        
                        %remove some shipment
                        returnback=randi([0 dist(si,di)]);
                        dist(si,di)=dist(si,di)-returnback;
                    end
                end
                
                
                
                %%%%constraint: all demands are to be shipped exactly.
                %%TODO: find shipment with least cost, and first fill that.
                for di=randperm(numel(demand)) %get next demand
                    while true
                        missing = demand(di)-sum(dist(:,di));
                        if missing == 0
                            break
                        end
                        
                        %get a random supplier
                        si= randi([1 numel(supply)]);%TODO: select mimimum cost supplier
                        capa=supply(si) - sum(dist(si,:)); %get its remaining capacity
                        
                        %set a random shipment
                        shipment = randi([0 min(capa,missing)]);%TODO: take all you can
                        
                        %ship
                        dist(si,di) = dist(si,di)+shipment;
                    end
                end
            end
        end
        
    end%methods
end
