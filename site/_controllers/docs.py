import os
import shutil
import stat
import sys
sys.path.insert(0, './_lib/')

from blogofile.cache import bf

output = "_site"
htdocs = "_work"
templates = "_templates/work"


def run():
    if not os.path.exists(htdocs):
        os.makedirs(htdocs)

    if not os.path.exists(templates):
        os.makedirs(templates)

    # copy files from individual doc builds to work dir
    for docs, prefix in bf.config.docs.standard_docs:
        copydir(os.path.join(docs, 'build/templates'), os.path.join(templates, 'docs', prefix), True)
        copydir(os.path.join(docs, 'build/output'), os.path.join(htdocs, 'docs', prefix))
        for name in ['docs.css', 'docutil.css', 'scripts.js', 'style.css', 'alphaapi.html', 
                    'alphaimplementation.html', 'syntaxhighlight.css']:
            if os.path.exists(os.path.join(docs, name)):
                conditional_copy(os.path.join(docs, name), os.path.join(htdocs, 'docs', prefix, name))

    for docs, prefix in bf.config.docs.sphinx_docs:
        copydir(docs, os.path.join(htdocs, 'docs', prefix))

    for root, dirs, files in os.walk(htdocs):

        relative = root.split(os.sep, 1)
        if len(relative) > 1:
            relative = relative[1]
        else:
            relative = ''

        for dir in dirs:
            if not os.path.exists(os.path.join(output, relative, dir)):
                os.makedirs(os.path.join(output, relative, dir))

        html = set([fname for fname in files if fname.endswith('.html')])
        nonhtml = set(files).difference(html)

        for fname in nonhtml:
            conditional_copy(os.path.join(root, fname), os.path.join(output, relative, fname))

#        for fname in html:
#            if isnewer(os.path.join(root, fname), os.path.join(output, relative, fname)):
#                print os.path.join(relative, fname), "->", os.path.join(output, relative, fname)
#                txt = lookup.get_template(os.path.join(relative, fname)).render(req={}, attributes={})
#                outfile = file(os.path.join(output, relative, fname), 'w')
#                outfile.write(txt)
#                outfile.close()




# semi generic directory copy function
def copydir(name, dest, htmlonly=False):
    for root, dirs, files in os.walk(name):
        relative = root[len(name + "/"):]

        for dir in dirs + ['.']:
            if not os.path.exists(os.path.join(dest, relative, dir)):
                os.makedirs(os.path.join(dest, relative, dir))

        for fname in files:
            if htmlonly and not fname.endswith('.html'):
                continue
            conditional_copy(os.path.join(root, fname), os.path.join(dest, relative, fname))

def conditional_copy(f1, f2):
    if isnewer(f1, f2):
        print f1, "->", f2
        shutil.copyfile(f1, f2)

def isnewer(f1, f2):
    return not os.path.exists(f2) or os.stat(f1)[stat.ST_MTIME] > os.stat(f2)[stat.ST_MTIME]

