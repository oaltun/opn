function out = ga_lift_binary(...
    ...
    number_of_starting_solutions, ...
    maximum_number_of_iterations, ...
    uygunf, ...
    caprazlama_yontemi, ....
    kat_sayisi, ....
    asansor_sayisi, ....
    yolcu_istekleri...
    )

%ilk nufusun (cozumun / baslangic noktalarinin) olusturulmasi.
solutions = get_initial_solutions(yolcu_istekleri, number_of_starting_solutions, asansor_sayisi);

% Baslangic nufusunun  uygunluk degeri.
[finit, liftruntime] = feval(uygunf, solutions, asansor_sayisi); %Uygunluk hesabi yapiliyor.

%Baslangic nufusundaki min uygunluk degerine sahip birey.
[best_error, baslangic_min] = min(finit);
best_solution = solutions(baslangic_min, :);

iteration = 0;
while(iteration<= maximum_number_of_iterations) %& (max(finit)>= opt_kriter)

    %secim: rulet tekerlegi ile gerceklestiriliyor.
    secnufus = ruletselection(solutions, finit, number_of_starting_solutions);
    
    %caprazlama: iteration boyunca gerceklestirilecek caprazlama_yontemi ile belirleniyor.
    switch caprazlama_yontemi 
        case 1, solutions = singlepointX(secnufus, 1);
        case 2, solutions = twopointX(secnufus, 1);
            %caprazlama_yontemi orani 1 ise tum nufus caprazlamaya dahil ediliyor. 0-1 arasinda degisebilir.
        case 3, solutions = uniformX(secnufus, 1);
    end

    %mutasyon
    for i = 1:number_of_starting_solutions
        solutions(i, :) = mutation_v1(solutions(i, :), yolcu_istekleri, asansor_sayisi, kat_sayisi);
    end

    %bir onceki nufustaki uygunluk degeri en buyuk bireyi yeni olusturdugumuz
    %nufusta sakliyoruz. Bu islemden sonra YENI NUFUS olusturulmus oluyor.
    %secim, caprazlama_yontemi, mutasyon ve eniyibireyin saklanmasindan 
    %sonra elde edilen nufus(solutions) YENI NUFUS'tur.
    solutions(number_of_starting_solutions, :) = best_solution;
    
    %finit: genetik islemcilerden sonra elde edilen yeni nufusun
    %uygunluk degerleri.
    [finit, liftruntime] = feval(uygunf, solutions, asansor_sayisi);

    iteration = iteration+1;
end
[minfval idx]=min(finit);

out.best_solution=solutions(idx,:);
out.fval = minfval;
end



% yeni nufusu olusturacak bireylerin secimi yapiliyor.
% uygunluklarina gore rulet tekerlegi yontemi kullanilarak gecerli
% olan nufus icerisinden secim yapiliyor.
% parname gecerli nufustan hangi bireylerin secilecegini gosterir,
% secnufus gecerli nufustan uygunluklarina gore secilmis bireylerden olusan nufusu gosterir.
function secnufus = ruletselection(nufus, uygunluk, krs)
uygunluk = uygunluk';

tpuyg = sum(1./uygunluk); % toplam uygunluk

for cr = 1:krs
    sval(cr) = sum(1./uygunluk(1, 1:cr));
end
sval;
parname = [];
for t = 1:krs
    rval = (tpuyg*rand); % toplam uygunlukla rasgele bir katsayinin carpilmasiyla elde edilen bir deg.
    if rval<sval(1)
        parname = [parname 1];
    else
        for tt = 1:krs-1
            sl = sval(tt);
            su = sval(tt)+1./uygunluk(tt+1);
            if (rval>= sl) & (rval<= su) %rval degeri hangi aralikta o tespit ediliyor.
                parname = [parname tt+1]; %if kosulu saglandiysa parname, kosulu saglayan kacinci bireyse o degeri aliyor.
            end % if
        end % for tt
    end % if
end % for
parname; % parname ilk nufustan hangi bireyin secilecegini gosteren degisken.

