function vars = cell2html(cells, a_out,varargin)
%CELL2HTML Convert a cell array to an HTML table
%   CELL2HTML(CELL,FILE) generates an HTML file called FILE whose contents
%   include an html table which reflects the matlab cell array (NxM) CELL.
%
%   CELL2HTML(CELL,FILE,VARARGIN) generates the HTML table based on the
%   cell array CELL, and the arguments passed in VARARGIN (see below). To
%   set the value of a property using varargin, pass the name of the
%   property as an argument, and the value as the very next argument.
%   Possible values are numerics, strings, and logicals. Color values can
%   currently be specified in one of three ways: 1)As a string by
%   specifying a MATLAB color name (e.g., ...'BorderColor','yellow',...)
%   2)As a string represeting an rgb triplet ranging from 0 to 255 (e.g.,
%   ...'BackgroundColor','rgb(255,0,0)',... sets the Background color to
%   red) or 3)In a cell array of the format {red,green,blue} where values
%   are from 0 to 255 (e.g., 'FontColor',{0,255,0},... sets the Font color
%   to green).
%
%       VARARGIN:Properties
%       -BorderSize: determines the thickness of the table border (0 for
%       off) HTML>table#border
%       -BorderColor: determines the color of the table border
%       HTML>table#bordercolor
%       -Caption: defines the tables caption HTML>table>caption
%       -Title: defines the title for the HTML document HTML>head>title
%       -BackgroundColor: defines the background color of the table
%       HTML>table>bgcolor
%       -BackgroundImage: NOT YET IMPLEMENTED
%       -FontColor: the font color inside the table HTML>table#style.color
%       -FontSize: the size of the font inside the table
%       HTML>table#style.font-size
%       -FontFace: the font family used inside the table
%       HTML>table#style.font-family
%       -ShowEmpty: determines whether(true) or not(false) to print a
%       non-breaking white space to otherwise empty cells so that they'll
%       be displayed as empty cells instead of non-eixstent cells.
%       -CellSpacing: the spacing between cells in the table
%       HTML>table#cellspacing
%       -CellPadding: internal padding between a cell and it's contents
%       HTML>table#cellpadding
%       -Transpose: whether(true) or not(false) to transpose the matrix
%       before generating table.
%       -StandAlone: whether to generate an entire HTML document with the
%       table in HTML>body (true), or just the HTML for the table (false)
%
%   See File for futher notes, revision history, future updates, and
%   contact information.
%   
%   Example: display a table of values for y=x^2 in an HTML table with some
%   cellpadding, fontsize of 14, and whose background color is cyan:
%
%       %create the x array
%       x = -10:10;
%       xs = num2cell(x);
%
%       %create the y array
%       y = x.^2;
%       ys = num2cell(y);
%
%       %create the cell array
%       valTable = {'X',xs{:};'Y',ys{:}};
%
%       %generate the HTML, view temp.html outside of ML to see the table
%       cell2html(valTable,'temp.html','Transpose',true,...
%       'CellPadding',3,'FontSize',14,'BackgroundColor','cyan');
%
%
%   See also

