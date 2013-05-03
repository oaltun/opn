
function cost=liftsyscost(problem,solution,upreq,downreq,ncar)
    
    times=zeros(ncar,1);
    
    nupreq=numel(upreq);
    
    solup   = solution(1:nupreq); %assignments for the up requests in this solution
    soldown = solution(nupreq+1:end); %assignments for the down requests in this solution
    for icar=1:ncar
        up_cagri = upreq(solup==icar);
        down_cagri = downreq(soldown==icar);
        if isempty(up_cagri) && isempty(down_cagri)
            liftruntime = 0;
        elseif isempty(up_cagri)
            liftruntime = 3*(max(down_cagri)-1)+3*(length(down_cagri)-1);
        elseif isempty(down_cagri)
            liftruntime = 3*(max(up_cagri)-1)+3*(length(up_cagri)-1);
        else
            liftruntime = ...
                + 3 * (max(up_cagri) - 1)...
                + 3 * abs(max(down_cagri) - max(up_cagri))...
                + 3 * (max(down_cagri) -  min(down_cagri))...
                + 3 * (length(up_cagri) + length(down_cagri)-1);
        end
        
        times(icar,1) = liftruntime;
    end %for each car
    
    %cost= (mean(times) + max(times) - min(times))';
    cost= mean(times) + 1.5*(max(times) - min(times));
    %cost= (max(times))';
    
    if problem.data.logtimes
        problem.data.lifttimes=times;
    end
    
end %function


