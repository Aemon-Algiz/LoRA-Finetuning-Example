import os
import json
from bs4 import BeautifulSoup
import requests

def process_xml_files(root_dir):
    data = []
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.xml'):
                filepath = subdir + os.sep + file
                with open(filepath, 'r', encoding='utf-8') as xml_file:
                    soup = BeautifulSoup(xml_file, 'xml')
                    qapairs = soup.find_all('QAPair')
                    for qapair in qapairs:
                        question = qapair.find('Question')
                        answer = qapair.find('Answer')
                        # Both question and answer exist and are non-empty
                        if question and question.text.strip() and answer and answer.text.strip():
                            # Clean up the text by replacing tabs, newlines, and multiple spaces with a single space
                            clean_question = ' '.join(question.text.split())
                            clean_answer = ' '.join(answer.text.split())
                            data.append({
                                "instruction" : "You are a medical expert and you will answer questions related to medical inquiries.",
                                "input": clean_question,
                                "output": clean_answer,
                            })
    return data

def write_json_file(data, output_file):
    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=4)

root_dir = 'D:\\Example Datasets\\Structured'  # Change this to the root directory of your XML files
output_file = 'output.json'  # The file where you want to store your JSON data

data = process_xml_files(root_dir)
write_json_file(data, output_file)