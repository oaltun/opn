function out = ts_lift_binary(request,ncar,niter)

% request=[[1 1 0 0 1 1 0 1 1 0 1 0 0 0 0 0] [ 0 1 0 0 1 0 0 0 0 1 1 0 0 1 0 1]];
% ncar=3;                %number of lift


%%%
fitnessfun='objectfun4';       %object function (fitness function) subroutine name
firstsol_n=20;                    %trial number to find best inital solution
shorttermmemsize=10*ncar;           % tabu list length
shorttermmemory=zeros(shorttermmemsize,ncar*length(request));
elitesolutionlist=[];
elitesolutionindx=0;
elitefrequencytable=zeros(ncar,length(request));
frequencytable=zeros(ncar,length(request));

elitefitness=[];
tabulist=zeros(1,ncar*length(request));
elitelist=zeros(1,ncar*length(request));

%%% find out best initial solution
bestfitnesvalue=1e200;
for I=1:1:firstsol_n-1
    new=sanitize_binary(initialsolution(request,ncar),ncar,request);
    [fitnesvalue,liftruntime]=feval(fitnessfun,new,ncar);
    if bestfitnesvalue>fitnesvalue
        bestsolution=new;
        bestfitnesvalue=fitnesvalue;
    end
end
oldsolution=bestsolution;
elitefitness=[elitefitness ; bestfitnesvalue];
shorttermmemory=[shorttermmemory ;bestsolution];
shorttermmemoryindx=1;
elitesolutionlist=[elitesolutionlist ;bestsolution];
frequencytable=addfrequencytable(frequencytable,new,request,ncar);
elitefrequencytable=addfrequencytable(elitefrequencytable,bestsolution,request,ncar);
elitelist=updateelitelist(elitefrequencytable,elitelist,request,ncar);
tabulist=updatetabulistv2(tabulist,frequencytable,elitelist,request,ncar);

cozumlist=[];
for I=1:1:niter
    %% find  a neigbourhood
    newsolution=swapv4(oldsolution,request,ncar,tabulist,shorttermmemory,shorttermmemsize,elitesolutionlist,elitesolutionindx);
    newsolution = sanitize_binary(newsolution,ncar,request);
    oldsolution=newsolution;

    % ---- add short term memory
    shorttermmemoryindx=shorttermmemoryindx+1;
    shorttermmemory(shorttermmemoryindx,:)=newsolution;
    if shorttermmemoryindx==shorttermmemsize
        shorttermmemoryindx=0;
    end

    % calculate fitness function
    [fitnesvalue,liftruntime]=feval(fitnessfun,newsolution,ncar);

    cozumlist(I)=fitnesvalue;
    %is it best solution?
    if bestfitnesvalue>fitnesvalue
        bestsolution=newsolution;
        bestfitnesvalue=fitnesvalue;
    end

    %is it good solution?
    if fitnesvalue<=(mean(cozumlist)+min(cozumlist))/2
        elitesolutionlist=[elitesolutionlist ; newsolution];
        elitesolutionindx=elitesolutionindx+1;
        elitefrequencytable=addfrequencytable(elitefrequencytable,newsolution,request,ncar);
        elitelist=updateelitelist(elitefrequencytable,elitelist,request,ncar);
        elitefitness=[elitefitness ; fitnesvalue];

    else
        % frequencytable=addfrequencytable(frequencytable,newsolution,request,ncar);
        %  tabulist=updatetabulistv2(tabulist,frequencytable,elitelist,request,ncar);
    end
    
    if fitnesvalue>1.5*max([(mean(cozumlist)+max(cozumlist))/2 mean(cozumlist)])
        frequencytable=addfrequencytable(frequencytable,newsolution,request,ncar);
        tabulist=updatetabulistv2(tabulist,frequencytable,elitelist,request,ncar);
    end
end
out.best_solution=bestsolution;
out.fval = bestfitnesvalue;
end

function tablo=initialsolution(istek,asansor_n)
% binary mantigini kullanmaktadir.
%istek: cagri tablosu
%asansor_n : asansor sayisi
%
%

maxcagri=max(size(istek)); %istek in eleman sayisi max 38 icin düsünüyoruz
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    kromozom1=[];
    oll=istek;
    for J=1:1:asansor_n-1;
        olasilik=round(rand(1,maxcagri));
        asansoryuk=oll & olasilik;
        oll=oll-asansoryuk;
        kromozom1=[kromozom1 asansoryuk];
    end
    tablo=[kromozom1 oll];
end



function table=addfrequencytable(table,solution,hallcalllist,totalcarnumber)
n=length(hallcalllist);
for I=1:1:totalcarnumber
    table(I,:)=table(I,:)+solution((I-1)*n+1:1:(I-1)*n+n);
end
end


