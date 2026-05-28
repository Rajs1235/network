import os
import sys
import json

from networksecurity.exception.exception import NetworkSecurityException

class S3Syncer:
    def _write_status(self, status_file_path, status, message=None):
        os.makedirs(os.path.dirname(status_file_path), exist_ok=True)
        with open(status_file_path, "w") as file_obj:
            json.dump({"status": status, "message": message}, file_obj)

    def sync_folder_to_s3(self, local_folder, bucket_url, status_file_path="artifact/network_security/last_training/sync_status.json"):
        try:
            command = f"aws s3 sync {local_folder} {bucket_url}"
            return_code = os.system(command)
            if return_code == 0:
                self._write_status(status_file_path, "completed", "pushed to s3 successfully")
            else:
                self._write_status(status_file_path, "failed", f"aws s3 sync exited with code {return_code}")
            return return_code == 0
        except Exception as e:
            self._write_status(status_file_path, "failed", str(e))
            raise NetworkSecurityException(e,sys)
    
    def sync_folder_from_s3(self, bucket_url, local_folder, status_file_path="artifact/network_security/last_training/sync_status.json"):
        try:
            command = f"aws s3 sync {bucket_url} {local_folder}"
            return_code = os.system(command)
            if return_code == 0:
                self._write_status(status_file_path, "completed", "pulled from s3 successfully")
            else:
                self._write_status(status_file_path, "failed", f"aws s3 sync exited with code {return_code}")
            return return_code == 0
        except Exception as e:
            self._write_status(status_file_path, "failed", str(e))
            raise NetworkSecurityException(e,sys)