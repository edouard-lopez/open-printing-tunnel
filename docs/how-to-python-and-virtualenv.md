### Python and virtualenv

### Requirement

* Python `3.5` ;
* (`Pip` should be [available](https://pip.pypa.io/en/stable/installing/#do-i-need-to-install-pip)).

### Installation

* [Create a Python virtual environement](https://docs.python.org/3.5/library/venv.html#creating-virtual-environments) ;

        python3.5 -m venv env
    
* [activate the virtual env](https://packaging.python.org/en/latest/installing/#creating-virtual-environments)

        source env/bin/activate
        
* install project's requirements:
    
        python3.5 -m pip install -r requirements-dev.txt   
