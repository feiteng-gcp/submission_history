import requests, json, time, collections, os, subprocess, collections
from datetime import datetime
import pytz

def getSubmissions(USERNAMES, CSRF_Token, submission_result, Question_Dict, Title_ID):
    crawl_successful = True
    try:
        for username in USERNAMES:
            getSubmission(username, CSRF_Token, submission_result, Question_Dict, Title_ID)
    except Exception as error:
        crawl_successful = False
        print(error)
        pass
    if crawl_successful: print('Successfully crawled submission..')
    return submission_result

def getSubmission(USERNAME, CSRF_Token, submission_result, Question_Dict, Title_ID):
    print('Getting submission for %s..' % (USERNAME))
    if USERNAME not in submission_result: submission_result[USERNAME] = {}
    COOKIE = 'csrftoken=' + CSRF_Token
    X_CSRFTOKEN = CSRF_Token
    url = 'https://leetcode.com/graphql'
    headers = {
            'referer': 'https://leetcode.com/accounts/login/',
            'cookie' : COOKIE,
            'x-csrftoken' : X_CSRFTOKEN
        }
    data = {
        "operationName":"getRecentSubmissionList",
        "variables":'{"username":"' + USERNAME + '"}',
        "query":"query getRecentSubmissionList($username: String!, $limit: Int) {\n  recentSubmissionList(username: $username, limit: $limit) {\n    title\n    titleSlug\n    timestamp\n    statusDisplay\n    lang\n    __typename\n  }\n  languageList {\n    id\n    name\n    verboseName\n    __typename\n  }\n}\n"
    }

    try:
        resptext = json.loads(requests.post(url, headers = headers, data = data).text)
        # print(resptext)
        submissionList = resptext['data']['recentSubmissionList']

        for each_submission in submissionList:
            questionTitle = each_submission['title']
            if questionTitle in Title_ID:
                submissionStatus = each_submission['statusDisplay']
                if submissionStatus == 'Accepted':
                    timeStamp = each_submission['timestamp']
                    submissionTime = datetime.fromtimestamp((int)(timeStamp), pytz.timezone('America/New_York'))
                    submissionTime = submissionTime.strftime('%Y %b %d %H:%M %p')
                    if questionTitle in submission_result[USERNAME]: continue
                    submission_result[USERNAME][Title_ID[questionTitle]] = submissionTime
    # print(submission_result)
    except Exception as error:
        print("Error when crawling..%s" % (USERNAME))
        print(Exception)

def updateMetaData(CSRF_Token):
    print('Updating meta data..')
    import requests, json
    url = 'https://leetcode.com/api/problems/algorithms/'

    COOKIE = 'csrftoken=' + CSRF_Token
    headers = {
        'referer': 'https://leetcode.com/accounts/login/',
        'cookie' : COOKIE,
        'x-csrftoken' : CSRF_Token
    }

    resp = json.loads(requests.get(url, headers = headers).text)

    data = {}
    for item in resp['stat_status_pairs']:
        map = item['stat']
        question_id = map['question_id']
        question__title = map['question__title']
        frontend_question_id = map['frontend_question_id']
        question_slug  = map['question__title_slug']
        data[str(frontend_question_id)] = {
            'question_id' : question_id,
            'question_title': question__title,
            'question_slug' : question_slug
        }

    with open('metadata.json', 'w') as file:
        json.dump(data, file)        