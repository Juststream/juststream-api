sam build --profile mate --template-file media_convert_trigger/media_convert_trigger.yml
sam package --template-file .aws-sam/build/template.yaml --output-template-file .aws-sam/build/package.yaml --profile mate --s3-bucket stream-cropper --region us-east-1
sam deploy --template-file .aws-sam/build/package.yaml --profile mate --stack-name media-convert-trigger --region us-east-1 --capabilities CAPABILITY_IAM
