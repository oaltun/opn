classdef SupplyChainCostState
     properties
%         WM %warehouse to Market distribution
%         PW %Plant to warehouse distribution
%         SP %Supplier to plant distribution
        dists = {};
        names = {'WM','PW', 'SP'};
    end
    methods
        function str= mat2str(self)
            str = '';
            for i=1:numel(self.dists)
                str = strcat(str, self.names{i}, ':', mat2str(self.dists{i}), ' ');
            end
        end
    end
end