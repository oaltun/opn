%%% REFERENCES:
% [Yang 2010]: X.-S. Yang, S. Deb, Engineering optimization by cuckoo search,
%            Int. J. Mathematical Modelling and Numerical Optimisation,
%            Vol. 1, No. 4, 330-343 (2010).
%            http://arxiv.org/PS_cache/arxiv/pdf/1005/1005.2908v2.pdf
% [Fileexchance]: http://www.mathworks.com/matlabcentral/fileexchange/29809-cuckoo-search-cs-algorithm

%TODO: [Fileexchange]  differ from in that [Yang 2010] a) [Fileexchange]
%code changes the position of all nests in each iteration, as if they are
%all bad nests. pa parameter determines the amount of dimensions that are
%changed. Whereas the pseudocode in [Yang 2010] says pa determines the
%fraction of the bad nests. b) In obtaining a new nest for a bad nest, the
%[Fileexchange] code uses a "biased random walk" where the new nest
%position is obtained using old position, and two random other nest
%positions. Whereas the pseudocode in [Yang 2010] says the new position
%should be determined by levy flights. Here we follow [Fileexchange]
%TODO: when an out of bounds occurs, the maxstep should be revised. (per
%cuckoo? self.maxstep?

%%  function implementing the algorithm
function bestposition   ... bestposition output argument will include the
                        ... best position found after the function returns.
    = CuckooSearch(...
    qualityfun, ... qualityfun is the function the algorithm will maximize.
                ... it should take a single row vector (a position/solution),
                ... and return a single scalar value.
    x,  ... the two dimensional x matrice includes initial positions.
        ... each position is in its own row. each coordinate is in its column.
    lb, ... lower bounds of positions.
    ub, ... upper bounds of positions
    stop,   ... stop is a struct that informs when to stop the main loop. 
            ... it can have the fields "iteration", "time", and "maxheight".
            ... stop.iteration=20 tells to stop at iteration 20. 
            ... stop.time = 2 tells
            ... to stop after 2 seconds. stop.maxheight=.99 tells to stop when ,
            ... maxheight surpasses .99 .
    fixfun, ... fixfun is a function that cures the out of bounds solutions.
            ... note that only solves out of bounds problem. other problems,
            ... like invalid inputs should be solved inside the qualityfun.
            ... look for fixboundXxx functions in the package.
    vis,... vis object is responsible for visualisation. keep empty ([]) if 
        ... you want no visualisation. look for XxxVisualiser classes in 
        ... this package
    opt     ... opt struct includes all other info that the function needs.
            ... especially algorithm specific parameters, etc are put in
            ... this struct. user may chose to pass this empty ([]). so 
            ... prepare necessary defaults in the function
    )

%% algorithm specific options
pa         = getoption(opt, 'pa',         .75); %probability of being discovered by host bird
stepfactor = getoption(opt, 'stepfactor', .01);
beta       = getoption(opt, 'beta',       3/4);

% Levy exponent and coefficient
% For details, see equation (2.21), Page 16 (chapter 2) of the book
% X. S. Yang, Nature-Inspired Metaheuristic Algorithms, 2nd
% Edition, Luniver Press, (2010). [Fileexchange]
defaultsigma= (gamma(1+beta)*sin(pi*beta/2)/(gamma((1+beta)/2)*beta*2^((beta-1)/2)))^(1/beta);
sigma = getoption(opt,'sigma', defaultsigma);

%% start of the algorithm
if not(isempty(vis))
    vis.pathcolor = [rand rand rand]; %line color
end

n = size(x,1); % number of host nests

%%% qualities of initial positions.
f=zeros(n,1); %allocate memory
for i=1:n
    f(i)=qualityfun(x(i,:));
end


%%%TODO: instead of fixed number of iterations, stop the search
%%%when the average or stop distance to the global best
%%%becomes too little. TODO: stop when the points start
%%%to move too little. E.g. their total velocity becomes 1/100
%%%of first iteration?

count.iteration = 0;
tstart = tic;
count.time      = toc(tstart);
count.maxheight = - inf;


[order, bestposition, maxheight] = orderpositions;

%%%iterations
while iscontinue(count, stop) %for each breeding year
    
    for i=order %for each cuckoo, starting from worst one
        %%% cuckoo finds and targets an alternative host nest
        xnew = fly(x(i,:), bestposition); %TODO: we can try to find the best nest after each bird move.
        fnew = qualityfun(xnew);
        
        %if the cuckoo likes the new nest more, she lays egg to
        %this one, abandoning her previus target host nest
        if f(i) <= fnew
            
            if not(isempty(vis)) %do visualisation if necessary
                vis.pathcolor = 'blue';
                vis.drawpath(xnew,x(i,:));
                vis.drawposition(xnew);
            end
            
            %%% move to new nest
            x(i,:)=xnew;
            f(i)=fnew;
        end
    end
    
    %%%% eggs in the worst self.pa percent of nests fail. for
    %%%% those, the cuckoos find new hosts and lay eggs there.
    
    %find how many nests are too bad
    %TODO: this part is currently same as the [Fileexchange]
    %approach. But I think pseudo code in the paper should be
    %different.
    %TODO: keep track of global best in some variable.
    nbad = round(pa *n);
    %nbad=n;
    
    %%%% cuckoo lays egg to somewhere else for each bad nest
    [order, bestposition, maxheight] = orderpositions;
    
    for i=1:nbad
        ni=order(nbad); %index of the bad nest
        xold=x(ni,:); %cache old position for visualisation
        
        %%%% find new nest and lay a new egg.
        %                     %%% use the [Fileexchange] approach.
        %                     K=rand(size(xold))>pa;
        %                     xnew=xold+(rand*x(randi(n),:)-x(randi(n),:)).*K;
        %                     x(ni,:)=self.problem.fixposition(xnew);
        %%% do a levy flight as [Yang 2010] says:
        x(ni,:) = fly(xold, bestposition); %TODO: we can try to find the best nest after each bird move.
        
        %%%% height of new nest
        f(ni)   = qualityfun(x(ni,:));
        
        if not(isempty(vis)) %do visualisation if necessary
            vis.pathcolor ='green';
            vis.drawpath(xold,x(ni,:));
            vis.drawposition(x(ni,:));
        end
    end
    
    %%book keeping
    [order, bestposition, maxheight] = orderpositions;
    count.iteration = count.iteration + 1;
    count.time = toc(tstart);
    count.maxheight = maxheight;
end % main loop



if not(isempty(vis))
    vis.drawbest(bestposition);
end

%% nested function orderpositions:
% order positions according to their heights
    function [order, bestposition, maxheight] = orderpositions
        %%%find the best nest. needed for fly
        [sorted order] = sort(f);
        bestidx = order(end);
        bestposition  = x(bestidx,:);
        maxheight = f(bestidx);
        order = order(:)';
    end

%% nested function fly:
%  when cuckoo flys to a new host nest this function is used to produce new
    function posnew = fly(s, best)
        %%%" This is a simple way of implementing Levy flights
        %%% For standard random walks, use step=1;
        %%% Levy flights by Mantegna's algorithm"[Fileexchange]
        %%% "Here the [self.stepfactor] comes from the fact that L/100
        %%% should the typical step size of walks/flights where L is
        %%% the typical lenghtscale;
        % otherwise, Levy flights may become too aggresive/efficient,
        % which makes new solutions (even) jump out side of the design domain
        % (and thus wasting evaluations)." [Fileexchange]
        u=randn(size(s))*sigma;
        v=randn(size(s));
        step=u./abs(v).^(1/beta);
        posnew = fixfun(lb,ub, s + stepfactor*step.*(s-best).*randn(size(s)));
    end



end