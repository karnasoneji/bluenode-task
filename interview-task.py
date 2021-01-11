import json
import constant
from helper_functions import read_json_file
from helper_functions import write_log
from helper_functions import process_standard_json_data
from helper_functions import read_input_file
from helper_functions import get_standard_sub_sections
from helper_functions import get_data_type
from helper_functions import validate_length
from helper_functions import validate_data_type
from helper_functions import write_summary
from helper_functions import process_error_code_json
from helper_functions import get_error_message
from helper_functions import prepare_error_message
from helper_functions import delete_file
from helper_functions import write_report
from helper_functions import identify_error_type


#Deleting previously created Log file, Summary File, Report File
delete_file(constant.LOG_FILE_PATH)
delete_file(constant.SUMMARY_FILE_PATH)
delete_file(constant.REPORT_FILE_PATH )

write_log("### The script has started the execution. ###")
print("The script has started the execution.\n")

#reading standard_definition.json file	
response=read_json_file(constant.STANDARD_DEFINITION_JSON_FILE_PATH)

#if the return type is False,there was an error reading the file, else it will return a string
if(response == False):
	write_log('### Problem reading Standard Definition file. Please check if the file name and path is correct in the constants file. ###')
	print("Couldn't read Standard Definition File.Please check if the file name and path is correct in the constants file.\n")
	exit()

# we receive the list object containing the standard definition
standard_definition_list = process_standard_json_data(response)


#reading input_data.txt file
input_lines_list = read_input_file(constant.INPUT_FILE_PATH)

#if the return type is False,there was an error reading the file.
if(input_lines_list == False):
	write_log('### Problem reading Input file. Please check if the file name and path is correct in the constants file. ###')
	print("Couldn't read Input File.Please check if the file name and path is correct in the constants file.\n")
	exit()


#read error_codes.json file and getting raw json string
error_codes_json_data = read_json_file(constant.ERROR_CODE_JSON_FILE_PATH)

#if the return type is False,there was an error reading the file.
if(error_codes_json_data == False):
	write_log('### Problem reading Error Codes Json file. Please check if the file name and path is correct in the constants file. Current file: interview-task.py ###')
	print("Couldn't read Error Codes Json File.Please check if the file name and path is correct in the constants file.\n")
	exit()

#We receive the list object containing error codes from raw json data
error_codes_list = process_error_code_json(error_codes_json_data)


# Below for loop is to iterate through each line of input file
for single_input_line in input_lines_list:											
	
	
	#it will return all the sub-sections for a specific section from standard_definition.json. For example, it will return all sub-sections under section L1 from standard definition json file
	
	standard_rule_list=get_standard_sub_sections(standard_definition_list,single_input_line[0])	
	
	# Test Case : For example, if input file has L10 but standard definition json file does not have that element, it will write a log and continue to next line of input file.
	if not standard_rule_list:
		write_log("### Section LX in the input file does not match with the section in the standard definition file. ###".replace('LX',single_input_line[0]));
		continue
	
	
	# For example, in above parent iteration we come across "L2" section in the input file. The below loop will iterate through all the sub-sections under "L2" from standard definition json file. For example, in the below iteration, we will compare L2's sub-sections from standard definition against L2's sub-sections of input data.
	
	for standard_rule_list_index in range (0,len(standard_rule_list)):
		
		flag_data_type_validation = None			#Initializing as None.
		flag_field_length_validation = None			#Initializing as None.
	
		#Below four variable are being used to write into summary file and report file.
		standard_definition_sub_section_key = standard_rule_list[standard_rule_list_index]['key'] # 'key': 'L11'
		standard_definition_sub_section_data_type = standard_rule_list[standard_rule_list_index]['data_type']  # 'data_type': 'digits'
		standard_definition_sub_section_max_length = standard_rule_list[standard_rule_list_index]['max_length'] #'max_length': 1
		standard_definition_sub_section_section = standard_rule_list[standard_rule_list_index]['section'] #'section': 'L1'
		
		# We are checking if the sub-section exists in input data or it is missing		
		try:
			input_line_sub_section= single_input_line[standard_rule_list_index+1] # getting the sub-sections using index
			
		except IndexError:
			
			#IndexError means sub-section is missing in input file which means it is 'E05' error.
			
			# we write the error in the summary file
			write_summary(prepare_error_message(get_error_message(error_codes_list , "E05"),standard_definition_sub_section_key,standard_definition_sub_section_section,standard_definition_sub_section_data_type,str(standard_definition_sub_section_max_length)))
			
			# we write the error in the report file
			write_report([standard_definition_sub_section_section,standard_definition_sub_section_key,'',standard_definition_sub_section_data_type,'',standard_definition_sub_section_max_length,'E05'])
			continue
		
		#If the sub-section of input is empty, we'll set length and data-type validation to false. It fails all criteria(both data-type and length).
		if not single_input_line[standard_rule_list_index+1]:
				flag_data_type_validation = False				#setting validation to False, this means data-type validation for that input sub-section has failed
				flag_field_length_validation = False			#setting validation to False, this means length validation for that input sub-section has failed
		else:
				#length validation : matching the length of each sub-section of input with the length of respective sub-section of standard definition
				flag_field_length_validation = validate_length(int(standard_definition_sub_section_max_length),len(single_input_line[standard_rule_list_index+1]))	
				
				#data-type validation : matching the data-type of each sub-section of input with the data-type of respective sub-section of standard definition
				flag_data_type_validation = validate_data_type(standard_definition_sub_section_data_type,get_data_type(single_input_line[standard_rule_list_index+1]))	
		
		
		#given data-type of the input sub-section
		given_data_type_input_sub_section=get_data_type(single_input_line[standard_rule_list_index+1])
		
		#given length of the input sub-section
		given_length_input_sub_section=str(len(single_input_line[standard_rule_list_index+1]))
		
		#Identify the error-type (E02 , E03 , E01, E04) 
		error_type = identify_error_type(flag_field_length_validation,flag_data_type_validation)
	
		#If error_type is not empty, we'll write the error to summary and report file.
		if(error_type):
			
			# we write the error in the summary file
			write_summary(prepare_error_message(get_error_message(error_codes_list , error_type),standard_definition_sub_section_key,standard_definition_sub_section_section,standard_definition_sub_section_data_type,str(standard_definition_sub_section_max_length)))
			
			# we write the error in the report file
			write_report([standard_definition_sub_section_section,standard_definition_sub_section_key,given_data_type_input_sub_section,standard_definition_sub_section_data_type,given_length_input_sub_section,standard_definition_sub_section_max_length,error_type])
		
	
	# Writing a new line character after each section has been processed
	write_summary();


write_log('### The script has completed the execution. ###')	
print("The script has completed the execution.\n\nFor more details, please check summary.txt , report.csv and log.txt located in the same folder as this executable.")	