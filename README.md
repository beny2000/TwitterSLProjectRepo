# TwitterSLProjectRepo

## How to use this repo
 - After downloading and extracting the lastest release
 - Run `main.py` in termnial with arguments to start program, `python main.py *arguments*`
 - Program will then write the cleaned data and realted file to an output folder (see below)
 - `main.py` takes 1 required argument which is the input  directory, of the data to clean eg. `$ python main.py *input_folder*`
 - Optional flags include `-o, -l, -p, -na`
  - use `-o` to specify the output directory, if not specifyied one is created
  - use `-l` to specify locations file to use to filter data, if not specifyied default file is used (see `scripts`)
  - use `-p` to print a summary of the cleaned data to the screen, is off by default
  - use `-na` to turn off appending all cleaned data to master file of all cleaned data so far, is on by default
  
## Running on input folder to default output folder
- all files to clean must be in the same folder with only the files to clean inside
- works best when folder with files to clean is in the same location as main.py (see `input` folder)
- run with python command in terminal `main.py *input_folder*`

## Running on input folder to custom output folder
- all files to clean must be in the same folder with only the files to clean inside
- works best when folder with files to clean is in the same location as main.py (see `input` folder)
- run with python command in terminal `main.py *input_folder* -o *output_folder`
