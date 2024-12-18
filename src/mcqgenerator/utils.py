import os
import PyPDF2
import json
import traceback

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader=PyPDF2.PdfReader(file)
            text=""
            for page in pdf_reader.pages:
                text+=page.extract_text()
            return text
        
        except Exception as e:
            raise Exception("error reading the PDF file")
        
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    
    else:
        raise Exception("unsupported file format, only PDF and text file supported")
    

def get_table_data(quiz_str):
    try:
        print("Debug - Input quiz_str type:", type(quiz_str))  # Debug print
        print("Debug - Input quiz_str:", quiz_str[:200])  # Print first 200 chars
        
        # Handle both string and dictionary inputs
        if isinstance(quiz_str, str):
            quiz_dict = json.loads(quiz_str)
        else:
            quiz_dict = quiz_str
            
        print("Debug - Parsed quiz_dict:", quiz_dict)  # Debug print
        #convert the quiz from a str to dict
        
        quiz_table_data=[]

        #iterate over the quiz dictionary and extract the required information
        for key, value in quiz_dict.items():
            mcq=value["mcq"]
            # Create the options string by actually using the values from options
            options_list = []
            for opt, opt_value in value["options"].items():
                option_str = f"{opt}-> {opt_value}"
                options_list.append(option_str)
            
            # Join all options with the separator
            options = " || ".join(options_list)
            correct = value["correct"]
            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})

        return quiz_table_data
    
    except Exception as e:
        print("Error in get_table_data:", str(e))  # Debug print
        traceback.print_exception(type(e), e, e.__traceback__)
        return None
    