function elitelist=updateelitelist(elitefrequencytable,elitelist,hallcalllist,totalcarnumber)
%disp('elitelistupdate basladi')
n=length(hallcalllist);
elitelist=elitelist*0;
for I=1:1:n
    if sum(elitefrequencytable(:,I))~=0
        mx=max(elitefrequencytable(:,I));
        whichcar=find(elitefrequencytable(:,I)==mx);
        %for J=1:1:length(whichcar)
         %   elitelist(1,(whichcar(J)-1)*n+I)=1;
        %end
        elitelist(1,(whichcar(1)-1)*n+I)=1;
    end

end
%disp('elitelistupdate bitti')
end

function tabulist=updatetabulistv2(tabulist,frequencytable,elitelist,hallcalllist,totalcarnumber)
%disp('Tabuupdate basladi')
n=length(hallcalllist);
%tabulist=tabulist*0;
for I=1:1:n
    if sum(frequencytable(:,I))~=0
        mx=max(frequencytable(:,I));
        whichcar=find(frequencytable(:,I)==mx);
        if length(whichcar)~=totalcarnumber
            for J=1:1:length(whichcar)
                if elitelist(1,(whichcar(J)-1)*n+I)~=1
                    tabulist(1,(whichcar(J)-1)*n+I)=1;
                end
            end
        end
    end
    count=0;
    for J=1:1:totalcarnumber
        
        if tabulist(1,(J-1)*n+I)==1
            count=count+1;
        end
    end
    if count==totalcarnumber
        for J=1:1:totalcarnuber
            tabulist(1,(J-1)*n+I)=0;
        end
    end
end
%disp('Tabuupdate bitti')
%check if all car add tabu release them
end


function kromozom=swapv4(kromozom,hallcalllist,carnumber,tabulist,shorttermmemory,shorttermmemsize,elitesolutionlist,elitesolutionindx)
%disp('swap3 basladi')

hlength=length(hallcalllist);
floornumber=hlength/2;
[a,callindx]=find(hallcalllist==1);

flag=1;
whichcallindx=round((length(callindx)-1)*rand(1))+1;
whichcall=callindx(whichcallindx);   %find which hallcall swap
for I=1:1:carnumber
    if kromozom((I-1)*hlength+whichcall)==1
        whichcar=I;
        break
    end
end
swpcarlist=[1:1:whichcar-1  whichcar+1:1:carnumber];
swapcarnumberindx=round((length(swpcarlist)-1)*rand(1)+1);
swapcarnumber=swpcarlist(swapcarnumberindx);
while flag==1
    doswap=1;
    newkromozom=kromozom;
    newkromozom((whichcar-1)*hlength+whichcall)=0;
        newkromozom((swapcarnumber-1)*hlength+whichcall)=1;

    if tabulist((swapcarnumber-1)*hlength+whichcall)==1
        doswap=0;
    end
    if doswap==1
        for J=1:1:shorttermmemsize
            if samevector(shorttermmemory(J,:),newkromozom,hallcalllist,carnumber)==1
                doswap=0;
                break
            end
        end
    end
    if doswap==1
        for J=1:1:elitesolutionindx
            if samevector(elitesolutionlist(J,:),newkromozom,hallcalllist,carnumber)==1
                doswap=0;
                break
            end
        end
    end
    if doswap==1
        kromozom=newkromozom;
        flag=0;
    else
        if length(swpcarlist)==1
            if length(callindx)==1
                pause(0.1);
                kromozom=initialsolution(hallcalllist,carnumber);
                flag=0;
            else
                
                callindx(whichcallindx)=[];
                whichcallindx=round((length(callindx)-1)*rand(1))+1;
                whichcall=callindx(whichcallindx);   %find which hallcall swap
                for I=1:1:carnumber
                    if kromozom((I-1)*hlength+whichcall)==1
                        whichcar=I;
                        break
                    end
                end
                swpcarlist=[1:1:whichcar-1  whichcar+1:1:carnumber];
                swapcarnumberindx=round((length(swpcarlist)-1)*rand(1)+1);
                swapcarnumber=swpcarlist(swapcarnumberindx);
            end
        else
            swpcarlist(swapcarnumberindx)=[];
            swapcarnumberindx=round((length(swpcarlist)-1)*rand(1)+1);
            swapcarnumber=swpcarlist(swapcarnumberindx);
        end
    end

end

end


function flag=samevector(A,B,hallcalllist,carnumber)
%iki yük vektörünün yük daðýlým dengesinin eþitliðini kontrol eder
% flag==1 ayný daðýlým var
% flag==0 farklý daðýlým var
flag=0;
N=length(hallcalllist);
if sum(abs(A-B))==0
    flag=1;
else
    count=0;
    for I=1:1:carnumber
        for J=1:1:carnumber
            if I~=J
                if sum(abs(A(1,((I-1)*N+1):I*N)-B(1,((J-1)*N+1):J*N)))==0
                    count=count+1;
                    break;
                end
            end
        end
    end
   if count==N
       flag=1;
   end
end
end

