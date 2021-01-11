import json
import constant
import re
import os
import csv


# it returns the data-type of the field. Result cab be "digits" or "word_characters" or "others"
def get_data_type(input):
	if (re.match(r"^[0-9]+$",input)):
		return "digits";
	elif (re.match(r"^[0-9a-zA-Z ]+$",input)):
		return "word_characters"
	else:
		return "others"

# it validates the length of the field
def validate_length(expected_length,input_field_length):
	if(input_field_length <= expected_length):
		return True
	else:
		return False

#it validates the data-type of the field
def validate_data_type(expected_data_type,input_field_data_type):
	if(expected_data_type == input_field_data_type):
		return True
	else:
		return False
		
#it returns the sub-sections for a specific section from standard definition	
def get_standard_sub_sections(standard_definition_list,section):
	#the below code will return the list with matched section
	return [item for item in standard_definition_list if item["section"] == section]

# it returns raw json data in string format
def read_json_file(file):
	
	err_flag = False
	
	try:
		with open(file, 'r') as file_handle:
			return file_handle.read()	#data in json string
	except Exception:
			err_flag = True
	finally:
			if(err_flag):
				return False;
				  

# it writes summary file				  
def write_summary(message=''):
	try:
		with open(constant.SUMMARY_FILE_PATH, 'a') as file_handle:
			file_handle.write(message+"\n")
	except Exception:
		print("Exception has occured and could not write to summary file. Please check if the folder has write permission or change the path in constants file.")
		pass

#it writes report file		
def write_report(data):
	try:
		#we are setting the flag below in order to know if to write header or not
		if os.path.exists(constant.REPORT_FILE_PATH):
			flag_header = False
		else:
			flag_header = True
		with open(constant.REPORT_FILE_PATH, 'a') as file_handle:
			csv_report_writer = csv.writer(file_handle, delimiter=',')
			if(flag_header):
				csv_report_writer.writerow(['Section','Sub-Section','Given DataType','Expected DataType','Given Length','Expected MaxLength','Error Code'])
			
			#if the given length is zero, we are setting given length and given data-type column as empty
			if(data[4] == '0'):
				data[2] = data[4] = ''
			csv_report_writer.writerow(data)
	except Exception as error:
		print(error)
		print("Exception has occured and could not write to report file. Please check if the folder has write permission or change the path in constants file.")
		pass		
		

#it writes log file
def write_log(message):
	try:
		with open(constant.LOG_FILE_PATH, 'a') as file_handle:
			file_handle.write("\n"+message)
	except Exception:
		print("Exception has occured and could not write to log file. Please check if the folder has write permission or change the path in constants file.")
		pass
		

# it process raw standard definition json data and convert into list for further use	
def process_standard_json_data(input_data_string):
	
	standard_definition_list = []
	
	try:
		raw_json_input=json.loads(input_data_string)	
		for list_item in raw_json_input:
				for object in list_item['sub_sections']:
					object['section']=list_item['key']
					standard_definition_list.append(object)
			
	except KeyError:
		write_log("### Error parsing standard definition json file. 'key' / 'sub_sections' / 'section' doesn't exist ###")
				
	except Exception:
		write_log("### Invalid json format for standard definition file.###")
			
	return standard_definition_list 

# it reads the input file and returns the list of sub-sections for each line	
def read_input_file(file):
	err_flag = False
	sections_subsections_list = []
	try:
		with open(file, 'r') as file_handle:
			for line in file_handle:										#reading each line through loop
				sections_subsections_list.append(line.strip().split("&"));	# striping new-line character and spliting into subsections separated by &
		return sections_subsections_list;
	except Exception:
			err_flag = True
	finally:
			if(err_flag):
				return False;
	
# it returns the error message
def get_error_message(error_codes_list,error_code):
	
	try:
		
		matches = [error_code_object for error_code_object in error_codes_list if error_code_object["code"] == error_code]	
		
		if(matches):
			return matches[0]["message_template"]
		else:
			return ""
	
	except KeyError:
		write_log("### Error parsing error codes json file. field 'message_template' doesn't exist ###")
		return ""
		
# it returns the prepared error message 		
def prepare_error_message(raw_message,key='',section='',data_type='',max_length=''):
	return raw_message.replace('LXY',key).replace('{data_type}',data_type).replace('{max_length}',str(max_length)).replace('LX',section)

# it returns list from the raw json data of error file
def process_error_code_json(raw_error_code_json):
	try:
		return json.loads(raw_error_code_json)							# put here try / catch for invalid json string
	except:
		write_log("### Invalid json format for error code file. ###")
		return []
	

#it deletes the file
def delete_file(file):
	if os.path.exists(file):
	  os.remove(file)

#identifying error type	  
def identify_error_type(flag_field_length_validation,flag_data_type_validation):
				
		# Below condition will check, if the length matches but data-type does not match
		if (flag_field_length_validation == True and flag_data_type_validation == False):
			
			return 'E02'
			
		# Below condition will check, if the length does not match but data-type match			
		if (flag_field_length_validation == False and flag_data_type_validation == True):
			
			return 'E03'
		
		#Below condition will check if both length and data-type matches
		if (flag_field_length_validation == True and flag_data_type_validation == True):
			
			return 'E01'
		
		#Below condition will check if both length and data-type does not match
		if (flag_field_length_validation == False and flag_data_type_validation == False):
			
			return 'E04'