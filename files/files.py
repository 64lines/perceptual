class FileManager():
    def __init__(self, file_path):
        self.file_path = file_path

    def get_file_lines(self, path):
        list_file_result = []
        file_data = open(path, "rb")
        list_file = file_data.readlines()

        for line in list_file:
            list_file_result.append(line.strip())

        file_data.close()
        return list_file_result

    def get_entries(self):
        return self.get_file_lines(self.file_path)