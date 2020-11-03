import os
import pathlib
import sys
from shutil import copy, rmtree, move, make_archive
from tempfile import mkdtemp
from time import sleep

import pytest

cmd = '' if len(sys.argv) < 2 else sys.argv[1]
thisDir = os.path.join(pathlib.Path(__file__).parent.absolute())
distDir = os.path.join(thisDir, 'dist')


# returns path to the unzipped addon
def mkAddon() -> str:
    tmpdir = mkdtemp()
    a1 = os.path.join(thisDir, 'anki_step_images.py')
    a2 = os.path.join(thisDir, 'cardarea.js')
    a3 = os.path.join(thisDir, 'extract_steps.py')
    b1 = os.path.join(tmpdir, 'anki_step_images.py')
    b2 = os.path.join(tmpdir, 'cardarea.js')
    b3 = os.path.join(tmpdir, 'extract_steps.py')
    b4 = os.path.join(tmpdir, '__init__.py')

    copy(a1, b1)
    copy(a2, b2)
    copy(a3, b3)

    with open(b4, 'w+') as fp:
        fp.write('from . import anki_step_images')

    return tmpdir


# zips the addon and places it in dist directory
def mkZippedAddon():
    tmpBundleDir = mkAddon()
    addonDest = os.path.join(distDir, 'anki-step-images.ankiaddon')
    addonDestWithZip = addonDest + '.zip'

    if not os.path.exists(distDir):
        os.makedirs(distDir)

    try:
        make_archive(addonDest, 'zip', tmpBundleDir)
        move(addonDestWithZip, addonDest)
    except:
        pass

    rmtree(tmpBundleDir)


def createAddonToTest():
    ankiTestDir = os.path.join(
        pathlib.Path.home(),
        'Library/Application Support/Anki2/addons21/test_anki_step_images')
    tmpdir = mkAddon()
    rmtree(ankiTestDir, ignore_errors=True)
    move(tmpdir, ankiTestDir)


def testAddon():
    createAddonToTest()
    os.system('killall Anki > /dev/null 2>&1')
    while os.system('pgrep Anki > /dev/null 2>&1') == 0:
        sleep(1)
    os.system('ANKI_DEV=true open -a Anki')


if cmd == 'test':
    pytest.main(['anki_step_images_test.py'])
    testAddon()
elif cmd == 'quicktest':
    pytest.main(['anki_step_images_test.py'])
elif cmd == 'dist':
    mkZippedAddon()
else:
    print('missing/invalid command argument')
