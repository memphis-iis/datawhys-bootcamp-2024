import os
import textwrap
from tkinter import S
# from aem import con
import nbformat as nbf
import sys
import re
from yattag import Doc, indent

import argparse

parser = argparse.ArgumentParser(
    description="Generate Blockly Hints after cells with tagged Blockly instructions"
)
parser.add_argument("file", help="Relative path to file that should be processed")
parser.add_argument(
    "--instr",
    action=argparse.BooleanOptionalAction,
    help="Flag to turn on inventory of detected blocks",
)

args = parser.parse_args()


def gen_hints(file, instructor_help=False):
    source_path = sys.argv[1]

    BL_TAG = "#!blhint"

    ntbk = nbf.read(source_path, nbf.NO_CONVERT)

    cells_to_keep = []
    for cell in ntbk.cells:
        if "Blockly Hints" in cell.source and not BL_TAG in cell.source:
            continue

        cells_to_keep.append(cell)

        if BL_TAG in cell.source:
            cell_content = cell.source.split("<br>")[0].replace(BL_TAG, "").strip()

            blocks_found = {}
            for key in BLOCK_KEYS:
                blocks_found[key] = contains(cell_content, key)

            hint_cell_content = []
            found = dict(filter(lambda elem: elem[1], blocks_found.items()))
            found = dict(sorted(found.items(), key=lambda item: item[1]))
            not_found = dict(filter(lambda elem: not elem[1], blocks_found.items()))
            if instructor_help:
                for key in found:
                    hint_cell_content.append("- {}? {}".format(key, found[key]))
                # for key in not_found:
                #     hint_cell_content.append(
                #         "- {}? {}".format(key, not_found[key]))

                hint_cell_content.append("\n\n")
            hint_cell_content.append(build_hints(found))

            new_cell = cell.copy()
            new_cell.source = "\n".join(hint_cell_content)
            cells_to_keep.append(new_cell)

    new_ntbk = ntbk
    new_ntbk.cells = cells_to_keep
    nbf.write(new_ntbk, os.path.join(source_path), version=nbf.NO_CONVERT)


BLOCK_KEYS = {
    "SNAP": r":",
    "INSERT": r"<-",
    "FREESTYLE": r"freestyle",
    "IMPORT": r"import \b\S*?\b as",
    "SET_TO": r"set \b\S*?\b to",
    "FROM_GET": r"from \b\S*?\b get",
    "WITH_DO_USING": r"with \b\S*?\b do \b\S*?\b using",
    "CREATE_LIST_WITH": r"create list with",
    "DICT": r"dict",
    "TUPLE": r"\( .. , .. \)",
    "VARIABLE": r"(?<!Create) variable",
    "TEXT": r"\`\" [^\n\"]*? \"\`",
    "BOOLEAN": r"(true|false)",
    "DICT_VARIABLE": r"\[ .. \]",
    "COMPARISON": r" .. (=|<|>|<=|>=|!=) ..",
}


def contains(str, block):
    match = re.search(BLOCK_KEYS[block], str)
    if match:
        return match.start()
    else:
        return None


def build_hints(blocks_found):
    doc, tag, text, line = Doc().ttl()

    with tag("details"):
        line("summary", "Blockly Hints")
        with tag("ul"):
            if blocks_found.get("SNAP") or blocks_found.get("INSERT"):
                with tag("li"):
                    text("Notation")
                    with tag("ul"):
                        for key in NOTATION:
                            if blocks_found.get(key):
                                doc.asis(NOTATION.get(key).get("hint"))
            with tag("li"):
                text("Blocks")
                with tag("ul"):
                    for key in blocks_found:
                        if key in NOTATION:
                            continue
                        block_hints(key, doc, tag)

    return doc.getvalue()


def block_hints(key, doc, tag):
    with tag("li"):
        doc.asis(BLOCKS.get(key).get("general"))
        with tag("ul"):
            doc.asis(BLOCKS.get(key).get("hint"))


