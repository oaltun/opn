
function height = rastriginsFunctionJavaLike(x)
n = numel(x);

height=10*n;
for i=1:n
    height=height+x(i)^2 - 10 * cos(2*pi*x(i));
end

end