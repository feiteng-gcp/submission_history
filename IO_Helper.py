import requests, json, time, collections, os, subprocess, collections
from datetime import datetime
import pytz



def readToken():
    with open('CSRF_TOKEN', 'r') as f:
        return f.readline()

def loadJSON(fileName, defaultOutput):
    dict = defaultOutput
    file_backup = 'backup/' + fileName
    # try:
    f = open(fileName, 'r')
    dict = json.load(f)
    writeFile(dict, file_backup)
    f.close()
    # except Exception: pass
    return dict
    
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
    # update_time = '# File updated on..' + cur_time
    
    # banner = update_time + '\n\n'

    flag = True
    content = [] #collections.OrderedDict()

    # banner += '|Question ID|Question Link|'
    nameList = ['Question ID', 'Question Link']
    for name in submission:
        # banner += UserNameDict[name] + '|'
        nameList.append(UserNameDict[name])
    

    submission_count = {}
    content_pt2 = []

    for targ_question in Question_Dict:
        contentList = [targ_question]
        # print(targ_question)
        question_slug = Question_Dict[targ_question]['question_slug']
        questionLink = 'https://leetcode.com/problems/' + question_slug
        question_href = '<a href="' + questionLink + '">' + question_slug + "</a>"
        contentList.append(question_href)

        # banner = '|' + targ_question + '|[' + question_slug + '](' + questionLink + ')|'
        for name in submission:
            if name not in submission_count: submission_count[name] = 0
            if targ_question in submission[name]:
                # banner += submission[name][targ_question] + '|'
                contentList.append(submission[name][targ_question])    
                submission_count[name] += 1
            else:
                # banner += '#n/a|'
                contentList.append('#n/a')
        
        # content[targ_question] = contentList
        # f.close()
        content_pt2.append(contentList)
    # try:
    submission_record_count = ['Submission Count', '#']
    for name in submission:
        submission_record_count.append(str(submission_count[name]))
    content.append(submission_record_count)
    content.append(nameList)
    for each_content in content_pt2:
        content.append(each_content)
    with open(fileName, 'w') as f:
        json.dump(content, f)
    # except Exception as err:
    #     flag = False
    #     print(err)
    if flag: print('Successfully written to file..' + fileName)


def writeFile(data, fileName):
    # if not os.path.exists(fileName): os.path.mkdir(fileName)
    with open(fileName, 'w') as f:
        json.dump(data, f)    




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

def commit_and_pushtoGithub(file):

    print('commiting file.. %s' % (file))
    curTime = datetime.now(pytz.timezone('America/New_York'))
    cur_time = curTime.strftime('%Y %b %d %H:%M %p %z')
    commit_message = 'auto committed on .. ' + cur_time
    print('Starting to push..')

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