# Cool Visualizer
## Park and Josh Jam Time
### To run:
* source venv/bin/activate
* python3 main.py -s [save_path_format] -d [should_display_bool] -g [should_generate_bool]
* examples:
  * generate and save: python3 main.py -s frames/frames -g 1
  * display from save: python3 main.py -s frames/frames -d 1


#### Impicit Runtime Logic
* -s, if no filepath specified, files not saved
* -d, will display generated frames only if -g is set to true, othewise it will read files in from filepath specified as -s

### To install:
* python3 -m venv venv
* source venv/bin/activate
* pip3 install -r requirements.txt


## TODO:
* switch debugging to using `logging`
