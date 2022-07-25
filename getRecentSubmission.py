import requests, json, time, collections, os, subprocess, collections
from datetime import datetime
import pytz

def getSubmissions(USERNAMES, CSRF_Token, submission_result, Question_Dict, Title_ID):
    # submission_result = collections.defaultdict(dict)
    crawl_successful = True
    try:
        for username in USERNAMES:
            getSubmission(username, CSRF_Token, submission_result, Question_Dict, Title_ID)
    except Exception as error:
        crawl_successful = False
        print(error)
        pass
    if crawl_successful: print('Successfully crawled submission..')
    # print(submission_result)
    return submission_result

def getSubmission(USERNAME, CSRF_Token, submission_result, Question_Dict, Title_ID):
    print('Getting submission for %s..' % (USERNAME))
    if USERNAME not in submission_result: submission_result[USERNAME] = {}
    # print(submission_result)
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




def readToken():
    with open('CSRF_TOKEN', 'r') as f:
        return f.readline()

def writeToFile(UserNameDict, Question_Dict, submission, fileName):

    curTime = datetime.now(pytz.timezone('America/New_York'))
    cur_time = curTime.strftime('%Y %b %d %H:%M %p %z')
    # timer keeps updating first row in file, even if no one has new submissions
    update_time = '# File updated on..' + cur_time
    
    banner = update_time + '\n\n'

    flag = True
    try:
        f = open(fileName, 'w')

        banner += '|Question ID|Question Link|'
        for name in submission:
            banner += UserNameDict[name] + '|'
        # print(banner)
        f.write(banner + '\n')
        banner = '|-|-|'
        for name in submission: banner += '-|'
        f.write(banner + '\n')
        for targ_question in Question_Dict:
            # print(targ_question)
            question_slug = Question_Dict[targ_question]['question_slug']
            questionLink = 'https://leetcode.com/problems/' + question_slug
            banner = '|' + targ_question + '|[' + question_slug + '](' + questionLink + ')|'
            for name in submission:
                if targ_question in submission[name]:
                    banner += submission[name][targ_question] + '|'
                else:
                    banner += '#n/a|'
            banner += '\n'
            f.write(banner)
        f.close()
    except Exception as err:
        flag = False
        print(err)
    if flag: print('Successfully written to file..')

def writeToJSON(UserNameDict, Question_Dict, submission, fileName):

    curTime = datetime.now(pytz.timezone('America/New_York'))
    cur_time = curTime.strftime('%Y %b %d %H:%M %p %z')
    # timer keeps updating first row in file, even if no one has new submissions
    update_time = '# File updated on..' + cur_time
    
    banner = update_time + '\n\n'

    flag = True
    content = [] #collections.OrderedDict()

    banner += '|Question ID|Question Link|'
    nameList = ['Question ID', 'Question Link']
    for name in submission:
        # banner += UserNameDict[name] + '|'
        nameList.append(UserNameDict[name])
    content.append(nameList)

    for targ_question in Question_Dict:
        contentList = [targ_question]
        # print(targ_question)
        question_slug = Question_Dict[targ_question]['question_slug']
        questionLink = 'https://leetcode.com/problems/' + question_slug
        question_href = '<a href="' + questionLink + '">' + question_slug + "</a>"
        contentList.append(question_href)

        # banner = '|' + targ_question + '|[' + question_slug + '](' + questionLink + ')|'
        for name in submission:
            if targ_question in submission[name]:
                # banner += submission[name][targ_question] + '|'
                contentList.append(submission[name][targ_question])
            else:
                # banner += '#n/a|'
                contentList.append('#n/a')
        
        # content[targ_question] = contentList
        # f.close()
        content.append(contentList)
    try:
        with open(fileName, 'w') as f:
            json.dump(content, f)
    except Exception as err:
        flag = False
        print(err)
    if flag: print('Successfully written to file..')

