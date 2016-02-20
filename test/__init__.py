import glob, os, shutil


TEST_FILE_DIR = 'test/files/'


def setup():
    """ Copy the testing files to the current working dir. """
    for file in glob.glob('{}*'.format(TEST_FILE_DIR)):
        new_dest = file.replace(TEST_FILE_DIR, '')
        shutil.copy(file, new_dest)


def teardown():
    """ Delete the files. """
    for file in glob.glob('{}*'.format(TEST_FILE_DIR)):
        new_dest = file.replace(TEST_FILE_DIR, '')
        os.remove(new_dest)

    for file in glob.glob('metapipe.*.job'):
        os.remove(file)

    for file in glob.glob('metapipe.*.output*'):
         os.remove(file)

    for file in glob.glob('metapipe.*_stdout'):
        os.remove(file)

    for file in glob.glob('metapipe.*_stderr'):
        os.remove(file)
