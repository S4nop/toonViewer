import os


def clean_caches():
    dir = './caches'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))


def make_cache_dir():
    try:
        if not os.path.exists('./caches'):
            os.makedirs('./caches')
    except OSError:
        pass


def remove_extension(file_name):
    new_name = os.path.splitext(file_name)[0]
    os.rename(file_name, new_name)
    return new_name