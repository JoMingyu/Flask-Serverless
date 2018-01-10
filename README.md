# Flask-Serverless
This is how I structure my serverless flask applications using AWS.

기존에 작성했던 <a href="https://github.com/JoMingyu/Flask-Large-Application-Example">Flask Large Application Example</a>을 기반으로, Flask를 이용한 serverless API의 구조에 대해 고민한 Flask serverless 어플리케이션 예제입니다.

## Preparations
### AWS credentials
### AWS S3

## Technical Stack
### Zappa
파이썬으로 serverless API를 AWS API Gateway와 Lambda 기반 환경에 배치하기 위한, Django와 Flask와의 접착성이 매우 좋은 프레임워크입니다. Python WSGI 어플리케이션을 배포하기 때문에 코드의 변경 없이 Django, Flask와 같은 WSGI 어플리케이션을 그대로 배포할 수 있고, Zappa Client가 프로젝트를 압축하여 Lambda에 배포하고 API Gateway에서 Lambda를 사용할 수 있게 알아서 세팅해 줍니다.

<a href="https://github.com/Miserlou/Zappa">Zappa repository</a>

#### Zappa client의 deploy 과정(예측)
server.py라는 모듈에 아래의 코드가 작성되어 있다고 칩시다.
~~~
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'hello', 200
~~~
위처럼 간단한 echo 서버를 만들고, zappa_settings.json에 app 객체의 위치를 명시합니다.
~~~
{
    "dev": {
        "app_function": "server.app",
        "profile_name": "planb"
        // aws_region, s3_bucket등 기타 세팅들도 있지만 생략합니다.
    }
}
~~~
이후 터미널에서 'zappa deploy' 명령을 입력하면,
1. zappa_settings.json에 명시된 profile_name의 AWS crendential에 포함된 Access Key ID/Secret Access Key를 이용해 ZappaLambdaExecutionRole이라는 IAM Role을 생성합니다.
2. S3의 HeadBucket과 CreateBucket operation을 이용해 bucket을 실제로 생성합니다.
3. Lambda의 CreateFunction operation을 이용해 app 객체의 라우팅을 기반으로 lambda function을 생성합니다.
4. 그리고 이 리소스들을 AWS cloudformation에서 관리합니다.
5. 생성된 lambda function과 app 객체의 url rule을 이용해 API Gateway의 UpdateRestApi operation으로 AWS API Gateway를 생성합니다.

따라서 Zappa deploy 과정에선 AWS 서비스에 관한 5개의 권한(IAM, S3, Lambda, Cloudformation, API Gateway)이 필요합니다.

### AWS Lambda
항상 서버를 올려 두고 관리하는 AWS EC2와 대조되게, API가 요청을 처리한 만큼(사용한 컴퓨팅 시간에 대해서만) 비용이 부과되는 구조의 AWS 서비스입니다. AWS Lambda 웹 콘솔에 들어가면 Lambda function을 직접 만들 수 있다. Node.js, Python 등 여러가지 런타임을 지원합니다. 만들어진 Lambda function은 이 함수를 실행시킬 '이벤트'가 필요한데, 이를 위해 이벤트 소스 혹은 API 엔드포인트를 만들어야 합니다.
1. AWS의 다른 이벤트에서 특정한 조건의 이벤트가 발생했을 때 Lambda function을 실행할 수 있도록 연결할 수도 있고(EC2에 설정한 가격 알림을 연결해서 Slack으로 알림을 주는 등)
2. URL을 정의해서 해당 엔드포인트로 요청을 보내면 이벤트를 발생시키도록 설정할 수 있습니다. AWS 내의 서비스를 이벤트 소스로 연결하는 방식이 아니라면 대부분 이 방식을 이용할 것이고, 반갑게도 HTTP 요청을 이용하므로 외부 서비스나 어플리케이션과 연동해서 사용할 수 있습니다.

따라서 Lambda 기반의 serverless API를 구현한다고 치면 API Gateway와 함께 묶어줘야 합니다.

### AWS API Gateway
이는 API 서비스의 입구를 담당해 주는 서비스로 보통의 API 서버에서 라우팅하는 것과 비슷합니다. API Gateway를 다양하게 사용할 수 있겠지만 여기서는 Lambda function에 연결하는 목적으로만 사용합니다.
