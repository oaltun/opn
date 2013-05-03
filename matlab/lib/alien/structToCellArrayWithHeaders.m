% This function accepts a MATLAB struct, and outputs
% a cell array with the same data contents as the struct
% laid out as a table with the field names of the structure
% as column headers.
% Example:
%
% weather = 
% 
% 1x3 struct array with fields:
%     temp
%     rainfall
%     sunrise
%     sunset
%
% weather(1)
% ans = 
%         temp: 68
%     rainfall: 0.2000
%      sunrise: 10.5000
%       sunset: 18.5000
%
% wxcell = structToCellArrayWithHeaders ( weather );
%
% wxcell = 
% 
%     'temp'    'rainfall'    'sunrise'    'sunset' 
%     [  68]    [  0.2000]    [10.5000]    [18.5000]
%     [  80]    [  0.4000]    [10.5500]    [18.6000]
%     [  72]    [       0]    [10.6000]    [18.6500]
%
function [outCellArray] = structToCellArrayWithHeaders ( inStruct )
	colnames = fieldnames ( inStruct );
	for colctr = 1:size(colnames,1)
		outCellArray(1,colctr) = {char(colnames(colctr))};
	end
	for rowctr = 1:size(inStruct,2)
		for colctr = 1:size(colnames,1)
			outCellArray(rowctr+1,colctr)={inStruct(rowctr).(char(colnames(colctr)))};
		end
	end
end