import os


def get_config(variable_name, default_value):
    value = os.getenv(variable_name, default_value)
    print(f"Variable {variable_name} set to {value}")
    return value
