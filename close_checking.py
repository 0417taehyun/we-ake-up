from worker import get_penalty_members, get_mission_person, post_message


def lambda_handler(event, context):
    penalty_content = get_penalty_members()
    mission_content = get_mission_person()
    content = penalty_content + "\n\n" + mission_content
    post_message(content = content)