[ps sp] = size(parname);

secnufus(1:sp, :) = nufus(parname, :); %yeninufus, ilk nufustan parnamedeki degerlere gore secilerek alinir.

end


% binary mantigini kullanmaktadir.
%yolcu_istekleri: cagri tablosu
% adet : kac adet solutions isteniyor
%asansor_n : asansor sayisi
function tablo = get_initial_solutions(yolcu_istekleri, adet, asansor_n)

cagri_index = find(yolcu_istekleri == 1); %yolcu_istekleri icindeki 1 lerin yerini bulur.
cagrisayisi = max(size(cagri_index)); % yolcu_istekleri icindeki 1 lerin sayisi
yolcu_istek_dizi_boyu = max(size(yolcu_istekleri)); 
m = asansor_n*yolcu_istek_dizi_boyu; %kac sutun
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
tablo = zeros(adet, m); %adet tane satir istiyoruz..
for I = 1:1:adet
    don = 1;
    while don == 1
        kromozom1 = [];
        oll = yolcu_istekleri;
        for J = 1:1:asansor_n-1;
            olasilik = round(rand(1, yolcu_istek_dizi_boyu));
            asansoryuk = oll & olasilik;
            oll = oll-asansoryuk;
            kromozom1 = [kromozom1 asansoryuk];
        end
        kromozom1 = [kromozom1 oll];
        if samevek(tablo, kromozom1) == 0
            tablo(I, :) = kromozom1;
            don = 0;
        end
    end
end

end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%ayni satirin olusmamasini saglar
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function varyok = samevek(A, B)
% nxm lik bir matris
% 1xm lik satir vektor
varyok = 0;
[n_a, m_a] = size(A);
[n_b, m_b] = size(B);
for I = 1:1:n_a
    esit = 0;
    for J = 1:1:m_a
        if A(I, J) == B(1, J)
            esit = esit+1;
        end
    end
    if esit == m_a
        varyok = 1;
        break
    end
end
end






function zz = bul(vektor)
zz = find(vektor>0);

end


% RECDIS.M (RECombination DIScrete)
%
% This function performs discret recombination between pairs of individuals
% and returns the new individuals after mating.
%
% Syntax: NewChrom = recdis(OldChrom, XOVR)
%
% Input parameters:
% OldChrom - Matrix containing the chromosomes of the old
% population. Each line corresponds to one individual
% (in any form, not necessarily real-values).
% XOVR - Probability of recombination occurring between pairs
% of individuals. (not used, only for compatibility)
%
% Output parameter:
% NewChrom - Matrix containing the chromosomes of the population
% after mating, ready to be mutated and/or evaluated,
% in the same format as OldChrom.

% Author: Hartmut Pohlheim
% History: 23.11.93 file created
% 24.11.93 style improved
% 06.12.93 change of name of function
% 25.02.94 clean up
% 19.03.94 multipopulation support removed

function NewChrom = uniformX(OldChrom, XOVR);

% Identify the population size (Nind) and the number of variables (Nvar)
[Nind, Nvar] = size(OldChrom);

% Identify the number of matings
Xops = floor(Nind/2);

% which parent gives the value
Mask1 = (rand(Xops, Nvar)<0.5);
Mask2 = (rand(Xops, Nvar)<0.5);

% Performs crossover
odd = 1:2:Nind-1;
even = 2:2:Nind;
NewChrom(odd, :) = (OldChrom(odd, :).* Mask1) + (OldChrom(even, :).*(~Mask1));
NewChrom(even, :) = (OldChrom(odd, :).* Mask2) + (OldChrom(even, :).*(~Mask2));

% If the number of individuals is odd, the last individual cannot be mated
% but must be included in the new population
if rem(Nind, 2), NewChrom(Nind, :) = OldChrom(Nind, :); end

end

% yolcu_istekleri tablosu ile caprazlanmiþ birey arasindaki mantiksal 
% iliþkiyi saðlar ve mutasyonu yapar
%
% birey : mutasyona ugratilacak birey
% yolcu_istekleri :yolcu_istekleri tablosu
% nasansör : asansör sayýsý
% storecount : asansörün duracagi max kat sayisi
 function birey = mutation_v1(birey, yolcu_istekleri, nasansor, storecount)
