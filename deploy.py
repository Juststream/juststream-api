import argparse
import subprocess

STACK_NAME = "juststream-api"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="JustStreamAPI")
    parser.add_argument("-e", "--env", choices=["dev", "prod"], required=True)
    parser.add_argument("-b", "--build", type=bool, default=True)

    args = parser.parse_args()
    env = args.env
    build = args.build

    if build:
        build_args = ["sam", "build", "--use-container", "-t", "fastapi_service.yml"]
        subprocess.call(build_args)

    package_args = [
        "sam",
        "package",
        "--template-file",
        ".aws-sam/build/template.yaml",
        "--output-template-file",
        "output-template.yaml",
        "--s3-bucket",
        f"{STACK_NAME}-{env}-builds",
    ]
    subprocess.call(package_args)

    deploy_args = [
        "sam",
        "deploy",
        "--stack-name",
        f"{STACK_NAME}-{env}",
        "--s3-bucket",
        f"{STACK_NAME}-{env}-builds",
        "--capabilities",
        "CAPABILITY_IAM",
        "--parameter-overrides",
        f"Environment={env}",
    ]
    subprocess.call(deploy_args)
