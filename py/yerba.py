from os import walk, getcwd, system
from os.path import dirname, relpath, abspath, exists
from sys import argv
from getopt import getopt, GetoptError

from toolnames import formats, exclude_dir
from display_results import generate_html

def get_project_files(project_root):
    """
    Given a project root, it returns a list 
    containing all absolute path tpproject files,
    given that they are not contained in a Version 
    Control Manager directory (.git, .svn, ...)
    """

    project = walk(project_root)
    project_files = []
    for base, dirs, files in project:
        if exclude_dir[0] not in base and exclude_dir[1] not in base and exclude_dir[2] not in base: 
            # we filter out files in .git/.svn... folders
            for f in files:
                for value in formats.values(): # Ugly but C++ contains several extensions (hpp, h, cpp)
                    if f.split('.')[-1].lower() in value: # if known extensions
                        project_files.append(abspath(base+'/'+f))
                                   
    return project_files

def stats_files(files):
    """
    Given a list of abspaths to files, it returns
    the number of files and the total number of lines
    in all files
    """

    tot_nb_lines= 0
    for p_file in files:
        with open(p_file, 'r') as f:
            for line in f:
                tot_nb_lines+=1
    nb_files = len(files)

    return (nb_files, tot_nb_lines)

def count_lines_by_extension(project_files):
    """
    Given a list of the project files, it returns
    the number of lines of code written in each language
    """

    res = []
    for extensions in formats.values():
        nb_lines = 0
        
        if type(extensions) is list: # ex : C++
            for extension in extensions: # C++ contains several exensions (hpp, cpp, h) 
                for p_file in project_files: # for each project file 
                    if p_file.split('.')[-1].lower() == extension: #split returns file extension
                        with open(p_file,'r') as f: # count nblines
                            for line in f:
                                Nb_lines+=1
            res.append(nb_lines)
            
        else:
            for p_file in project_files:
                if p_file.split('.')[-1].lower() == extensions: #split returns file extension
                    with open(p_file,'r') as f:
                        for line in f:
                            nb_lines+=1
            res.append(nb_lines)

    return res

def filter_files_by_language(project_files):
    """
    Given a list of the project files, it returns
    a list of lists of all programming languages
    used in the project, each one with an associated
    value representing the number of lines written
    in a given language
    """

    res = filter( 
        lambda x : x[1]>0, # filter out languages with no found associated files
        [
            [lang, nblines]
            for lang, nblines in zip(formats.keys(), count_lines_by_extension(project_files))
         ])
    return res

def results_percent(count):
    """
    Given numeric results, returns them in percentage 
    (result integer : 60% --> 60)
    """
    
    tot_nb_lines = sum(lines for (lang, lines) in count)
    percent = list(count) # This is not copying, this is cloning

    for i in range(len(count)):
        percent[i][1] = int(100*round(float(count[i][1]) / tot_nb_lines,2))
    
    percent = sort_result(percent)

    return percent

def sort_result(percent):
    return sorted(percent, key = lambda x: -x[1]) 

def yerba_main(project_root, yerba_root, title):
    """
    Main wrapper for yerba project
    Returns a dictionnary of all programming languages
    used in the project, each one with an associated
    value representing the number of files using this
    language
    """

    project_files = get_project_files(project_root)
    stats = stats_files(project_files)
    count = filter_files_by_language(project_files)
    percent = results_percent(count)
    generate_html(project_root, yerba_root,  percent, stats, title)

if __name__ == '__main__':
 
    EXIT_MESSAGE = 'Program is terminating.'
    if len(argv) >1:
        
        if argv[1].startswith('-'):
            print 'Error : first argument must be the path to your project. Got %s instead.' %(argv[1])
            print EXIT_MESSAGE
            exit(2)

        try:
            arg, opts = getopt(argv[2:], 't:')
        except GetoptError as err:
            print 'Error:', err
            print EXIT_MESSAGE
            exit(2)

        title = None
        for o, a in arg:
            if o in "-t":
                title = a
            else:
                assert False, "unhandled option"
            
        yerba_root = dirname(abspath(argv[0])).replace('/py','')
        project_root = relpath(argv[1])
        if exists(project_root):
            yerba_main(project_root, yerba_root, title)
        else:
            print 'Error: the given path %s leads to no existing directory.' %(project_root)
            print EXIT_MESSAGE
            exit(2)
    
    else:
        print 'Too few arguments. Project root directory is needed.'