for J = 1:1:2*storecount %har bir kat istegi icin
    if yolcu_istekleri(J) == 1 %o kat istegi varsa
        is_say = 0; %istek sayisi?
        is_index = [];
        for I = 0:1:nasansor-1 %her bir asansor icin
            if birey(I*2*storecount+J) == 1 %cozumde o katta durmak varsa
                is_say = is_say+1; %o katta duracak asansor sayýsýný mý artýrýyor?
                is_index(is_say) = I*2*storecount+J; 
            end
        end
        if is_say>1 %bir katta birden fazla asansor duracaksa mý?
            birey = is_sil(birey, is_index);
        elseif is_say == 0 %o katta duracak asansor yoksa  mý?
            %%asansorlerin brine rasgele atamak mý? 
            n_dagit = round((nasansor-1)*rand(1)); 
            birey(n_dagit*2*storecount+J) = 1;
        end
    end

end

end

function birey = is_sil(birey, is_index)
say = 0;
while 1
    say = say+1;
    zar = round(rand(1));
    if zar == 1
        birey(is_index(say)) = 0;
        is_index(say) = [];
    end
    if length(is_index) == 1
        break
    end
    if say == length(is_index)
        say = 0;
    end
end
end


function savefigs

uisave
[filein, pathin, filterindex] = uiputfile('*.fig', 'Figurlerin kaydedilecegi dosya ismi');
saveas(1, [ pathin filein '1.fig'])
saveas(2, [ pathin filein '2.fig'])
saveas(3, [ pathin filein '3.fig'])
saveas(4, [ pathin filein '4.fig'])
saveas(5, [ pathin filein '5.fig'])
saveas(6, [ pathin filein '6.fig'])
saveas(7, [ pathin filein '7.fig'])
saveas(8, [ pathin filein '8.fig'])
save eniyicozumdata best_error best_solution tolamsure

end

% XOVDP.M        (CROSSOVer Double Point)
%
% This function performs double point crossover between pairs of
% individuals and returns the current generation after mating.
%
% Syntax:  NewChrom = xovdp(OldChrom, XOVR)
%
% Input parameters:
%    OldChrom  - Matrix containing the chromosomes of the old
%                population. Each line corresponds to one individual
%                (in any form, not necessarily real values).
%    XOVR      - Probability of recombination occurring between pairs
%                of individuals.
%
% Output parameter:
%    NewChrom  - Matrix containing the chromosomes of the population
%                after mating, ready to be mutated and/or evaluated,
%                in the same format as OldChrom.

%  Author:    Hartmut Pohlheim
%  History:   28.03.94     file created

function NewChrom = twopointX(OldChrom, XOVR);

if nargin < 2, XOVR = NaN; end

% call low level function with appropriate parameters
   NewChrom = xovmp(OldChrom, XOVR, 2, 0);


% End of function
end

% XOVSP.M        (CROSSOVer Single-Point)
%
% This function performs single-point crossover between pairs of 
% individuals and returns the current generation after mating.
%
% Syntax:  NewChrom = xovsp(OldChrom, XOVR)
%
% Input parameters:
%    OldChrom  - Matrix containing the chromosomes of the old
%                population. Each line corresponds to one individual
%                (in any form, not necessarily real values).
%    XOVR      - Probability of recombination occurring between pairs
%                of individuals.
%
% Output parameter:
%    NewChrom  - Matrix containing the chromosomes of the population
%                after mating, ready to be mutated and/or evaluated,
%                in the same format as OldChrom.

%  Author:    Hartmut Pohlheim
%  History:   28.03.94     file created

function NewChrom = singlepointX(OldChrom, XOVR);

if nargin < 2, XOVR = NaN; end

% call low level function with appropriate parameters
   NewChrom = xovmp(OldChrom, XOVR, 1, 0);

% End of function
end

