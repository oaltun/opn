%pts: probabilistic tabu search. binarý inputs.
function out = pts_lift_binary(request,ncar,niter,whtflglimit)

% clc
% request=[1 1 1 1 1 1 1 1 0 1 1 1 1 0 1 1 1 1 ]; %10 katlý
% ncar=4;                 %number of lift
% niter=50;
% whtflglimit=5;

%% init
fitnessfun='objectfun4';       %object function (fitness function) subroutine name
firstsol_n=20;                 %trial number to find best inital solution
shorttermmemsize = 2*ncar;     % tabu list length
shorttermmemory  = zeros(shorttermmemsize,ncar*length(request));
elitesolutionlist= [];
elitesolutionindx= 0;
elitefrequencytable=zeros(ncar,length(request));
frequencytable=zeros(ncar,length(request));
tabulist=zeros(1,ncar*length(request));
elitelist=zeros(1,ncar*length(request));

%% find out best initial solution
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

shorttermmemory=[shorttermmemory ;bestsolution];
shorttermmemoryindx=1;
elitesolutionlist=[elitesolutionlist ;bestsolution];
frequencytable=addfrequencytable(frequencytable,new,request,ncar);
elitefrequencytable=addfrequencytable(elitefrequencytable,bestsolution,request,ncar);
elitelist=updateelitelist(elitefrequencytable,elitelist,request,ncar);
tabulist=updatetabulistv2(tabulist,frequencytable,elitelist,request,ncar);

%%
cozumlist=[];
whtflgcount=0;
for iterasyon=1:1:niter

    %%%  find  a new neigbourhood (solution)
    [whtflg newsolution]=swapv5(oldsolution,request,ncar,tabulist,shorttermmemory,shorttermmemsize,elitesolutionlist,elitesolutionindx,fitnessfun);
    %yeni solution duzelt.
    newsolution = sanitize_binary(newsolution,ncar,request);
    
    oldsolution=newsolution;
    
    %tamamen rasgele yeni bir cozum gelmiþ
    if whtflg==1
        whtflgcount=whtflgcount+1;
    end
    if whtflgcount>whtflglimit 
        disp('tekrar çýkýþý')
        break
    end
     
    %%% üretilen yeni cozumu short term memorye at.
    shorttermmemoryindx=shorttermmemoryindx+1;
    shorttermmemory(shorttermmemoryindx,:)=newsolution;
    if shorttermmemoryindx==shorttermmemsize
        shorttermmemoryindx=0;
    end

    %%yeni cozumun fitness valuesýný not al
    [fitnesvalue,liftruntime]=feval(fitnessfun,newsolution,ncar);
    
    %%en iyi cozum ise kaydet
    cozumlist(iterasyon)=fitnesvalue;
    if bestfitnesvalue>fitnesvalue
        bestsolution=newsolution;
        bestfitnesvalue=fitnesvalue;
    end
    
    %% ortalmadan iyi bir cozum ise
    if fitnesvalue<=(mean(cozumlist)+min(cozumlist))/2 
        %% elit listeye ekle
        elitesolutionlist=[elitesolutionlist ; newsolution];
        elitesolutionindx=elitesolutionindx+1;
        
        %%frekans tablosunu update et
        elitefrequencytable=addfrequencytable(elitefrequencytable,newsolution,request,ncar);
        
        %%frekans tablosuna bakarak elit listeyi sýfýrdan yeniden oluþtur.
        elitelist=updateelitelist(elitefrequencytable,elitelist,request,ncar);
    end
    
    %% ortalamadan kotu bir cozumse
    if fitnesvalue>(mean(cozumlist)+max(cozumlist))/2
        %kötülerin tabu frekansýný update et.
        frequencytable=addfrequencytable(frequencytable,newsolution,request,ncar);
        % kotulerin frekansýnýdan yararlanarak tabu listi update et.
        tabulist=updatetabulistv2(tabulist,frequencytable,elitelist,request,ncar);
    end
end
out.best_solution=bestsolution;
out.fval=bestfitnesvalue;
end

function tablo=initialsolution(request,ncar)
% binary mantigini kullanmaktadir.
%request: cagri tablosu
%ncar : asansor sayisi
maxcagri=max(size(request)); %request in eleman sayisi max 38 icin düsünüyoruz
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    kromozom1=[];
    oll=request;
    for J=1:1:ncar-1;
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
    table(I,:)=table(I,:)+solution((I-1)*n+1 :1: (I-1)*n+n);
end
end


function elitelist=updateelitelist(elitefrequencytable,elitelist,hallcalllist,totalcarnumber)
%disp('elitelistupdate basladi')
n=length(hallcalllist);
elitelist=elitelist*0;
for I=1:1:n %tum katlar icin
    if sum(elitefrequencytable(:,I))~=0 % o kata gelmis asansor varsa
        mx=max(elitefrequencytable(:,I)); % en fazla asansor ugrama sayisi
        whichcar=find(elitefrequencytable(:,I)==mx); % en fazla ugrayan asansor
        elitelist(1,(whichcar(1)-1)*n+I)=1; %elit listede o kata o asansoru ata
    end

