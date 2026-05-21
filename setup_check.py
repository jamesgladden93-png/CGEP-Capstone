import json
import platform
import shutil
import subprocess
import sys


EXPECTED_PYTHON_MAJOR = 3
EXPECTED_PYTHON_MINOR = 14
EXPECTED_AWS_CLI_MAJOR = 2


def print_result(name, passed, detail):
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}: {detail}")


def check_python_version():
    version = sys.version_info
    passed = (
        version.major == EXPECTED_PYTHON_MAJOR
        and version.minor == EXPECTED_PYTHON_MINOR
    )
    expected = f"{EXPECTED_PYTHON_MAJOR}.{EXPECTED_PYTHON_MINOR}.x"
    actual = platform.python_version()
    print_result("Python version", passed, f"expected {expected}, found {actual}")
    print(f"        executable: {sys.executable}")
    return passed


def check_pip():
    try:
        import pip

        print_result("pip", True, f"found {pip.__version__}")
        return True
    except ImportError:
        print_result("pip", False, "not installed for this Python interpreter")
        return False


def check_aws_cli():
    aws_path = shutil.which("aws")
    if not aws_path:
        print_result("AWS CLI", False, "aws command was not found on PATH")
        return False

    version_command = subprocess.run(
        ["aws", "--version"],
        capture_output=True,
        text=True,
        check=False,
    )
    version_output = (version_command.stdout or version_command.stderr).strip()
    passed = version_output.startswith(f"aws-cli/{EXPECTED_AWS_CLI_MAJOR}.")
    print_result(
        "AWS CLI",
        passed,
        f"expected v{EXPECTED_AWS_CLI_MAJOR}.x, found {version_output}",
    )
    print(f"        executable: {aws_path}")
    return passed


def check_aws_identity():
    aws_path = shutil.which("aws")
    if not aws_path:
        print_result("AWS identity", False, "skipped because AWS CLI is not installed")
        return False

    identity_command = subprocess.run(
        ["aws", "sts", "get-caller-identity", "--output", "json"],
        capture_output=True,
        text=True,
        check=False,
    )
    if identity_command.returncode != 0:
        error = (identity_command.stderr or identity_command.stdout).strip()
        print_result("AWS identity", False, error or "unable to read caller identity")
        return False

    identity = json.loads(identity_command.stdout)
    account = identity.get("Account", "unknown")
    arn = identity.get("Arn", "unknown")
    print_result("AWS identity", True, f"account {account}, arn {arn}")
    return True


def main():
    print("Setup check")
    print("===========")
    print(f"Platform: {platform.platform()}")
    print()

    checks = [
        check_python_version(),
        check_pip(),
        check_aws_cli(),
        check_aws_identity(),
    ]

    print()
    if all(checks):
        print("Setup check complete: all checks passed.")
        sys.exit(0)

    print("Setup check complete: one or more checks failed.")
    sys.exit(1)


if __name__ == "__main__":
    main()
