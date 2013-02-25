classdef SupplyChainCost3 < GenericOptimizationProblem
    properties
        %%% capacities
        
        M %marketRequests
        W %warehouseCapacities
        P %plant capacities
        S %supplier capacities
        
        tra %transfer cost related cached information.
        
        WMCX %market warehouse transfer costs max
        PWCX %plant warehouse transfer costs max
        
        %%%% supplier - plant cost calculation related properties
        
        SPCX %maximum supplier plant transfer costs that happen when lead time is min.
        
        minSLt % min lead times
        maxSLt % max lead times
        CStPnt %sum of costs*probability over min lead time to max lead times.cached for fast total cost calculation
        
        SPmu    %for each supplier-plant pair, we will have a random normal distribution for possible lead times. This will be the randomly generated mu, to be used matlabs normpdf.
        SPsigma %for each supplier-plant pair, we will have a random normal distribution for possible lead times. This will be the randomly generated sigma, to be used matlabs normpdf.
        Ploss %loss probabilities. probabilities of material not delivering before max lead time
        %Pn %probability of lead time being min lead time and max lead time
        
        LossCoef %loss coefficients. we assume lostfunction(quantity)=quantity*loss_coefficient
        
        er %exchange rates for the suppliers
        
        Reliability %supplier - plant reliability
        
        %%% plant - warehouse cost calculation related properties
        PlantC %cost of productions for plants
        PlantF %fixed costs of productions for plants
        PlantReliability
        PlantEr %plant exchange rate
        
        
        
        
    end
    
    methods
        %% constructor
        function self = SupplyChainCost3(varargin)
            %%%TODO: construct the super class first.
            %self = self@GenericOptimizationProblem(varargin);
            
            %%% set default values
            self.visualiser = DummyVisualiser;
            self.name = 'SupplyChainCost3';
            
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
            
            
            %%% cache information about echelons. (transfers)
            e=0;
            echelons = struct();
            e=e+1;
            echelons(e).supply=self.S;
            echelons(e).demand=self.P;
            echelons(e).cxrange = [10 120]; %max cost range
            echelons(e).lnrange = [5 15];   %min lead time range
            echelons(e).lxrange = [16 25];  %max lead time range
            echelons(e).rrange  = [.8 .9];  %reliability range
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
            echelons(e).supply=self.W;
            echelons(e).demand=self.M;
            echelons(e).cxrange = [10 120];
            echelons(e).lnrange = [5 15];
            echelons(e).lxrange = [16 25];
            echelons(e).rrange = [.8 .9]; %relaibility range
            echelons(e).errange = [.5 1.5]; %exchange rate range
            
            
            for e=1:numel(echelons) %%for each echelon
                eche = echelons(e);
                
                eche.ns = numel(eche.supply); %number of suppliers
                eche.nd = numel(eche.demand); %number of demanders
                eche.size = [eche.ns eche.nd]; %size of the supply - demand matrix.
                
                %
                
                % WMCX = rand(numel(W),numel(M));%warehouse to market unit costs
                % PWCX = rand(numel(P),numel(W));%plant to warehouse unit costs
                % SPCX = rand(numel(S),numel(P));%supplier to plant unit costs
                %
                %
                %
                %
                %
                %             if isempty(self.WMCX)
                %                 self.WMCX = ones(nW,nM);
                %             end
                %
                %             if isempty(self.PWCX)
                %                 self.PWCX = ones(nP,nW);
                %             end
                %
                %
                %             if isempty(self.SPCX)
                %                 minimum =10;
                %                 maximum = 120;
                %                 %self.SPCX = ones(nS,nP);
                %                 self.SPCX = randi([minimum maximum], [nS,  nP]);
                %             end
                
                eche.CX = randi(eche.cxrange, eche.size);%maximum unit cost that correspond to min lead time
                eche.CN = eche.CX/2; %we assume minimum unit costs are half of maximum unit costs.
                eche.LN = randi(eche.lnrange, eche.size); %minimum lead times
                eche.LX = randi(eche.lxrange, eche.size); %maximum lead times
                
                
                
                %             if isempty(self.minSLt)
                %                 minimum = 5;
                %                 maximum = 15;
                %                 self.minSLt = randi([minimum maximum], [nS,  nP]);
                %             end
                %
                %             if isempty(self.maxSLt)
                %                 minimum = 16;
                %                 maximum = 25;
                %                 self.maxSLt = randi([minimum maximum], [nS, nP]);
                %             end
                %
                %
                %
                % %
                % %
                %             if isempty(self.LossCoef)
                %                 self.LossCoef = rand([nS nP]);
                %             end
                eche.LossCoef = rand(eche.size);
                
                %             %%% supplier dependent material reliability
                %             if isempty(self.Reliability)
                %                 minimum = .80;
                %                 maximum = .98;
                %                 self.Reliability = minimum + (maximum-minimum)*rand(nS, 1);
                %                 self.Reliability = repmat(self.Reliability, 1, nP);
                %             end
                %
                eche.Reliability = randrows(eche.rrange(1),eche.rrange(2),eche.size(1), eche.size(2));
                
                
                
                %             %%% exchange rates for the suppliers (let them be between .5
                %             %%% and 1.5)
                %             if isempty(self.er)
                %                 self.er = .5 + (1.5 - 0.5)*rand(nS,1);
                %                 self.er = repmat(self.er, 1, nP);
                %             end
                %
                eche.er = randrows(eche.errange(1),eche.rrange(2),eche.size(1),eche.size(2));
                
                
                
                %%% prepare SPmu and SPsigma
                for i=1:eche.ns
                    for j=1:eche.nd
                        %                         self.SPmu(i,j) = randi([self.minSLt(i,j) self.maxSLt(i,j)]); %we assume distribution mean is somewhere between min and max lead times
                        %                         diff = self.maxSLt(i,j) - self.minSLt(i,j);
                        %                         self.SPsigma(i,j) = randi([diff 2*diff]);
                        eche.mu(i,j) = randi([eche.LN(i,j) eche.LX(i,j)]); %TODO: discuss with Ali bey
                        diff = eche.LX(i,j)-eche.LN(i,j);
                        eche.sigma(i,j) = randi([diff 2*diff]);
                    end
                end
                
                %%% prepare probability of all scenarios of not being able to
                %%% deliver in time.
                %                 success=[];
                %                 for i=1:nS
                %                     for j=1:nP
                %                         sum=0;
                %                         for t=1:self.maxSLt(i,j)
                %                             sum=sum+normpdf(t, self.SPmu(i,j), self.SPsigma(i,j));
                %                         end
                %                         success(i,j)=sum;
                %                     end
                %                 end
                %                 self.Ploss = 1-success;
                success = zeros(eche.size);
                for i=1:eche.ns
                    for j=1:eche.nd
                        sum=0;
                        for t=1:eche.LX(i,j)
                            sum = sum + normpdf(t, eche.mu(i,j), eche.sigma(i,j));
                        end
                        success(i,j) = sum;
                    end
                end
                eche.Ploss = 1 - success;
                
                
                %
                %             %%% prepare the cost total value when lead time is between
                %             %%% minleadtime and maxleadtime
                %             if isempty(self.CStPnt)
                %                 for i=1:nS %for each supplier
                %                     for j=1:nP %for each plant
                %                         sum=0;
                %                         for t=self.minSLt(i,j):self.maxSLt(i,j) %from minimum valid lead time to maximum valid lead time
                %                             %lead time dependent cost. Maximum lead time
                %                             %maxSLt, minimum lead time minSLt, and maximum cost
                %                             %value SPCX are given to us. We assume minimum
                %                             %cost value SPCN is half of the SPCX. then we assume
                %                             %a line between points (SPCX,minSLt) and
                %                             %(SPCN,maxSLt). the equation below is get using
                %                             %this line equation.
                %                             c=(self.SPCX(i,j) - self.SPCX(i,j)/2)*(self.maxSLt(i,j)- t )/(self.maxSLt(i,j) - self.minSLt(i,j)) + self.minSLt(i,j);
                %                             %lead time dependent probability
                %                             p=normpdf(t, self.SPmu(i,j), self.SPsigma(i,j));
                %                             sum=sum+c*p;
                %                         end
                %                         self.CStPnt(i,j)=sum;
                %                     end
                %                 end
                %             end
                
                %%% prepare the cost total value when lead time is between
                %%% minleadtime and maxleadtime
                
                for i=1:eche.ns %for each supplier
                    for j=1:eche.nd %for each demander
                        sum=0;
                        for t=eche.LN(i,j):eche.LX(i,j) %from minimum valid lead time to maximum valid lead time
                            %lead time dependent cost. we assume
                            %a line between points (CX,LN) and
                            %(CN,LX). the equation below is get using
                            %this line equation.
                            c=(eche.CX(i,j) - eche.CN(i,j))*(eche.LX(i,j)- t )/(eche.LX(i,j) - eche.LN(i,j)) + eche.LN(i,j);
                            %lead time dependent probability
                            p=normpdf(t, eche.mu(i,j), eche.sigma(i,j));
                            sum=sum+c*p;
                        end
                        eche.CStPnt(i,j)=sum;
                    end
                end
                
                
            end %end prepare echelons
            
            
            %%% plant - warehouse specific costs
            %%% plant fixed costs
            %             PlantF = 1000*randi([10 30], nP, 1);
            %             self.PlantF = repmat(PlantF, 1, nW);
            self.PlantF = 1000*randrows(10,30,nP,nW,'int');
            
            %%% plant production costs
            %             PlantC = randi([10 50], nP,1);
            %             self.PlantC = repmat(PlantC, 1, nW);
            %
            self.PlantC = randrows(10,50,nP,nW,'int');
            
            
            
            
            
            %%%% properties necessary for superclass
            
            %%%make sure ubcon ubint lbcon lbint maxstepint maxstepcon are prepared nicely.
            self.ubcon = [];
            self.lbcon = [];
            self.maxstepcon = [];
            
            %%determine integer upper bounds for supply demands
            %%ubint
            myub.WM = sdub(self.W,self.M);
            myub.PW = sdub(self.P,self.W);
            myub.SP = sdub(self.S,self.P);
            self.ubint=self.struct2vec(myub);
            
            %%lbint
            self.lbint=zeros(size(self.ubint));
            
            %%maxstepint
            if isempty(self.maxstepint)
                self.maxstepint = ceil((self.ubint - self.lbint)/self.maxstepdivisor);
            end
            
            
            self.lb = [self.lbcon self.lbint];
            self.ub = [self.ubcon self.ubint];
            
            
            
            
            %%determine supply demand upper bound
            function maxi=sdub(supply,demand)
                dd=repmat(vert(demand)',numel(supply),1); %market demand
                ss=repmat(vert(supply),1,numel(demand)); %supplier supply
                maxi=min(ss,dd); %maximum shipment can not exceed the minimum of ss and dd
            end
            
            
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
            vec = [s.WM(:); s.PW(:); s.SP(:)];
        end
        
        %%
        function s = vec2struct(self,vec)
            s=SupplyChainCostState;
            
            nWM = numel(self.WMCX);
            nPW = numel(self.PWCX);
            nSP = numel(self.SPCX);
            s.WM = reshape(vec(1:nWM),size(self.WMCX));
            s.PW = reshape(vec(nWM+1:nWM+nPW), size(self.PWCX));
            s.SP = reshape(vec(nWM+nPW+1:nWM+nPW+nSP), size(self.SPCX));
        end
        
        %%
        function str = pos2str(self,pos)
            str = mat2str(self.vec2struct(pos));
        end
        
        %%
        % the search algorithms try to MAXIMIZE this function.
        % so height, or value, or fitness, or goodness, or -cost
        function val =  height(self, position)
            
            val  = - self.getcost(position); %%% height is the negative of cost.
        end
        
        %%cost of the supply chain
        function cost = getcost(self,position)
            chain = self.vec2struct(position);
            
            %%% SC: supply - plant echelon costs
            spcostmat = (chain.SP .* self.CStPnt) ./ (self.Reliability.*self.er) ...
                + self.Ploss .* (chain.SP .* self.LossCoef) .* self.er; %equation 4
            SC = sum(sum(spcostmat));
            
            %%% PC: plant-warehouse echolon costs
            pccostmat = (((chain.PW .* self.PlantC) ./ self.PlantReliability) + self.PlantF) .* self.PlantEr; %equation 6
            PC = sum(sum(pccostmat));
            
            
            cost = SC + PC;
        end
        
        
        
        
        %%
        %%% checks whether given position is "bad", e.g. out of bounds,
        %%% violating constraints, etc. and fixes it. It can populate an
        %%% empty position too.
        function [position]=fixposition(self,aposition)
            position = self.vec2struct(aposition);
            
            position.WM = fixdist(position.WM,self.W,self.M);
            warehousedemands = sum(position.WM,2);
            
            position.PW = fixdist(position.PW, self.P, warehousedemands);
            plantdemands = sum(position.PW, 2);
            
            position.SP = fixdist(position.SP, self.S, plantdemands);
            
            position = self.struct2vec(position);
            
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
