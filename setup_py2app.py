# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import glob
import sys
import os
import site
import meld.build_helpers
import meld.conf
from setuptools import setup

if sys.version_info[:2] < meld.conf.PYTHON_REQUIREMENT_TUPLE:
    version = ".".join(map(str, meld.conf.PYTHON_REQUIREMENT_TUPLE))
    raise Exception("Meld setup requires Python %s or higher." % version)

APP_NAME = 'MeldMerge'
VERSION_STRING = meld.conf.__version__
FORCE_32_BIT = False

PLIST = {
    'CFBundleDocumentTypes': [
        {
            'CFBundleTypeExtensions': ['scmdifftool'],
            'CFBundleTypeIconFile': 'DiffToolDocument',
            'CFBundleTypeName': 'Diff Tool',
            'CFBundleTypeRole': 'Editor',
            'LSTypeIsPackage': True,
        },
    ],
    'LSEnvironment':
    {
        'DYLD_LIBRARY_PATH': 'Contents/Resources/lib:Contents/Frameworks/',
        'LIBRARY_PATH': 'Contents/Resources:/lib:Contents/Frameworks/'
    },
    'CFBundleIdentifier': 'org.gnome.meld',
    'CFBundleShortVersionString': VERSION_STRING,
    'CFBundleSignature': '???',
    'CFBundleVersion': VERSION_STRING,
    'LSPrefersPPC': False,
    'LSArchitecturePriority': 'x86_64',
    'NSHumanReadableCopyright': u'Copyright © 2023',
    'CFBundleDisplayName': 'Meld',
    'CFBundleName': 'Meld',
    'NSHighResolutionCapable': True,
    'NSSupportsSuddenTermination': False,
    'LSApplicationCategoryType': 'public.app-category.productivity',
    'LSRequiresNativeExecution': True,
    'MinimumSystemVersion': '10.13.0',
    'NSRequiresAquaSystemAppearance': False,
    'NSQuitAlwaysKeepsWindows': False,
    'ApplePersistenceIgnoreState': True
}

#find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])

from modulegraph.find_modules import PY_SUFFIXES
PY_SUFFIXES.append('')

gtk_data_dirs = [
    'etc/fonts',
    'etc/gtk-3.0',
    'lib/gdk-pixbuf-2.0',
    'lib/girepository-1.0',
    'share/fontconfig',
    'share/glib-2.0',
    'share/gtksourceview-4',
    #'share/icons',
]

gtk_data_files = []
for data_dir in gtk_data_dirs:
    local_data_dir = os.path.join(sys.prefix, data_dir)

    for local_data_subdir, dirs, files in os.walk(local_data_dir):
        data_subdir = os.path.relpath(local_data_subdir, local_data_dir)
        gtk_data_files.append((
            os.path.join(data_dir, data_subdir),
            [os.path.join(local_data_subdir, file) for file in files]
        ))

setup(
    name="Meld",
    version=meld.conf.__version__,
    description='Visual diff and merge tool',
    author='The Meld project',
    author_email='meld-list@gnome.org',
    maintainer='Kai Willadsen',
    url='http://meldmerge.org',
    license='GPLv2+',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: X11 Applications :: GTK',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Desktop Environment :: Gnome',
        'Topic :: Software Development',
        'Topic :: Software Development :: Version Control',
    ],
    packages=[
        'meld',
        'meld.matchers',
        'meld.ui',
        'meld.vc',
    ],
    package_data={
        'meld': ['README', 'COPYING', 'NEWS']
    },
    scripts=['bin/meld'],
    app=['bin/meld'],
    setup_requires=["py2app"],
    options={'py2app': {
                'includes': [ 'gi', 'weakref', 'encodings', 'pycairo', 'PyGObject', 
                              'pyobjc-core', 'pyobjc-framework-Cocoa',
                              'CoreFoundation', 'Foundation' ],
                'excludes': [ 'tkinter' ],
                'dylib_excludes': [ 'Python' ],
                'frameworks': [ ],
                'argv_emulation': False,
                'no_chdir': True,
                'iconfile': 'osx/meld.icns',
                'plist': PLIST,
                'prefer_ppc': False,
    }},
    data_files=[
        ('share/man/man1',
         ['data/meld.1']
         ),
        ('share/doc/meld',
         ['COPYING', 'NEWS']
         ),
        ('share/meld',
         ['data/gschemas.compiled']
        ),
        ('share/meld',
         ['data/org.gnome.meld.gschema.xml']
        ),
        ('share/meld/icons',
         glob.glob("data/icons/*.png") +
         glob.glob("data/icons/COPYING*")
         ),
        ('share/meld/styles',
         glob.glob("data/styles/*.xml")
         ),
        ('share/meld/ui',
         glob.glob("data/ui/*.ui") + glob.glob("data/ui/*.xml")
        ),
    ] + gtk_data_files,
    cmdclass={
        "build_i18n": meld.build_helpers.build_i18n,
        "build_help": meld.build_helpers.build_help,
        "build_icons": meld.build_helpers.build_icons,
        "build_data": meld.build_helpers.build_data,
    },
)
