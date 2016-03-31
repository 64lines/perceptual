#!/usr/bin/python

# Coverts a file to a list using its lines.
def get_file_lines(path):
    list_file_result = []
    file_data = open(path, "rb")
    list_file = file_data.readlines()

    for line in list_file:
        list_file_result.append(line.replace("\n", ""))

    file_data.close()
    return list_file_result
