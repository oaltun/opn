function q = rosenbrockFunction(solution)
xi=solution(1:end-1);
xip1=solution(2:end);
q = sum((1-xi).^2 + 100*(xip1-xi.^2).^2);