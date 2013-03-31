%random double values between elements of lb and ub.
function r = randin(lb,ub)
r = rand(size(ub)).*(ub-lb) + lb;