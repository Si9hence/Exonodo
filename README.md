# Exonodo

The Exonodo program aims to collect the database information from ExoMol website and then register the database on Zenodo. The motivation and implementation could be checked in the associated report.
Exonodo provides 2 ways to call the program: python package and CLI.

# Installation

Exonodo could be used as an python package.  
It could be installed by the following script by running the command in the same directory of README.md

>git clone https://github.com/Si9hence/Exonodo  
>cd Exonodo  
>pip install .

Then Exonodo could be called as a normal package, there are two demos **collection_demo.ipynb** and **registration_demo.ipynb**.

# Composition
Functions has been split into 5 python files associated different features. They are stord in the folder ./Exonodo.
>**exomol_arc.py**: Collection  
>**exomol_val.py**: Validation  
>**zenodo_reg.py**: Registration  
>**exonodo.py**: command line interface  
>**zenodo_sup.py**: supplementary functions for debugging and post analysis  

Comments are left inside the functions to explain their usage. Each function could be called individually for customized requirement. A integrated method with configuation file is recommended for the collection and registration process.

# Configuration
The program accepts a configuration file to control the process of collection, registration.  
The configuration file is in json and accepts keyword as

>"option": "arc"(for collection) or "reg"(for registration),  
>"token": Zenodo access token, for registration only  
>"path_arc": "path to save(for collection) or load(for registration) json file",  
>"path_data": "file path to store related files for registration", for registration only
>"sub_set": the subset of Zenodo database to collection, for collection only

For collection:
```json
{
    "option": "arc",
    "path_arc": "./demo.json",
    "sub_set": {"cat":["metal hydrides"]}
}

```

For Registration:
```json
{
    "option": "reg",
    "token": "Mitwo0cwfer47Lvx51CTawELNJt9OYknMfP5WOvmNvJcYspgo9dGYDQiEFlL",
    "path_arc": "../sample/data_26Al1H.json",
    "path_data": "../sample/data/mnt/data/exomol/exomol3_data/"
}
```
use  
> Exonodo.load_config('path of config.json')

to call to load and run the configuration file.


# Demo

Three demo has been supplied to show the main usage of the program: 

>**Collection(integrated with validation)**  
>./sample/collection_demo.ipynb

>**Registration**  
>./sample/registration_demo.ipynb

Zenodo requires an account to view the registration form from the web interface. 
In registration demo, author's token has been provided the associated config_reg.json file to make the demo registration work. However, the unpublished registration form could only be accessed by the owner of the token/account.  
Thus, it is recommended for user who would like to try and check the unpublished registration form to create their own Zenodo account and token.
The account could be create on https://zenodo.org/signup/  
The access token is generated in Zenodo Settings > Applications > Personal access tokens. See also https://developers.zenodo.org/#rest-api  
Once you got your own token, just replace the "token" in the *./sample/config_reg.json* file with your own one. And you can view the unpublished registration after running exomol_reg.ipynb