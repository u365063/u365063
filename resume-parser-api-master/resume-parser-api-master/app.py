from flask import Flask, request, send_file,jsonify
from flask_restful import Api, Resource
import os
import glob

from analyzer import analyzer
from fileParser import fileParser
from fileReader import fileReader

app = Flask(__name__)
api = Api(app)

# Specify the folder where uploaded files will be stored
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
DELETE_FOLDER = 'uploads'
app.config['DELETE_FOLDER'] = DELETE_FOLDER


class ResumeUpload(Resource):
    def post(self):
        # Check if the request contains files
        if 'files[]' not in request.files:
            return {'error': 'No files part'}, 400

        files = request.files.getlist('files[]')

        # Iterate over the uploaded files
        uploaded_files = []
        for file in files:
            # If the user does not select a file, the browser submits an empty part
            if file.filename == '':
                return {'error': 'No selected file'}, 400

            # Save the uploaded file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            uploaded_files.append(file_path)

        return {'message': 'Files uploaded successfully', 'file_paths': uploaded_files}


@app.route('/predict1', methods=['GET'])
def predict1():

    #parse the pdf file
    parsedResume = fileReader()

    #Run the model
    result = analyzer(parsedResume)
    print("++++++")
    print(result)
    print(result.to_json(path_or_buf = None, orient = 'records', date_format = 'epoch', double_precision = 10, force_ascii = True, date_unit = 'ms', default_handler = None))



    # Return the file for download
    return jsonify(result.to_json(path_or_buf = None, orient = 'records', date_format = 'epoch', double_precision = 10, force_ascii = True, date_unit = 'ms', default_handler = None))

@app.route('/predict', methods=['POST'])
def predict():

    data = request.get_json()

    threshold = data.get('threshold')
    noOfMatches = data.get('noOfMatches')
    inputPath = data.get('inputPath')
    context = data.get('context')

    #parse the pdf file
    parsedResume = fileReader(inputPath)

    #Run the model
    result = analyzer(parsedResume, context, noOfMatches, threshold)
    return jsonify(result.to_json(path_or_buf = None, orient = 'records', date_format = 'epoch', double_precision = 10, force_ascii = True, date_unit = 'ms', default_handler = None))

#dummy get call
@app.route('/getHello', methods=['GET'])
def getHello():
   print('Hello World')
   return "Hello World"


class ReportDownload(Resource):

    def get(self, filename):

        #parse the pdf file
        parsedResume = fileReader()

        #Run the model
        result = analyzer(parsedResume)

        # Construct the file path
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Check if the file exists
        if not os.path.exists(file_path):
            return {'error': 'File not found'}, 404

        # Return the file for download
        return result.to_json('ranking.json', orient='records')

class ExistingFileDelete(Resource):
    def delete(self):
        # Get the list of files in the folder
        folder_path = app.config['DELETE_FOLDER']
        files = os.listdir(folder_path)

        # Delete all files in the folder
        deleted_files = []
        for file in files:
            file_path = os.path.join(folder_path, file)
            os.remove(file_path)
            deleted_files.append(file)

        return {'message': 'All files deleted successfully', 'deleted_files': deleted_files}

# @app.route('/predict', methods=['POST'])
class Analyzed(Resource):
    def analyze(self):
        # Get the list of files in the folder
        analyzer()

        return {'analyzing'}

# Create API routes
api.add_resource(ResumeUpload, '/resumeUpload')
api.add_resource(ReportDownload, '/ReportDownload/<string:filename>')
api.add_resource(ExistingFileDelete, '/existingFileDelete')

if __name__ == '__main__':
    # Create the 'uploads' folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    app.run(debug=True)
