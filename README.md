# PlayfulPredictions

### 1. Configure the virtual environment
You can create the Windows virtual environment by running commands as in Linux following this [guide](https://linuxhint.com/activate-virtualenv-windows/). However, I will summarise the steps:

- Install Python if you don't already have it on your computer.
- Install command pip if you don't already have it on your computer.
- Install virtualenv with `pip install virtualenv` in a cmd console
- Create Project Directory: 1º `mkdir project-dir `2º `cd project-dir`

- Create virtualenv for Project Directory: `virtualenv venvironment`

My recommendation before activating the virtual environment is to move to the Visual Studio Code console and work on it.
So before activating the virtual environment:

-  Open Visual Studio Code and access the directory we created in previous steps.
- Once inside, we check that the virtual environment created is the one we have created. 
- To be able to run the environment in our Visual Studio Code console, we must execute this command `Set-ExecutionPolicy Unrestricted -Scope Process`, also every time we want to activate the environment.
- Finally we activate the virtual environment: `venvironment\Scripts\activate`

If you want to use the command console and perform the process there you only need to activate the virtual environment: `venvironment\Scripts\activate`

### 2. Clone the repository
- Clone PlayfulPredictions in the repository by executing `https://github.com/pedlopruz/PlayfulPredictions.git` in the directory or import the zip.

### 3. Install requirements
- Install project dependencies by running `pip install -r requirements.txt` in the project's root folder.

### 4. Migrate the app and populate the database
In the root folder of the project, run:
- `python manage.py makemigrations`
- `python manage.py migrate`

### 5. Run the app
In the root folder of the project, run:
- `python manage.py runserver`