NOTATION = {
    "SNAP": {
        "general": ":",
        "regex": r":",
        "hint": "<li><code>A</code> &nbsp;:&nbsp; <code>B</code>&nbsp; means snap blocks A and B together.</li>",
    },
    "INSERT": {
        "general": "&lt;-",
        "regex": r"<-",
        "hint": "<li><code>A</code> &nbsp;&lt;-&nbsp; <code>B</code>&nbsp; means insert block B into the hole in block A.</li>",
    },
}

BLOCKS = {
    "FREESTYLE": {
        "general": "freestyle",
        "regex": r"freestyle",
        "hint": "<li>Unless specifically instructed, use the first block from the FREESTYLE menu.</li>",
    },
    "IMPORT": {
        "general": "<code>import .. as ..</code>",
        "regex": r"import \b\S*?\b as",
        "hint": "<li>The <code>import .. as ..</code> block is found under IMPORT.</li> <li>A variable must have been created before it will appear in the dropdown.</li>",
    },
    "SET_TO": {
        "general": "<code>set .. to</code>",
        "regex": r"set \b\S*?\b to",
        "hint": "<li>The <code>set .. to</code> block is found under VARIABLES.</li> <li>A variable must have been created before it will appear in the dropdown.</li>",
    },
    "FROM_GET": {
        "general": "<code>from .. get ..</code>",
        "regex": r"from \b\S*?\b get",
        "hint": "<li>The <code>from .. get ..</code> block is found under VARIABLES.</li>",
    },
    "WITH_DO_USING": {
        "general": "<code>with .. do .. using ..</code>",
        "regex": r"with \b\S*?\b do \b\S*?\b using",
        "hint": '<li>The <code>with .. do .. using ..</code> block is found under VARIABLES.</li> <li>If <code>do</code> dropdown says "!Not populated until you execute code", click anywhere in the notebook tab, then click try "Run All Above Selected Cell" from the "Run" menu.</li> <li>If <code>with .. do .. using ..</code> block does not want to snap together nicely with the <code>set .. to</code> block, try dragging the <code>set .. to</code> block instead.</li> <li>You can use the <code>+ -</code> controls on the block to change the number of notches. Unless specifically instructed, the block should not have any empty notches when you click Blocks to Code. </li>',
    },
    "CREATE_LIST_WITH": {
        "general": "<code>create list with</code>",
        "regex": r"create list with",
        "hint": "<li>The <code>create list with</code> block is found under LISTS.</li> <li>You can use the <code>+ -</code> controls on the block to change the number of notches. Unless specifically instructed, the block should not have any empty notches when you click Blocks to Code. </li>",
    },
    "DICT": {
        "general": "<code>dict ..</code>",
        "regex": r"dict",
        "hint": "<li>The <code>dict ..</code> block is found under LISTS.</li>",
    },
    "TUPLE": {
        "general": "<code>( .. , .. )</code>",
        "regex": r"\( .. , .. \)",
        "hint": "<li>The <code>( .. , .. )</code> block is found under LISTS.</li>",
    },
    "VARIABLE": {
        "general": "variable",
        "regex": r"(?<!Create) variable",
        "hint": "<li>After it is created, each variable has its own block at the end of the VARIABLES menu.</li>",
    },
    "TEXT": {
        "general": '<code>" .. "</code>',
        "regex": r"\`\" [^\n\"]*? \"\`",
        "hint": '<li>The <code>" .. "</code> block is found under TEXT.</li>',
    },
    "BOOLEAN": {
        "general": "<code>true</code>",
        "regex": r"(true|false)",
        "hint": "<li>The <code>true</code> block is found under LOGIC.</li> <li>Click the dropdown on the <code>true</code> block to make a <code>false</code> block.</li>",
    },
    "DICT_VARIABLE": {
        "general": "<code>\{dictVariable\} [ .. ]</code>",
        "regex": r"\[ .. \]",
        "hint": "<li>The <code>\{dictVariable\} [ .. ]</code> block is found under LISTS.</li>",
    },
    "COMPARISON": {
        "general": "<code> .. = .. </code>",
        "regex": r" .. (=|<|>|<=|>=|!=) ..",
        "hint": "<li>The <code> .. = .. </code> block is found under LOGIC.</li> <li>Use the dropdown to get other comparison operators.</li>",
    },
}

file = args.file
instructor_help = args.instr

gen_hints(file, instructor_help)
