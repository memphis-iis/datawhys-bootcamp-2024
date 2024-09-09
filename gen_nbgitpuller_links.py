import urllib.parse as ulp
import argparse

parser = argparse.ArgumentParser(
    description='Generate nbgitpuller link for Datawhys Bootcamp repo subtree branches')
parser.add_argument('branch',
                    help='Name of branch in repo to clone')
parser.add_argument('-f', '--file',
                    default='', dest='file',
                    help='Relative path to file or subdirectory that should be automatically opened in JupyterHub (default is to open cloned folder in file tree sidebar but not open any new file tabs)')
parser.add_argument('-b', '--blockly',
                    default='py', dest='blockly',
                    help='Set Blockly plugin version, default is python version')

args = parser.parse_args()


def generate_link(branch, file_to_open='', blockly_version='py'):
    jupyter_hub_url = 'https://saturn.olney.ai'
    # repo = 'https://github.com/kbridson/datawhys-bootcamp'
    repo = 'https://github.com/kbridson/datawhys-bootcamp-2022'

    # Subdirectory to clone into
    if branch == 'main':
        target_path = 'datawhys-bootcamp'
    else:
        target_path = branch

    # Folder or file to auto-open in Jupyterlab
    url_path = 'lab/tree/{}'.format(target_path)
    if file_to_open:
        file_path = '/{}'.format(file_to_open)
    else:
        file_path = ''

    logging_flag = '?log=https://logging.olney.ai/datawhys/log'
    file_path += logging_flag

    if file_to_open.endswith('.ipynb'):
        blockly_flag = '&bl={}'.format(blockly_version)
        file_path += blockly_flag

    # return '{}/hub/user-redirect/git-pull?repo={}&branch={}&targetPath={}&urlpath={}{}'.format(
    return '{}/hub/user-redirect/git-pull?repo={}&urlpath={}{}&branch={}&targetPath={}'.format(
        jupyter_hub_url,
        ulp.quote_plus(repo),
        ulp.quote_plus(url_path),
        ulp.quote_plus(file_path),
        branch,
        target_path,
    )


branch = args.branch
file_to_open = args.file
blockly_version = args.blockly

url = generate_link(branch, file_to_open, blockly_version)
print(url)


# # Test cases
# branch = 'plotting-1'
# file = 'scatterplots_e1.ipynb'
# test_url = 'https://saturn.olney.ai/hub/user-redirect/git-pull?repo=https%3A%2F%2Fgithub.com%2Fkbridson%2Fdatawhys-bootcamp&branch=plotting-1&targetPath=plotting-1&urlpath=lab%2Ftree%2Fplotting-1/scatterplots_e1.ipynb'
# url = generate_link(branch, file)
# print(url == test_url)

# branch = 'plotting-1'
# test_url = 'https://saturn.olney.ai/hub/user-redirect/git-pull?repo=https%3A%2F%2Fgithub.com%2Fkbridson%2Fdatawhys-bootcamp&branch=plotting-1&targetPath=plotting-1&urlpath=lab%2Ftree%2Fplotting-1'
# url = generate_link(branch)
# print(url == test_url)
