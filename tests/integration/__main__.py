from argparse import ArgumentParser
from .concurrency import run_concurrency_test
from .deadlocks import run_deadlocks_test

# TODO: test that checks environment variables are used for critical stuff
#       e.g. JWT does not use default secret


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
    cmds = {"test": _run_test_cmd}
    cmds[cmd](kwargs)


if __name__ == "__main__":
    main_parser = ArgumentParser()
    main_subparsers = main_parser.add_subparsers(dest="main_cmd")

    test_parser = main_subparsers.add_parser("test")
    _add_test_args(parser=test_parser)

    main(vars(main_parser.parse_args()))
    print("done")