end
%disp('elitelistupdate bitti')
end


function tabulist=updatetabulistv2(tabulist,frequencytable,elitelist,hallcalllist,totalcarnumber)
%disp('Tabuupdate basladi')
n=length(hallcalllist);
%tabulist=tabulist*0;
for I=1:1:n %her bir kat icin
    
    
    %%%tabu listesini updated et: o kat icin kotüler frekans tablosuna bak. en fazla ugrayan arabalar elit
    %%%listesinde de  yok ise tabu listesinde o kata icin konulsun
    if sum(frequencytable(:,I))~=0 %o kata ugrayan varsa
        mx=max(frequencytable(:,I)); %en fazla ugrama sayisi
        whichcar=find(frequencytable(:,I)==mx); %en fazla ugrayan arabalar
        
        if length(whichcar)~=totalcarnumber %tum asasonler esit miktar ugramamis ise
            for J=1:1:length(whichcar) %cok ugrayanlarin her biri icin
                if elitelist(1,(whichcar(J)-1)*n+I)~=1 %elite listte o kata o asansoru atanmamis ise
                    tabulist(1,(whichcar(J)-1)*n+I)=1; %tabu listte o kata o asansoru ata
                end
            end
        end
    end
    
    
    %% tabu listte bu kat icin tüm arabalar yasaklý hale gelmiþ ise tümünü
    %% listeden çýkar.
    count=0;
    for J=1:1:totalcarnumber %her bir araba icin
        if tabulist(1,(J-1)*n+I)==1 %tabu listte bu katta bu araba varsa
            count=count+1; %bu kattaki tabulu araba sayisini bir artir
        end
    end
    if count==totalcarnumber %bu katta tum arabalar tabulu ise
        for J=1:1:totalcarnumber %tum arabalar icin
            tabulist(1,(J-1)*n+I)=0; %tabu listesinde bu katla ilgili tum araba atamalarini kaldirdi
        end
    end
    
    
end
%disp('Tabuupdate bitti')
%check if all car add tabu release them
end


function [whtflg kromozomnew]=swapv5(kromozom,hallcalllist,carnumber,tabulist,shorttermmemory,shorttermmemsize,elitesolutionlist,elitesolutionindx,fitnessfun)
%disp('swap3 basladi')
kromozomnew=[];
hlength=length(hallcalllist);

[a,callindx]=find(hallcalllist==1);
%bestfitness=1e500;
[bestfitness,bestliftruntime]=feval(fitnessfun,kromozom,carnumber);

flag=1;
whtflg=0;
for I=1:1:length(callindx) %her bir kat icin
    whichcall=callindx(I);
    
    for J=1:1:carnumber %her bir asansor icin
        if kromozom((J-1)*hlength+whichcall)==1 % 
            whichcar=J; %her bir cagrý icin hangi asansor atanmýs kaydet
            break
        end
    end

    swpcarlist=[1:1:whichcar-1  whichcar+1:1:carnumber]; %o kata atanabilecek diger arabalarýn listesi
    
    for J=1:1:length(swpcarlist) %diger her bir araba icin
        swapcarnumber=swpcarlist(J);
        tryone=kromozom;
        doswap=1;
        
        %%o kata olan asansörleri degistir
        tryone((whichcar-1)*hlength+whichcall)=0;
        tryone((swapcarnumber-1)*hlength+whichcall)=1;
        
        %tabu listte o katta o asansor varsa swap etme
        if tabulist((swapcarnumber-1)*hlength+whichcall)==1
            doswap=0;
        end

        %short listede ise swap etme
        if doswap==1
            for J=1:1:shorttermmemsize
                if samevector(shorttermmemory(J,:),tryone,hallcalllist,carnumber)==1
                    doswap=0;
                    break
                end
            end
        end
        
        %elit listede ise swap etme
        if doswap==1
            for J=1:1:elitesolutionindx
                if samevector(elitesolutionlist(J,:),tryone,hallcalllist,carnumber)==1
                    doswap=0;
                    break
                end
            end
        end
        
        %yeni fitness daha iyi ise o cozumu dondur.
        if doswap==1
            [fitnesvalue,bestliftruntime]=feval(fitnessfun,tryone,carnumber);
            if fitnesvalue<bestfitness 
                kromozomnew=tryone;
                bestfitness=fitnesvalue;
                flag=0;
            end
        end
        
    end
end

%iyi bir solution bulunmamis ise rasgele bir þey döndür
if flag==1
    kromozomnew=initialsolution(hallcalllist,carnumber);
    whtflg=1; 
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

