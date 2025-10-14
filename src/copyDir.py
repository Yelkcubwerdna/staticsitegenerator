import os
import shutil

def copyDir(src_dir, copy_dir):
    # Check if copy_dir exists, delete it if does
    if os.path.exists(copy_dir):
        shutil.rmtree(copy_dir)

        #Make a new dir
        os.mkdir(copy_dir)
    else:
        # Make the dir
        os.mkdir(copy_dir)


    # Get a list of the src dir
    ls = os.listdir(src_dir)


    # Go thru the list and copy each file and folder
    for item in ls:
        src_path = os.path.join(src_dir, item)
        # Is this a file or folder
        # Copy it either way, but requires a different method per result
        if os.path.isfile(src_path):
            shutil.copy(src_path, copy_dir)
        else:
            copy_path = os.path.join(copy_dir, item)
            copyDir(src_path, copy_path)