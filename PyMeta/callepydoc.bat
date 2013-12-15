rem aim: this batch file rebuilds the documentation
rem      read epydoc documentation to make the documentation better.

rem installation: download and install these: epydoc, graphviz 

rem usage: double click the file IN THE WINDOWS EXPLORER


rem 
cd /d %~dp0
epydoc.py --html -o doc pymeta -v --name PyMeta --url https://bitbucket.org/oaltun/metaheuristics --graph all --dotpath "C:\Program Files (x86)\Graphviz2.34\bin\dot.exe"
pause
