[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fchenghui-lee%2FMAYA-Xtractor&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)

# MAYA-Xtractor
MAYA-Xtractor is a script to extract all the timetables over the faculties and tabulate them in CSV files.

## Prerequisite
- Python 3: [Download](https://www.python.org/downloads/)
- pip: [Download](https://pip.pypa.io/en/stable/installing/)
- git: [Download](https://git-scm.com/download/)
- Google Chrome: [Download](https://www.google.com/chrome/)
- ChromeDriver: [Download](https://chromedriver.chromium.org/downloads)

## Initialize
To begin, clone this repository in your local environment.

```$ git clone https://github.com/chenghui-lee/MAYA-Xtractor/```

And cd into the cloned directory

```$ cd MAYA-Xtractor/```

Install the required packages

```$ pip install -r requirements.txt```

Change the environment attributes in ```env.py``` according to your needs.

This including your Maya username, password and path to your ChromeDriver.

```python
os.environ['USERNAME'] = '175598874' # Your new Maya ID here
os.environ['PASSWORD'] = 'password12345' # Your Maya Password
os.environ['PATH'] = 'E:\Selenium\ChromeDriver' # Path to your ChromeDriver
os.environ['HEADLESS'] = 'True' # Change to 'False' if you like to visualise it
```

## Run
To run the program

```$ python maya-xtractor.py```

```CTRL+C``` to terminate the program during the runtime.

## Output
You can view the real-time progress of the script in your command line prompt.

The script will output a CSV file for every faculty.

![fsktm-generated](https://i.imgur.com/26NenwJ.png)

## Future Update
To update the script when there is new version.
```
$ cd MAYA-Xtractor/
$ git pull
```

