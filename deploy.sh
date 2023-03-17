#!/bin/bash

STACK_NAME="juststream-api"

while getopts "e:b:" opt; do
  case ${opt} in
  e)
    env=$OPTARG
    ;;
  b)
    build=$OPTARG
    ;;
  \?)
    echo "Invalid option: -$OPTARG" 1>&2
    exit 1
    ;;
  :)
    echo "Option -$OPTARG requires an argument." 1>&2
    exit 1
    ;;
  esac
done

if [[ -z "${env}" ]]; then
  echo "Error: -e is a required option." >&2
  exit 1
fi

if [[ "${build}" == "true" ]]; then
  aws ssm get-parameters \
    --name="/juststream/${env}" \
    --with-decryption | jq -r '.Parameters | map("\(.Value)") | .[]' | cut -d'/' -f3- > requirements_layer/${env}.env
  sam build \
    --use-container \
    --container-env-var ENV=${env} \
    -t fastapi_service.yaml
fi

sam package \
  --template-file .aws-sam/build/template.yaml \
  --output-template-file output-template.yaml \
  --s3-bucket ${STACK_NAME}-${env}-builds

sam deploy \
  --stack-name ${STACK_NAME}-${env} \
  --s3-bucket ${STACK_NAME}-${env}-builds \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides Environment=${env}
