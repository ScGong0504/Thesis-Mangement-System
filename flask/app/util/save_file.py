import time
from config import file_path


def save_file(file_name, content):
    new_file_name = file_path + file_name[0:file_name.rindex('.'):] + str(time.time()) + '.' \
                    + file_name[file_name.rindex('.')::]
    with open(new_file_name, 'w') as f:
        f.write(str(content))
        f.close()
    return new_file_name
