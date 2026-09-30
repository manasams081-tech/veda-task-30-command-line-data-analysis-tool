# VEDA Technology — Task 30: Command-Line Data Analysis Tool

A complete beginner-friendly implementation of the VEDA Technology Task 30.

## Task requirements covered

- Accepts a CSV file path from the command line
- Uses Pandas for analysis
- Uses `argparse` for command-line options
- Summary, filtering, grouping and statistical reports
- Validates requested columns and gives readable errors
- Includes reusable application design
- Includes help documentation
- Includes sample output
- Includes a unique lightweight browser dashboard
- Uses the same analysis functions for CLI + web interface
- No dataset filename is hardcoded into the CLI

## Technology

Only the task-specified technologies are used for the core application:

- Python
- Pandas
- argparse

The web interface uses Python's built-in `http.server`; no Flask/Django/React dependency is required.

## Folder structure

```text
VEDA_Task_30_Command_Line_Data_Analysis_Tool/
├── app.py
├── analysis.py
├── cli_tool.py
├── requirements.txt
├── README.md
├── .gitignore
├── sample_data/
│   └── sales.csv
└── web/
    ├── index.html
    ├── style.css
    └── app.js
```

## 1. Open the project folder

Windows PowerShell:

```powershell
cd VEDA_Task_30_Command_Line_Data_Analysis_Tool
```

## 2. Create and activate a virtual environment

Recommended with Python 3.12:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Then activate again:

```powershell
.venv\Scripts\Activate.ps1
```

## 3. Install the only external dependency

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 4. Test the CLI

### Help

```powershell
python cli_tool.py --help
```

### Summary

```powershell
python cli_tool.py --file sample_data/sales.csv --summary
```

### Preview

```powershell
python cli_tool.py --file sample_data/sales.csv --preview 5
```

### Filter

```powershell
python cli_tool.py --file sample_data/sales.csv --filter region South
```

### Group

```powershell
python cli_tool.py --file sample_data/sales.csv --group region --metric sales
```

### Statistics

```powershell
python cli_tool.py --file sample_data/sales.csv --stats sales
```

### JSON output

```powershell
python cli_tool.py --file sample_data/sales.csv --summary --json
```

## 5. Run the web application

```powershell
python app.py
```

Open:

```text
http://127.0.0.1:8000
```

The browser dashboard provides Summary, Preview, Filter, Group and Statistics operations.

Press `Ctrl+C` in the terminal to stop the server.

## 6. Test with your own CSV

Put another CSV anywhere you want and pass its path to the CLI:

```powershell
python cli_tool.py --file path\to\your_file.csv --summary
```

For the web dashboard, the included sample dataset is used by default. The CLI is the primary reusable interface for arbitrary CSV files.

## 7. GitHub push — exact safe sequence

### Create the repository

GitHub username shown in the supplied profile screenshot:

```text
manasams081-tech
```

Create a new repository using:

```text
veda-task-30-command-line-data-analysis-tool
```

Do NOT initialize the GitHub repository with a README, `.gitignore`, or license because this project already contains them.

After creating it, the repository URL will be:

```text
https://github.com/manasams081-tech/veda-task-30-command-line-data-analysis-tool
```

### Initialize Git locally

Run these commands from the project folder:

```powershell
git init
git branch -M main
git add .
git status
git commit -m "Complete VEDA Technology Task 30"
git remote add origin https://github.com/manasams081-tech/veda-task-30-command-line-data-analysis-tool.git
git remote -v
git push -u origin main
```

### If Git asks for GitHub login

Complete the browser/device authentication GitHub provides. Do not paste a password into the terminal.

### Verify

Open:

```text
https://github.com/manasams081-tech/veda-task-30-command-line-data-analysis-tool
```

You should see the project files and README.

## If `remote origin already exists`

Run:

```powershell
git remote set-url origin https://github.com/manasams081-tech/veda-task-30-command-line-data-analysis-tool.git
git push -u origin main
```

## If Git says `src refspec main does not match any`

Make sure the commit exists:

```powershell
git status
git add .
git commit -m "Complete VEDA Technology Task 30"
git branch -M main
git push -u origin main
```

## If GitHub says the remote repository already has commits

If you accidentally created the GitHub repository with a README, first run:

```powershell
git pull origin main --rebase
git push -u origin main
```

Resolve any conflict if Git reports one, then:

```powershell
git add .
git rebase --continue
git push -u origin main
```

## Interview questions

### Why build a CLI data tool?

A CLI tool is lightweight, scriptable and easy to automate. Users can run repeatable analysis without opening a graphical application.

### How would you make it work with different datasets?

The CSV path is passed through `--file`, and the tool validates requested column names at runtime instead of hardcoding a specific dataset.

### How would you handle a missing column?

The reusable validation function checks whether the requested column exists and returns a clear error containing the available columns.

## Sample expected outputs

Summary should report 20 rows, 6 columns and the numeric columns.

Grouping by `region` with `sales` produces count, sum, mean, minimum and maximum for each region.

Statistics for `sales` produces count, mean, median, minimum, maximum, standard deviation and sum.

## Submission checklist

- [ ] `python cli_tool.py --help` works
- [ ] Summary works
- [ ] Filter works
- [ ] Group works
- [ ] Statistics works
- [ ] Missing-column validation works
- [ ] Web application opens on port 8000
- [ ] Git commit created
- [ ] GitHub repository is public
- [ ] README is visible
- [ ] LinkedIn post published
- [ ] Repository link submitted to the VEDA internship portal
