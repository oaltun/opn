        function arr=arrayof(n,fun,varargin)
            arr{n}=[];
            for i=1:n
                arr{i}=fun(varargin{:});
            end
        end