import requests
from os.path import expanduser, isdir, exists
from os import remove
import zipfile


file_id = '1-JI__pcY2IST6mCV9JanOWmeD6h8wYME'
home = expanduser("~")
zip_dst = home + '/data.zip'
unzip_dst = home + '/.facebot'

def download_file_from_google_drive(id, destination):
    '''
    '''
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    '''
    '''
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    '''
    '''
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

def unzip_and_delete(zip_path, dir_path):
    '''
    unzips data.zip to .facebot dir, deletes data.zip
    '''
    with zipfile.ZipFile(zip_path, 'r') as file:
        file.extractall(dir_path)
    remove(zip_path)

def check(path):
    '''
    checks if directory .facebot exists
    '''
    if exists(path) and isdir(path):
        return True
    return False

def main():
    '''
    '''
    if not check(unzip_dst):
        print('Fetching files...')
        download_file_from_google_drive(file_id, zip_dst)
        unzip_and_delete(zip_dst, unzip_dst)
        print('Complete')
    return home

if __name__ == '__main__':
    main()

