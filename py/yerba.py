from os import walk, getcwd
from os.path import dirname, relpath, abspath
from sys import argv

from toolnames import formats, vcm_dir
from display_results import generate_html

def get_project_files(project_root):
    """
    Given a project root, it returns a list 
    containing all project files, given that
    not contained in a Version Control Manager
    directory (.git, .svn, ...)
    """

    project = walk(project_root)
    project_files = []
    for base, dirs, files in project:
        if vcm_dir[0] not in base and vcm_dir[1] not in base: 
            # we filter out files in .git/.svn... folders
            project_files += files

    return project_files
        
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
    a dictionnary of all programming languages
    used in the project, each one with an associated
    value representing the number of files using this
    language
    """

    res = filter( 
        lambda x : x[1]>0, # filter languages with no found associated files
        [
            (lang, count_files_with_extension(project_files, extension)) 
            for lang, extension in zip(formats.keys(), formats.values())
         ])
    
    return dict(res)

def results_percent(count):
    """
    Given numeric results, returns them in percentage 
    (result integer : 60% --> 60)
    """
    
    nb_files = sum(x for x in count.values())
    percent = dict(count) # This is not copying, this is cloning
    
    for language in percent:
        ratio = int(100*round(float(percent[language]) / nb_files,2))
        percent[language] = ratio
    
    return percent

def yerba_main(project_root, yerba_root):
    """
    Main wrapper for yerba project
    Returns a dictionnary of all programming languages
    used in the project, each one with an associated
    value representing the number of files using this
    language
    """

    project_files = get_project_files(project_root)
    count = filter_files_by_language(project_files)
    stats = results_percent(count)
    generate_html(project_root, yerba_root,  stats)

if __name__ == '__main__':

    if len(argv) >1:
        
        yerba_root = dirname(abspath(argv[0])).replace('/py','')
        root = relpath(argv[1])
        yerba_main(root, yerba_root)
    
    else:
        print 'Too few arguments. Project root directory is needed.'
