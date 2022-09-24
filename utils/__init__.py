import uuid
import random
import string


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = "".join(random.choice(letters) for i in range(length))
    return result_str


def _generate_file_name(filename):
    extension = filename.split(".")[-1]
    return f"{uuid.uuid4()}.{extension}"


def generate_file_name(instance, filename):  # pylint: disable=unused-argument
    return f"add/assets/{_generate_file_name(filename)}"
