import os
START_SEQUENCE = "\033[93m"
END_SEQUENCE = "\033[0m"
def log(text):
    if os.getenv("DEBUG") == "True":
        print(f" {START_SEQUENCE}{text}{END_SEQUENCE}")
