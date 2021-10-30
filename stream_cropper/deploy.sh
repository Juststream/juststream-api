sam build --profile mate --template-file stream_cropper/stream-cropper.yml -m stream_cropper/requirements.txt
sam package --template-file .aws-sam/build/template.yaml --output-template-file .aws-sam/build/package.yaml --profile mate --s3-bucket stream-cropper --region us-east-1
sam deploy --template-file .aws-sam/build/package.yaml --profile mate --stack-name stream-cropper --region us-east-1 --capabilities CAPABILITY_IAM
