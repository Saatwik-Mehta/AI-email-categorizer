def ok_response(message=""):
    return {
            "statusCode": 200,
            "body": message,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
            },
            "isBase64Encoded": False
        }

def internal_server_error_response(message=""):
    return {
            "statusCode": 500,
            "body": message,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
            },
            "isBase64Encoded": False
        }