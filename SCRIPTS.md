# Datawhys Bootcamp Materials

## Repository Structure

```ascii
.
├── datasets (original datasets)
├── instructor (demo source files with solutions for each session)
│   ├── ...
│   ├── plotting-1 (all materials for this session)
│   │   ├── datasets (datasets used in this session's activities)
│   │   │   ├── age_height.csv
│   │   │   └── ...
│   │   ├── scatterplots_e1.ipynb
│   │   └── ...
│   ├── plotting-2
│   └── ...
├── student (auto-generated to mirror instructor tree)
│   ├── ...
│   ├── plotting-1 (distributed to students with nbgitpuller links)
│   └── ...
├── data_generation.ipynb (handy code snippets, csv dataset edits)
└── README.md
```

## Turning Instructor Source Files into Student Versions for Sessions

### 0. Add Session Activities in instructor

What is needed:

1. Create a directory under instructor with the name of your session with hyphens
2. Create images/datasets subdirectories under your session folder with any files needed for that day's activities
3. Create any Python notebooks for the session and include solutions.
   1. **Don't reference any files or folders outside the session folder**
   2. **Make sure any cells (Markdown or code) that include solutions include a `#!response` tag, so the cell will be empty in the student versions!**
4. If you want to include a PowerPoint presentation, export it as a PDF and include both the pptx and pdf files in the instructor session folder. Any pptx files will be automatically removed from the student version. When exporting, you can also choose a subset of the full ppt slides to appear in the pdf version.
5. If you want to include any additional group activity instruction documents, use either:
   1. a Python notebook with Markdown cells
   2. a docx file exported to PDF. Include both the docx and pdf files in the instructor session folder. Any docx files will be automatically removed from the student version.
6. If you want to include a what-to-do guide for the instructor to follow throughout the session, use a docx file exported to PDF. **Make sure to name the files README_IO.docx and README_IO.pdf.** Include both the docx and pdf files in the instructor session folder. Any files with README_IO in the name will be automatically removed from the student version.

### 1. Generate student notebooks

#### How-tos: Using gen_student_nbks_v2.py

To regenerate the entire student tree:

```zsh
python gen_student_nbks_v2.py $PWD/instructor
```

To regenerate a single subdirectory:

```zsh
python gen_student_nbks_v2.py $PWD/instructor/plotting-1
```

### 2. Generate student subtree branches

Subtree Arguments:

- prefix: relative path to subdirectory to split into separate branch
- b: name of branch

NOTE: `git subtree` might be wonky if there are empty subdirectories in repo

#### How-to

1. From main branch of repo:

```zsh
git subtree split --prefix="student/plotting-1" -b plotting-1
```

1. Push branch to Github:

```zsh
git push -u origin plotting-1
```

### 3. Generate nbgitpuller links

Defaults:

- Uses the JupyterHub server @ https://saturn.olney.ai
- Uses the bootcamp materials repo @ https://github.com/kbridson/datawhys-bootcamp

#### How-tos: Using gen_nbgitpuller_links.py

To see script info and arguments:

```zsh
python gen_nbgitpuller_links.py -h
```

##### Instructor Links

NOTE: Instructor links should be to the main branch which will clone/update the entire repo to a datawhys-bootcamp subdirectory under their JupyterLab home directory.

To generate instructor link:

```zsh
python gen_nbgitpuller_links.py main
```

To generate instructor link to automatically open instructor folder for a specific session:

```zsh
python gen_nbgitpuller_links.py main -f instructor/plotting-1
```

##### Student Links

NOTE: Student links should be to subtree branches which will create subdirectories under their JupyterLab home directory with the same name as the branch.

To generate link for the plotting-1 branch:

```zsh
python gen_nbgitpuller_links.py plotting-1
```

To generate link for the plotting-1 branch and automatically open file scatterplots_e1.ipynb:

```zsh
python gen_nbgitpuller_links.py plotting-1 -f scatterplots_e1.ipynb
```

or

```zsh
python gen_nbgitpuller_links.py plotting-1 --file=scatterplots_e1.ipynb
```
