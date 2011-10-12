"""

"""

from os import system
import fileinput

def create_project_folders(root):
    system('mkdir -p {0}/yerba/html/'.format(root))
    system('mkdir -p {0}/yerba/css/'.format(root))
    system('cp ../html/template.html {0}/yerba/html/yerba.html'.format(root))
    system('cp ../css/yerba.css {0}/yerba/css/'.format(root))
    return
               

def fill_html(root, results):
    html = open('{0}/yerba/html/yerba.html'.format(root), 'r')
    text = html.read()
    html.close()
    
    out = ''
    for lang in results:
        out+='\n<tr>\n'
        out+='\t<td width="80">\n'
        out+='\t\t<p class"lang">{0}</p>\n'.format(lang)
        out+='\t</td>\n'
        out+='\t<td>\n'
        out+='\t\t<p class="bar" style="width: {0}%">{1}%</p>\n'.format(results[lang], results[lang])
        out+='\t</td>\n'
        out+='</tr>\n'
        
    html = open('{0}/yerba/html/yerba.html'.format(root), 'w')
    html.write(text.replace('<!-- REPLACE ME -->', out))
    html.close()
    return

def generate_html(project_root, results):
    create_project_folders(project_root)
    fill_html(project_root, results)
    return
    
    
