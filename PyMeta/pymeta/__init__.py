# 
# def import_subpackages_and_modules():
#     
#     import os
#     from importlib import import_module
#         
#     #get directory of this file
#     filedir=os.path.dirname(os.path.realpath(__file__));
#     
#     #get the length of unneeded first part of the paths
#     l=len(os.sep.join(filedir.split(os.sep)[:-1]))+1
#     
#     #function for preparing the module name and importing it
#     def myimport(apath):
#         try: #try to import. It may not be possible, e.g. may be the dir is not a package.
#             modname= '.'.join(apath[l:].split(os.sep))
#             import_module(modname)
#         except:
#             pass
#         
#     #walk the file system and call myimport function
#     s=os.sep
#     for root, dirs, files in os.walk(filedir):
#         for d in dirs: #import subpackages
#             myimport(root+s+d) 
#         for f in files: #import modules
#             if not f.startswith('_'): 
#                 if f[-3:]=='.py':
#                     myimport(root+s+f[:-3])
#                 if f[-4:]=='.pyc':
#                     myimport(root+s+f[:-4])
#     
# import_subpackages_and_modules()
