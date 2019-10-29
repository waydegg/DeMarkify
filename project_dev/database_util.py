import boto3
from config import *
import json


def delete_file(file_name):
    """Deletes the specified file"""

    if os.path.exists(str(file_name)):
        os.remove(str(file_name))
    else:
        RuntimeError(f"{file_name} doesn't exist")



def s3_transfer(bucket_name, file_name, direction, folder_path=None):
    """
    Transfers a file between AWS s3 and the client. 

    Parameters:
    bucket_name - (str) An aws s3 storage bucket
    file_name - (str) the path to the file
    direction - (str) "upload" or "download"
    folder_path - (str) path to file_name
    """
    s3 = boto3.resource("s3")
    fn = file_name.split("/")[-1]
    file_type = file_name.split(".",1)[1]

    if str(direction).lower() == "upload":
        s3.Bucket(name=str(bucket_name)).upload_file(
            Filename=str(file_name),
            Key=str(fn))
    
    elif str(direction).lower() == "download":
        s3.Object(bucket_name=str(bucket_name), key=str(folder_path)).download_file(file_name)
        
        if file_type.lower() == "csv":
            df = pd.DataFrame(os.getcwd(f"{os.getcwd()}/{file_name}"))
            delete_file(file_name)
            return df

        elif file_type.lower() == "json":
            with open(f"{os.getcwd()}/{file_name}") as f:
                dictionary = json.load(f)
                delete_file(file_name)
                return dictionary
        
        else:
            RuntimeError(f"Direction can only be 'upload' or 'download'. You entered {direction}")
    

def get_credentials():
    """Returns a dictionary of personal credentials"""

    bucket = "my-credentials-waydegg"
    filename = "credentials.json"
    creds = s3_transfer(
        bucket_name=bucket,
        file_name=filename,
        direction="download",
        folder_path=filename)
    return creds