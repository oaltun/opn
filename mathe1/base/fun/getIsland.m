%this function prepares a two dimensional matrix for trying optimization
%routines. For this, the peaks function is used. matrices returned by the
%peaks functions are added to the random places in the map.
%parameters:
%h: height of the island
%w: width of the island
%k: width parameter for the peaks function
%s: random generator start point
%n: number of peaks overlapped.
function island=getIsland(varargin)

%%% arg handling
args.height = 100;
args.width = 500;
args.pwidth = 50;
args.rstart =0;
args.npeaks =1000;
args=overwrite(args,varargin);


%shorter names
h=args.height;
w=args.width;
k=args.pwidth;
s= args.rstart;
n=args.npeaks;

rng(s);

%rng(s,'twister')

% k=200;
% w=500;

island = zeros(h,w);

for i=1:n
    y=randint(1,1,[1 h-k]);
    x=randint(1,1,[1 w-k]);
    island(y:y+k-1,x:x+k-1)=island(y:y+k-1,x:x+k-1)-peaks(k)*rand;
end

% surf(island)
% shading flat
% view(150,10)
end