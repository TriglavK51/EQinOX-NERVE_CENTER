from tools._common import meta, run_local_tool

NAME = "pdf"


def run(input_data: dict) -> dict:
    return run_local_tool(NAME, input_data)


def health() -> dict:
    return meta(NAME)


def get_meta() -> dict:
    return meta(NAME)