def commit_and_pushtoGithub(file):

    print('commiting file.. %s' % (file))
    curTime = datetime.now(pytz.timezone('America/New_York'))
    cur_time = curTime.strftime('%Y %b %d %H:%M %p %z')
    commit_message = 'auto committed on .. ' + cur_time
    print('Trying to push..')

    push_successful = True
    try:

        subprocess.call(['git', 'add', file])
        subprocess.call(['git', 'commit' ,'-m', commit_message])
    # set your remote origin to https://<USERNAME>:<TOKEN>@github.com/USERNAME/PROJECT.git
    # or use subprocess.call(['git push', MYREPO])
    # where MYREPO = https://<USERNAME>:<TOKEN>@github.com/USERNAME/PROJECT.git
        subprocess.call(['git' ,'push'])
    except Exception as error:
        push_successful = False
        print(error)
        pass

    if push_successful:
        print("Successful..")

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

def loadFile(fileName, defaultOutput):
    dict = defaultOutput
    file_backup = 'backup/' + fileName
    # try:
    f = open(fileName, 'r')
    dict = json.load(f)
    writeFile(dict, file_backup)
    f.close()
    # except Exception: pass
    return dict

def writeFile(data, fileName):
    # if not os.path.exists(fileName): os.path.mkdir(fileName)
    with open(fileName, 'w') as f:
        json.dump(data, f)

def loadQuestion():
    question_list = []
    with open('QuestionList', 'r') as f:
        question_list.append(f.readline())
    return question_list

def loadTargetQuestion_metaData():
    targetQuestions = collections.OrderedDict()
    f = open('metadata.json', 'r')
    metaData = json.load(f)
    f.close
    with open('QuestionList', 'r') as f:
        line = f.readline()
        while line:
            frontend_question_id = line.strip('\n')
            try:
                targetQuestions[frontend_question_id] = {
                    'question_slug' : metaData[frontend_question_id]['question_slug'],
                    'question_title' :  metaData[frontend_question_id]['question_title']
                }
            except Exception as err:
                print(err)
                pass
            line = f.readline()
    return targetQuestions

def createTitleIDMap(questionMap):
    title = {}
    for frontend_id in questionMap:
        question_title = questionMap[frontend_id]['question_title']
        title[question_title] = frontend_id
    return title

def updateFile(file):
    curTime = datetime.now(pytz.timezone('America/New_York'))
    cur_time = curTime.strftime('%Y %b %d %H:%M %p %z')
    commit_message = cur_time
    f = open(file, 'w')
    f.write(commit_message)
    f.close()

if __name__ == '__main__':
    UserName_File = 'Username_LeetcodeID.json'
    Crawled_File = 'Crawled.json'
    Submission_File = 'index.md'
    Submission_Record = 'assets/submission.json'
    Last_Modified_Record = 'assets/last_modified.json'

    CSRF_Token = readToken()
    updateMetaData(CSRF_Token)
    USERNAME_DICT = loadFile(UserName_File, {})
    # print(USERNAME_DICT)
    CRAWLED_RESULT = loadFile(Crawled_File, collections.defaultdict(dict))
    
    Question_Dict = loadTargetQuestion_metaData()
    Question_title_ID = createTitleIDMap(Question_Dict)


    while True:
        submissionResult = getSubmissions(USERNAME_DICT,CSRF_Token,
            CRAWLED_RESULT, Question_Dict, Question_title_ID)

        # print(submissionResult)
        writeFile(submissionResult, Crawled_File)

        # writeToFile(USERNAME_DICT, Question_Dict, submissionResult, Submission_File)
        writeToJSON(USERNAME_DICT, Question_Dict, submissionResult, Submission_Record)
        updateFile(Last_Modified_Record)

        # commit_and_pushtoGithub(Submission_File)
        commit_and_pushtoGithub(Submission_Record)
        commit_and_pushtoGithub(Last_Modified_Record)

        print('waiting...')
        time.sleep(60)


