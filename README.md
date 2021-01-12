
## Instructions:

The solution is built on python and was run and tested on "3.8.1" version.

As the scale of the task was very small, i have kept the project structure very simple. As per the complexity of the project, it can go more sophisticated by packaging the code into separate modules and even unit tests can be divided into multiple folders based on the context.


## How to run the program:

Navigate to the root directory of the project, and type the following command on the terminal.

	```
	py interview-task.py
	
	```

The complete code is divided into three files:

1. interview-task.py
2. helper_functions.py (it contains helper functions)
3. constant.py (it contains file paths)


The program uses three files and those are located in the "files" folder in root directory.:

1. "input_file.txt" 
2. "standard_definition.json" 
3. "error_codes.json" 

After the script completes it's execution, it will create "summary.txt" and "report.csv" in "Report and Summary" folder located in the root folder.

## How to run Unit Tests: 

Navigate to the root directory of the project, and type following command on the terminal.

	```
	
	py test_cases.py
	
	```

## Logging

The program has a logging capability. It logs all kinds of states and errors including:

1. When an input file has a section which does not exist in the standard_definition.json. For example. input file has section "L10" but it does not exist in the standard_definition.json. then, it will log an error.
2. Error reading error_codes.json or standard_definition.json or input_file.txt will be logged.
3. If the required keys like 'key','sub_sections', 'section', 'message-template' etc does not exist in the error_codes.json or standard_definition.json , then it will log an error.
4. If the json format of error_codes.json or standard_definition.json is invalid, then it will log the error.

	
## Thank you very much for the opportunity to work on this task! For any questions:

Please reach me at karna.soneji@smu.ca