from os import walk, getcwd, system
from os.path import dirname, relpath, abspath
from sys import argv
from getopt import getopt, GetoptError

from toolnames import formats, vcm_dir
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
        if vcm_dir[0] not in base and vcm_dir[1] not in base: 
            # we filter out files in .git/.svn... folders
            for f in files:
                if f.split('.')[-1] in formats.values(): # if known extension
                    project_files.append(abspath(base+'/'+f) )                                   

    return project_files

def stats_files(files):
    """
    Given a list of abspaths to files, it returns
    the number of files and the total number of lines
    in all files
    """
    tot_nb_lines= 0
    for p_file in files:
        f = open(p_file, 'r')
        li = len(f.readlines())
        f.close()
        tot_nb_lines += li
    nb_files = len(files)

    return (nb_files, tot_nb_lines)
        
        
        
def count_files_with_extension(project_files, extension):
    """
    Given a list of the project files, it returns
    an integer value of the number of times a file
    extension is seen
    """

    res = 0
    for p_file in project_files:
        if extension == p_file.split('.')[-1]: #split returns file extension
            res+=1

    return res

def filter_files_by_language(project_files):
    """
    Given a list of the project files, it returns
    a list of lists of all programming languages
    used in the project, each one with an associated
    value representing the number of files using this
    language
    """

    res = filter( 
        lambda x : x[1]>0, # filter languages with no found associated files
        [
            [lang, count_files_with_extension(project_files, extension)] 
            for lang, extension in zip(formats.keys(), formats.values())
         ])

    return res

def results_percent(count):
    """
    Given numeric results, returns them in percentage 
    (result integer : 60% --> 60)
    """
    
    nb_files = sum(value for (lang, value) in count)
    percent = list(count) # This is not copying, this is cloning
    
    for language, value in percent:
        ratio = int(100*round(float(value) / nb_files,2))
        value = ratio
    
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
    
    if len(argv) >1:
        arg, opts = getopt(argv[2:], 't:')

        title = None
        for o, a in arg:
            if o in "-t":
                title = a
            else:
                assert False, "unhandled option"
            
        yerba_root = dirname(abspath(argv[0])).replace('/py','')
        root = relpath(argv[1])
        yerba_main(root, yerba_root, title)
    
    else:
        print 'Too few arguments. Project root directory is needed.'
