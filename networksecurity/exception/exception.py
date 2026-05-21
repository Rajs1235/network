import sys
from networksecurity.logging import logger
class NetworkSecurityException(Exception):
    def __init__(self,error_message,error_detail:sys):
        self.error_message=error_message
        _,_,exc_tb=error_detail.exc_info()
        self.file_name=exc_tb.tb_frame.f_code.co_filename
        self.line_number=exc_tb.tb_lineno

    def __str__(self):
        return f"Error occurred in file: {self.file_name} at line number: {self.line_number} with error message: {self.error_message}"
        
if __name__=="__main__":
    try:
        logger.logging.info("try block started")
        a=1/0
        print("will not be printed")
    except Exception as e:
        
        raise NetworkSecurityException(e,sys)