from botocore.exceptions import ClientError
from tenacity import retry_if_exception


TRANSIENT_AWS_ERROR_CODES = {
    "Throttling",
    "ThrottlingException",
    "ServiceUnavailable",
    "RequestTimeout",
    "InternalError",
    "ProvisionedThroughputExceededException",
    "TooManyRequestsException",
}


def is_transient_aws_error(exc: BaseException) -> bool:

    if isinstance(exc, ClientError):
        code = exc.response.get("Error", {}).get("Code", "")
        return code in TRANSIENT_AWS_ERROR_CODES

    if isinstance(exc, (ConnectionError, TimeoutError)):
        return True

    return False


retry_on_transient_aws = retry_if_exception(is_transient_aws_error)
