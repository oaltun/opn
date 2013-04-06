function usage %#ok<FNDEF>

clc
%%prepare search space and show it
maxxy = 500;
space = getSearchSpace(500,200,0);
hold off
imagesc(space)
colormap gray
hold on


%%prepare initial solutions
ninitialx = 10;
ub = [maxxy, maxxy];
lb = [1,1];
initialx = randsol(lb,ub,ninitialx);
maxstep = round((max(ub)-min(lb))/25);
k=1;
T=1;
nruns=maxstep;
maxnostep=8;


    function cost=costfun(solution)
        cost = space(solution(1), solution(2));
    end

    function T = coolfun(T)
        T=T * 0.99;
    end

    function showfun(o,n,color)
        plot([o(2) n(2)], [o(1) n(1)], 'color', color)
    end

out = fun(@costfun,@randomstep,@coolfun, ...
    @showfun, lb,ub, initialx,...
    maxstep,k,T,nruns,maxnostep);
out.fval
out.best_solution

end

%dot:function:sa(lb,ub,initialx,Tinit,nruns,maxnostep)
function out = fun(costfun,movefun,coolfun,showfun,lb,ub,initialx,...
    maxstep,k,Tinit,nruns,maxnostep)

out=struct;

%dot:for:for run=1 to nruns
%%restart algorithm from a new starting point
ninit = size(initialx,1);
for run=1:nruns
    
    %dot:process:T=Tinit
    %reset Temperature 
    T=Tinit;
    
    %assign new color to this path
    color = 0.3+0.7*rand(1,3);
    color(2)=1;
    
    %dot:process:X=random()
    %%%get the new run point and its energy
    if run<=ninit
        X = initialx(run,:);
    else
        X = randsol(lb,ub,1);
    end
    %dot:process:E=Energy(X)
    E=costfun(X); 
    
    %dot:process:nostep=0
    %%%step around
    nostep=0;
    
    %dot:while:nostep<maxnostep
    while nostep<maxnostep
        
        %dot:process:Xnew=randomNeigbor(X)
        %dot:process:Enew=Energy(Xnew)
        %%%get new neigbor and its energy
        Xnew=movefun(X,maxstep,lb,ub);
        Enew=costfun(Xnew);
        
        %dot:if:Enew <= E or rand<exp(-(Enew-E)/T)
        %dot:process:X=Xnew\lE=Enew\lT=coo()\lnostep=0\l
        %dot:else:nostep=nostep+1
        %dot:end:if
        %%%decide if we should take a a step
        if Enew <= E 
            takestep=true;
            showfun(X,Xnew,color);
        elseif rand<exp(-(Enew-E)/(k*T)) %take the step
            takestep=true;
            showfun(X,Xnew,'red');
        else
            takestep=false;
            showfun(X,Xnew,[.5 .5 .5 ]);
        end
        
        %%%take the step
        if takestep
            X=Xnew;
            E=Enew;
            T=coolfun(T);
            nostep=0;
        else
            nostep=nostep+1;
        end
        %dot:end:while
    end 
    
    %plot last point
    %plot(X(2),X(1),'.','color','yellow');
    
    %dot:process:append X to solutions
    %dot:process:append E to energies
    %%%note the last points for this run of simulated annealing
    solutions{run}=X; %#ok<AGROW>
    energies(run)=E; %#ok<AGROW>
    %dot:end:for
end
%dot:process:Emin=min(energies)\lXmin=X of Emin
[~, idx] = min(energies);
out.fval = energies(idx);
out.best_solution = solutions{idx};
end%dot:end:function
