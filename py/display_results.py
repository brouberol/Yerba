from os import system
import fileinput

def create_project_folders(yerba_root, project_root):
    """
    Creates/copy needed folder and .css & .html files in target project root
    """
    system('mkdir -p {0}/yerba/html/'.format(project_root))
    system('mkdir -p {0}/yerba/css/'.format(project_root))
    system('cp {0}/html/template.html {1}/yerba/html/yerba.html'.format(yerba_root, project_root))
    system('cp {0}/css/yerba.css {1}/yerba/css/'.format(yerba_root, project_root))
    return
               

def fill_html(root, results, stats, title):
    """
    Fill html template with project information
    """
    html = open('{0}/yerba/html/yerba.html'.format(root), 'r')
    text = html.read()
    html.close()
    html = open('{0}/yerba/html/yerba.html'.format(root), 'w')

    # --- TITLE & HEADER GENERATION ---
    if title:
        head  = '<header>\n'
        head += '\t<h1>{0}</h1>\n'.format(title)
        head += '</header>\n'
        text = text.replace('__TITLE__', title + ' - Stats by Yerba')
        text = text.replace('<!-- HEADER -->', head)
    else:
        text = text.replace('__TITLE__', 'Powered by Yerba')
    
    # --- STATS GENERATION ---
    nbfiles, nblines = stats
    st = '<ul>\n'
    st += '\t<li>{0} files</li>\n'.format(nbfiles)
    st += '\t<li>{0} lines of code</li>\n'.format(nblines)
    st += '</ul>\n'
    text = text.replace('<!-- STATS -->', st)

    # --- BARCHART GENERATION ---
    out = ''
    for lang, value in results:
        out += '\n<tr>\n'
        out += '\t<td width="80">\n'
        out += '\t\t<p class"lang">{0}</p>\n'.format(lang)
        out += '\t</td>\n'
        out += '\t<td>\n'
        out += '\t\t<p class="bar" style="width: {0}%">{0}%</p>\n'.format(value)
        out += '\t</td>\n'
        out += '</tr>\n'

    html.write(text.replace('<!-- BARCHART -->', out))
    html.close()
    return

def generate_html(project_root, yerba_root, results, stats, title):
    """
    Main wrapper
    """
    create_project_folders(yerba_root, project_root)
    fill_html(project_root, results, stats, title)
    return
    
    
