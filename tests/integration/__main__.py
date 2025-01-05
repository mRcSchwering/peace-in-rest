from argparse import ArgumentParser
from .concurrency import run_concurrency_test
from .deadlocks import run_deadlocks_test
from .sample_data import add_sample_data


def _run_sample_data_cmd(kwargs: dict):
    add_sample_data(**kwargs)


def _add_sample_data_args(parser: ArgumentParser):
    parser.add_argument(
        "--app-url", default="http://app:80", help="default: %(default)s"
    )
    parser.add_argument("--n-users", default=3, type=int, help="default: %(default)s")


def _run_test_cmd(kwargs: dict):
    cmd = kwargs.pop("test_cmd")
    cmds = {"concurrency": run_concurrency_test, "deadlocks": run_deadlocks_test}
    cmds[cmd](**kwargs)


def _add_test_args(parser: ArgumentParser):
    parser.add_argument(
        "--app-url", default="http://app:80", help="default: %(default)s"
    )
    subparsers = parser.add_subparsers(dest="test_cmd")
    subparsers.add_parser("concurrency", help="run concurrency tests")
    subparsers.add_parser("deadlocks", help="run deadlocks tests")


def main(kwargs: dict):
    cmd = kwargs.pop("main_cmd")
    cmds = {"test": _run_test_cmd, "sample_data": _run_sample_data_cmd}
    cmds[cmd](kwargs)


if __name__ == "__main__":
    main_parser = ArgumentParser()
    main_subparsers = main_parser.add_subparsers(dest="main_cmd")

    test_parser = main_subparsers.add_parser("test")
    _add_test_args(parser=test_parser)

    sample_data_parser = main_subparsers.add_parser("sample_data")
    _add_sample_data_args(parser=sample_data_parser)

    main(vars(main_parser.parse_args()))
    print("done")
