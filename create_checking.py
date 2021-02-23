from worker import create_time, post_message


def lambda_handler(event, context):
    date    = create_time()
    content = f"{date} 기상 기상! 얼른 스레드에 미션을 남겨주세요 :)"
    post_message(content = content)