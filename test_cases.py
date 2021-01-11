import unittest
import json
import helper_functions


class TestCases(unittest.TestCase):
	
	def test_get_data_type(self):
		self.assertEqual('digits',helper_functions.get_data_type('123'))
		self.assertEqual('word_characters',helper_functions.get_data_type('A1234'))
		self.assertEqual('others',helper_functions.get_data_type('.'))
		self.assertEqual('others',helper_functions.get_data_type(''))
	
	
	def test_identify_error_code(self):
		
		length_validation = True
		data_type_validation = False
		
		self.assertEqual('E02',helper_functions.identify_error_type(length_validation,data_type_validation))
	
		length_validation = False
		data_type_validation = True

		self.assertEqual('E03',helper_functions.identify_error_type(length_validation,data_type_validation))

		length_validation = True
		data_type_validation = True
		
		self.assertEqual('E01',helper_functions.identify_error_type(length_validation,data_type_validation))

		length_validation = False
		data_type_validation = False

		self.assertEqual('E04',helper_functions.identify_error_type(length_validation,data_type_validation))
		
	
	def test_get_sub_sections_standard_definition(self):
		
		standard_definition_processed_raw_json = '[{"key": "L11", "data_type": "digits", "max_length": 1, "section": "L1"}, {"key": "L12", "data_type": "word_characters", "max_length": 3, "section": "L1"}, {"key": "L13", "data_type": "word_characters", "max_length": 2, "section": "L1"}, {"key": "L21", "data_type": "word_characters", "max_length": 1, "section": "L2"}, {"key": "L22", "data_type": "digits", "max_length": 1, "section": "L2"}, {"key": "L23", "data_type": "word_characters", "max_length": 2, "section": "L2"}, {"key": "L31", "data_type": "word_characters", "max_length": 1, "section": "L3"}, {"key": "L41", "data_type": "word_characters", "max_length": 1, "section": "L4"}, {"key": "L42", "data_type": "digits", "max_length": 6, "section": "L4"}]'
		
		standard_definition_list = json.loads(standard_definition_processed_raw_json )
		
		result_raw_json = '[{"key": "L11", "data_type": "digits", "max_length": 1, "section": "L1"}, {"key": "L12", "data_type": "word_characters", "max_length": 3, "section": "L1"}, {"key": "L13", "data_type": "word_characters", "max_length": 2, "section": "L1"}]'
		
		result_list = json.loads(result_raw_json)
		
		self.assertEqual(result_list,helper_functions.get_standard_sub_sections(standard_definition_list,'L1'))
		
		
	def test_process_standard_definition_json_data(self):
		
		standard_definition_json_raw='[{"key":"L1","sub_sections":[{"key":"L11","data_type":"digits","max_length":1},{"key":"L12","data_type":"word_characters","max_length":3},{"key":"L13","data_type":"word_characters","max_length":2}]},{"key":"L2","sub_sections":[{"key":"L21","data_type":"word_characters","max_length":1},{"key":"L22","data_type":"digits","max_length":1},{"key":"L23","data_type":"word_characters","max_length":2}]},{"key":"L3","sub_sections":[{"key":"L31","data_type":"word_characters","max_length":1}]},{"key":"L4","sub_sections":[{"key":"L41","data_type":"word_characters","max_length":1},{"key":"L42","data_type":"digits","max_length":6}]}]'
		
		standard_definition_processed_json = '[{"key": "L11", "data_type": "digits", "max_length": 1, "section": "L1"}, {"key": "L12", "data_type": "word_characters", "max_length": 3, "section": "L1"}, {"key": "L13", "data_type": "word_characters", "max_length": 2, "section": "L1"}, {"key": "L21", "data_type": "word_characters", "max_length": 1, "section": "L2"}, {"key": "L22", "data_type": "digits", "max_length": 1, "section": "L2"}, {"key": "L23", "data_type": "word_characters", "max_length": 2, "section": "L2"}, {"key": "L31", "data_type": "word_characters", "max_length": 1, "section": "L3"}, {"key": "L41", "data_type": "word_characters", "max_length": 1, "section": "L4"}, {"key": "L42", "data_type": "digits", "max_length": 6, "section": "L4"}]'	
		
		self.assertEqual(json.loads(standard_definition_processed_json),helper_functions.process_standard_json_data(standard_definition_json_raw)) 
		
		

if __name__ == '__main__':
		unittest.main()
	