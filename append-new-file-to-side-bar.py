import os
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')


def get_markdown_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.md')]


def update_sidebar(sidebar_path, files):
    with open(sidebar_path, 'r') as f:
        lines = f.readlines()

    with open(sidebar_path, 'a') as f:
        for file in files:
            if file not in ''.join(lines):
                if lines[-1] != '\n':
                    f.write('\n')
                f.write(f'  - [{file[:-3]}]({file})\n')
                logging.info(f'Added link to {file[:-3]} in sidebar')


if __name__ == '__main__':
    docs_directory = 'docs'
    sidebar_path = os.path.join(docs_directory, '_sidebar.md')
    files = get_markdown_files(docs_directory)
    files = [f for f in files if f not in ['README.md', '_sidebar.md']]
    update_sidebar(sidebar_path, files)
