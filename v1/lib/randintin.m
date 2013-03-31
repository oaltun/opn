%random integer values between elements of lb and ub.
function r = randintin(lb,ub)
r = floor(lb + (ub-lb+1) .* rand(size(ub)));