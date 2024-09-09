import os
import nbformat as nbf
import sys
import shutil
import textwrap


def generate_file_tree():
    source_path = sys.argv[1]
    # print('Proj folder: {}'.format(proj_root))
    # print(os.path.exists(proj_root))

    destination_path = source_path.replace('instructor', 'student')

    if os.path.exists(destination_path):
        shutil.rmtree(destination_path)
    shutil.copytree(source_path, destination_path)

    directories_to_convert = [destination_path]
    for root, dirs, files in os.walk(destination_path):
        for d in dirs:
            directories_to_convert.append(os.path.join(root, d))

    for dir in directories_to_convert:
        # print(dir)
        revise_directory(dir)


ACTION_TAG = "#!action"
RESPONSE_TAG = "#!response"
EDIT_TAG = "#!edit"
BL_TAG = "#!blhint"
RESPONSE_ALERT_WRAPPER = [
    '<div class="alert alert-block alert-info">\n',
    '<!-- YOUR ANSWER BEGIN -->\n',
    '\n',
    '\n',
    '\n',
    '\n',
    '\n',
    '<!-- YOUR ANSWER END -->\n',
    '</div>'
]


def revise_directory(dir):
    os.chdir(dir)
    for file in os.listdir():
        # Remove binary files
        if file.endswith('.pptx'):
            os.remove(file)
            continue
        if file.endswith('.docx'):
            os.remove(file)
            continue
        if '_IO' in file:
            os.remove(file)
            continue

        # Revise student activity notebooks
        if file.endswith('.ipynb'):
            ntbk = nbf.read(file, nbf.NO_CONVERT)

            # Change from default conda python in vscode to xpython kernel in Jupyterlab
            ntbk.metadata.kernelspec = {
                "display_name": "xpython",
                "language": "python",
                "name": "xpython"
            }
            # print(ntbk.metadata)

            response_cell_counter = 1

            cells_to_keep = []
            for cell in ntbk.cells:
                # Lock structure and instruction cells
                cell.metadata.editable = False
                cell.metadata.deletable = False

                # Skip toc numbering on Step and Substep cells
                if cell.source.startswith('#') and ('Step' in cell.source or 'Substep' in cell.source):
                    # remove #s
                    heading = cell.source.lstrip('#')
                    header_level = len(cell.source) - len(heading)
                    cell.source = ['<span><h{}>\n'.format(header_level),
                                   heading,
                                   '\n</h{}></span>'.format(header_level)]

                if BL_TAG in cell.source:
                    cell.source = cell.source.replace(BL_TAG, '').strip()

                # Handle student take action cells
                # Cells must contain the appropriate tag
                if ACTION_TAG in cell.source:
                    content = cell.source.replace(ACTION_TAG, '').strip()
                    cell.source = ['<div class="alert alert-block alert-danger">\n',
                                   content,
                                   '\n</div>']

                # Handle student response cells
                # Cells must contain the appropriate tag
                if RESPONSE_TAG in cell.source:
                    # Allow edits
                    cell.metadata.editable = True
                    # Remove answers
                    cell.source = []
                    # Flag as student response in cell metadata
                    if 'datawhys' not in cell.metadata:
                        cell.metadata.datawhys = {}
                    cell.metadata.datawhys.student_response = True
                    cell.metadata.datawhys.response_id = response_cell_counter
                    response_cell_counter += 1
                    # Indicate empty Markdown response cells
                    if cell.cell_type == "markdown":
                        # Wrap in alert-block
                        cell.source = RESPONSE_ALERT_WRAPPER

                if EDIT_TAG in cell.source:
                    # Allow edits
                    cell.metadata.editable = True
                    # Remove tag and newlines at start
                    cell.source = cell.source.replace(EDIT_TAG, '').strip()
                    # Flag as student response in cell metadata
                    if 'datawhys' not in cell.metadata:
                        cell.metadata.datawhys = {}
                    cell.metadata.datawhys.student_response = True
                    cell.metadata.datawhys.response_id = response_cell_counter
                    response_cell_counter += 1
                    # print(repr(cell.source))

                # Remove output from all code cells
                if cell.cell_type == "code":
                    cell.outputs = []
                    cell.execution_count = None

                # Keep revised cell
                cells_to_keep.append(cell)
                # print(cell.metadata)

            # Generate new notebook
            new_ntbk = ntbk
            new_ntbk.cells = cells_to_keep
            nbf.write(new_ntbk, os.path.join(
                dir, file), version=nbf.NO_CONVERT)


generate_file_tree()
