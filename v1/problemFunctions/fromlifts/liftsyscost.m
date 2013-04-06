
function [costs varargout]=costs6(solutions,upreq,downreq,ncar)
minstd=1;

nsolutions=size(solutions,1);

gettimes=0;
if nargout>1
    gettimes = 1;
end

times=zeros(ncar,nsolutions);

nupreq=numel(upreq);

for isol=1:nsolutions
    solution = solutions(isol,:); %this solution
    %solution = [2 2 3 2 3]; %this solution
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

        times(icar,isol)=liftruntime;
    end %for each car
end %for each solution

%costs= (mean(times)+max(times)-min(times))';
costs= (mean(times)+ 1.5*(max(times)-min(times)))';
%costs= (max(times))';

if gettimes
    varargout{1}=times';
end

end %function