%   Notes:
%
%   Bugs/Issues/Current Version/Future Versions:
%       -Future: work on properties/values, comment better
%       -Distant (DISTANT) Future: GUI for special formatting of individual
%       cells/rows/cols/groups, etc.
%
%   Revision history:
%       V. 1.0 R1 - 2004-05-04 - Brian Mearns
%       =====================================
%       -Created
%
%   Contact:
%       -Brian Mearns
%        bmearns#coe.neu.edu
%        (change # to @)
%        Please include something coherent and relevant in the subject line 
%        so I don't toss it out with the junk mail. And feel free to harass
%        me about making updates/fixes. Otherwise, I may never care enough
%        again.
%
%   version = I.F:b.q R
%       I: Infrastructure: Primarily reserved for major changes to the
%       infrstructure or other huge changes
%       F: Functionality: When new features are added
%       b: bug fixes: when a bug is fixed
%       q: quality engineering: slight alterations to improve quality;
%       e.g., increase speed (without major re-architecting), clean up gui,
%       etc. 
%       R: release number: the number of times this has been released up to
%       (and inclduing) this one (preceeded by an 'R');

%initialize variables
vars = struct(	'BorderSize','1',...
				'BorderColor','',...
				'Caption','',...
				'Title','',...
				'BackgroundColor','',...
				'BackgroundImage','',...
				'FontColor','black',...
				'FontSize','20',...
				'FontFace','Times',...
				'ShowEmpty','true',...
				'CellSpacing','0',...
				'CellPadding','0',...
				'Transpose','false',...
				'StandAlone','true'...
			);

%allowable color names
colorNames = {'yellow','magenta','cyan','red','green','blue','white',...
															'black',''};
														
F = false;
T = true;

%Evaluate VARARGINS
idx=1;
while idx<=length(varargin);
	
	%find out what the argument is
	arg = varargin{idx};
	if ~ischar(arg)
		warning(['Unacceptable argument passed: Arguments other than ',...
			'property values must be chars. Ignoring Argument.']); 
	else

		%step to the next index, possibly the value for the property.
		%If the argument doesn't take a value, that case will decremement
		%the idx to compensate for this.
		idx = idx + 1;

		warn = false;
		warnMessage = '';
		val = [];
		%get the 'value' for the property, which may or may not be a value,
		%depending on the argument.
		if (idx<=length(varargin))
			val = varargin{idx};
			oval = val;
		end

		if ~isnumeric(val) && ~ischar(val) && ~islogical(val)
			val = [];
			warn = true;
			warnMessage = sprintf(['Unacceptable value passed to ',...
				'property (',arg,'):\n',...
				'\tArguments must be ',...
				'chars, numerics, or logicals. Ignoring.']);
		end

		evaluateArg = true;
		if isfield(vars,arg)
			defVal = getfield(vars,arg); %#ok<GFLD>
		else
			defVal = '';
		end
		
		colorArgs = {vars,arg,val,oval,colorNames,defVal};
		switch arg

			case 'StandAlone'
				expectedCells = {T,F,F,'true','false'};
				
			case 'FontFace'
				expectedCells = {F,F,F,'arial','times','serif'};
				
			case 'FontSize'
				expectedCells = {F,T,F};
				
			case 'Transpose'
				expectedCells = {T,F,F,'true','false'};
				
			case 'BorderSize'
				expectedCells = {T,T,F};
				
			case 'Caption'
				expectedCells = {F,F,T};
				
			case 'Title'
				expectedCells = {F,F,T};
                
            case 'FontColor'
				[vars,evaluateArg,expectedCells,defVal] =...
											evaluateColor(colorArgs{:});
				
			case 'BackgroundColor'
				[vars,evaluateArg,expectedCells,defVal] =...
											evaluateColor(colorArgs{:});
				
			case 'BorderColor'
				[vars,evaluateArg,expectedCells,defVal] =...
											evaluateColor(colorArgs{:});
                                        
            case 'CellPadding'
                expectedCells = {F,T,F};
                
            case 'CellSpacing'
                expectedCells = {F,T,F};
				
			otherwise
				warning(['Unknown argument: ',arg,'. Ignoring.']);
				evaluateArg = false;
				idx = idx - 1;
		end
		if evaluateArg
			pVal = takeAnArgCase(warn,warnMessage,arg,...
												expectedCells,val,defVal);
			if ~isempty(pVal)
				vars = setfield(vars,arg,pVal); %#ok<*SFLD>
			end
		end
	end
	idx = idx+1;
	
end



%transpose if desired
if strcmp(vars.Transpose,'true')
	cells = cells';
end

%find out how big the table will be
sz = size(cells);

%open the output file for writing
fid = fopen(a_out,'w');

%setup an html document and table
if strcmp(vars.StandAlone,'true')
	fprintf(fid,['<html>\n\n\t<head>\n\t\t<title>',vars.Title,...
                    '</title>\n\t</head>\n\n\t<body>\n\n']);
end

%set up an HTML table
fprintf(fid,['\t\t<table ',...
				'style="',...
					'color:',vars.FontColor,'; ',...
					'font-size:', vars.FontSize,'; ',...
					'font-family:', vars.FontFace,'; ',...
				'" ',...
                'cellpadding="',vars.CellPadding,'" ',...
                'cellspacing="',vars.CellSpacing,'" ',...
				'border="',vars.BorderSize,'" ',...
				'bordercolor="',vars.BorderColor,'" ',...
				'bgcolor="',vars.BackgroundColor,'"',...
			'>\n']);	
		
%add the caption
fprintf(fid,['\t\t\t<caption>',vars.Caption,'</caption>\n']);

%step through each row
for j=1:sz(1);
	
	%begin a TableRow
	fprintf(fid,'\t\t\t<tr>\n');
	
	%step through each column in the current row
	for i=1:sz(2);

		%find out the value of the cell, convert it to a string if
		%neccessary. If it's not a char not a numeric, or is NaN, c will be
		%left unchanged, that is, it will be a 'Non Breaking White Space'.
		%This is an HTML convention which causes an otherwise empty cell to
		%be displayed.
		
		x = cells{j,i};                    %get the value
		if strcmp(vars.ShowEmpty,'true')
			c = '&nbsp;';					%'Non Breaking White Space'
		else
			c = '';
		end;
%         x
%         isnumeric(x)
%         ~isnan(x)
		if isnumeric(x)
            if ~isnan(x)
                c = num2str(x);
            end
		elseif ischar(x)
			c = x;
		end
		
		%write a TableData element with the correct contents
		fprintf(fid,['\t\t\t\t<td>',c,'</td>\n']);	
		
	end
	
	%close the TableRow 
	fprintf(fid,'\t\t\t</tr>\n');
	
end

%Close the table
fprintf(fid,'\t\t</table>\n\n');

if strcmp(vars.StandAlone,'true')
	fprintf(fid,'\t</body>\n\n</html>');
end

%close the file
fclose(fid);

end
%-------------------------------------------------------------------------%
function warnUnknownValue(propName,expected,got, varargin)	
	if length(varargin)==1
		defaultVal = [' ',varargin{1}];
	else
		defaultVal = '';
	end
		
	if isnumeric(got)
		got = num2str(got);
	elseif ischar(got)
		got = ['''',got,''''];
	end
	
	expVals = '';
	if islogical(expected{1}) && expected{1}
		expVals = [expVals,'A logical:'];
	end
	if islogical(expected{2}) && expected{2}
		expVals = [expVals,'A numeric:'];
	end
	if islogical(expected{3}) && expected{3}
		expVals = [expVals,'A double:'];
	end
	expVals = [expVals,cell2str(expected(4:length(expected)))];
	
	warning off MATLAB:sprintf:InputForPercentSIsNotOfClassChar
	warning(['Unknown value for property, %s.\n'...
				'\tExpected: %s.\n',...
				'\tReceived: %s.\n',...
				'\tIgnoring Property configure, using default value%s.'],...
				propName,expVals,got,defaultVal);	
	warning on MATLAB:sprintf:InputForPercentSIsNotOfClassChar
end
%-------------------------------------------------------------------------%
function warnNeedsValue(propName)
	warning(['Property requires a value: ',propName]); %#ok<*WNTAG>
end
%-------------------------------------------------------------------------%
function val = evalArgin(propName,expectedCells,received,varargin)
%expectedCells = {bLogicalOk, bNumericOk, bCharOk, otherAcceptables}
	if isempty(received) && isnumeric(received)
		warnNeedsValue(propName);
		val = [];
		return;
	end
	if ~islogical(expectedCells{1}) ||...
		~islogical(expectedCells{2}) ||...
		~islogical(expectedCells{3})
			error(['I''m sorry. There is an error in the program.\n',...
				'The expectedCells array for property %s does not ',...
				'match the expected format.\nThe first three items ',...
				'must be  logicals.\n',...
				'Please send this error message to Brian Mearns at\n',...
				'\tbmearns@coe.neu.edu\t\n',...
				'With the subject line: ',...
				'"ROATUSUDAUA:Program Bug in xls2html".\n',...
				'Sorry for any inconvenience.'],propName);
	end
	if expectedCells{1} && islogical(received)
		if (received)
			val='true';
		else
			val = 'false';
		end
		return;
	elseif expectedCells{2} && isnumeric(received)
		val = num2str(received);
		return;
	elseif expectedCells{3} && ischar(received)
		val = received;
		return;
	else
		for i=4:length(expectedCells)
			x = expectedCells{i};
			if isnumeric(received) && isnumeric(x) && received==x
				val = num2str(received);
				return;
			elseif ischar(received) && ischar(x) && strcmp(received,x)
				val = received;
				return;
			end
		end
	end
	val = [];
	%varargin is default value or nothing
	warnUnknownValue(propName,expectedCells,received,varargin{:});
	return;
	
end
%-------------------------------------------------------------------------%
function string = cell2str(cellArray)
	string = '';
	for i=1:length(cellArray)
		x = cellArray{i};
		if isnumeric(x);
			str = num2str(x);
		elseif ischar(x);
			str = ['''',x,''''];
		elseif islogical(x) && x
			str = 'true';
		elseif islogical(x) && ~x
			str = 'false';
		else
			str = '<unknown value>';
		end
		if(i>1)
			str = [':', str]; %#ok<*AGROW>
		end
		string = [string,str];
	end

end
%-------------------------------------------------------------------------%
function retVal = takeAnArgCase(warn,message,propName,expectedCells,received,varargin)

	retVal = [];
	%means that the value passed was of an undesriable type
	if warn
		warning(message);

	%means there was no value passed
	elseif isempty(received) && isnumeric(received)
		warnNeedsValue(propName);

	%an agreeable value was passed, evaluate it
	else
		retVal = evalArgin(propName,expectedCells,received,varargin{:});
	end
	
end
%-------------------------------------------------------------------------%
function [vars,evaluateArg,expectedCells,defVal] = ...
						evaluateColor(vars,arg,val,oval,colorNames,defVal)

	evaluateArg = false;
	expectedCells = {false,false,false};
	if ischar(val)
		%can specify in rgb(x,x,x) format where 0<=x<=255
		if strncmpi(val,'rgb(',4) && val(length(val))==')'
			vars = setfield(vars,arg,val);
		%can specify with specific color names
		else
			expectedCells = {false,false,false,colorNames{:},'',}; %#ok<*CCAT>
			evaluateArg = true;
		end
	%can specify an rgb value in an cell array
	elseif iscell(oval) && length(oval)==3
		vars = setfield(vars,arg,...
					['rgb(',num2str(oval{1}),',',...
							num2str(oval{2}),',',...
							num2str(oval{3}),')']);
	else
		%will automatically fail, and behave accordingly
		expectedCells = {false,false,false};
		evaulateArg = true; %#ok<NASGU>
	end
	
end

