%%% a class to easily obtain a pass-by-reference
%%% behaviour.
classdef Ref<handle
    properties
        data
    end
    methods
        function self = Ref(dat)
            self.data=dat;
        end
    end
end