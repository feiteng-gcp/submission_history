import requests, json, time, collections, os, subprocess, collections
from datetime import datetime
import pytz

import Crawlers, IO_Helper, Logger

if __name__ == '__main__':
    USERNAME_FILE = 'Username_LeetcodeID.json'
    CRAWLED_FILE = 'Crawled.json'
    # Submission_File = 'index.md'
    SUBMISSION_RECORD = 'assets/submission.json'
    LAST_MODIFIED_RECORD = 'assets/last_modified.json'

    CSRF_TOKEN = IO_Helper.readToken()
    Crawlers.updateMetaData(CSRF_TOKEN)
    USERNAME_DICT = IO_Helper.loadJSON(USERNAME_FILE, {})
    # print(USERNAME_DICT)
    CRAWLED_RESULT = IO_Helper.loadJSON(CRAWLED_FILE, collections.defaultdict(dict))
    
    QUESTION_DICT = IO_Helper.loadTargetQuestion_metaData()
    QUESTION_TITLE_ID = IO_Helper.createTitleIDMap(QUESTION_DICT)

    rootLogger = Logger.getLogger("root")


    while True:
        submissionResult = Crawlers.getSubmissions(USERNAME_DICT,CSRF_TOKEN,
            CRAWLED_RESULT, QUESTION_DICT, QUESTION_TITLE_ID)

        # print(submissionResult)
        IO_Helper.writeJSON(CRAWLED_FILE, submissionResult)

        # writeToFile(USERNAME_DICT, QUESTION_DICT, submissionResult, Submission_File)
        # IO_Helper.writeRecord(USERNAME_DICT, QUESTION_DICT, submissionResult, SUBMISSION_RECORD)
        IO_Helper.writeToJSON_(USERNAME_DICT, QUESTION_DICT, submissionResult, SUBMISSION_RECORD)
        IO_Helper.updateFile(LAST_MODIFIED_RECORD)

        # commit_and_pushtoGithub(Submission_File)
        IO_Helper.commit_and_pushtoGithub(SUBMISSION_RECORD)
        IO_Helper.commit_and_pushtoGithub(LAST_MODIFIED_RECORD)

        rootLogger.info('Waiting 60 seconds for next crawl..')
        time.sleep(60)

