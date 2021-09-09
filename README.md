##  养老对赌刷题小组 第5轮

Github Pages 链接: https://feiteng-gcp.github.io/submission_history



# 目标

- 记录是否成功提交过群内规定题目
- 使用谷歌云电脑进行爬虫，记录首次提交时间
- 自动更新内容，记录等，解放双手！

# 使用方法

- `git clone https://github.com/feiteng-gcp/submission_history.git` 到本地
- 更改以下内容：

![image-20210908234133267](C:\Users\lifeiteng\AppData\Roaming\Typora\typora-user-images\image-20210908234133267.png)

- 在Google Cloud Platform (GCP) 平台:

  ```bash
  $ nohup python3 main.py &
  # 这里 nohup 是 no hang up 的意思，此时可以关闭平台，脚本依然会进行
  # & 是指不要在屏幕上输出，会在当前文件夹内把输出记录到一个nohup.out的文件内
  $ logout #进行断开
  
  # 再次登录GCP后，如何关闭这个脚本？
  $ ps -aux | grep python3 
  # 这里会找到 python3 在运行的脚本，找到PID
  $ kill -9 [对应的PID] #即可
  
  ```

  - 提前安装所需library: requests, json, pytz 等

- 在本地的git设置

  - git remote -v 查看remote url，此时应该与 `https://github.com/feiteng-gcp/submission_history` 相同

  - 更改你的remote origin url， 设置origin，同时写上access token

    格式为 https://USER_NAME:USER_TOKEN@gihub.com/USER_NAME/USER_PROJECT.git

    ```bash
    $ git remote -v
    origin  https://github.com/feiteng-gcp/submission_history.git (fetch)
    origin  https://github.com/feiteng-gcp/submission_history.git (push)
    
    $ git remote set-url origin https://feiteng-gcp:<例:abcd_Ud2LZYvsRGmGDehYfZQaRdJqr31cUz3>@github.com/feiteng-gcp/submission_history.git
    # 这样git push 或者 git push remote_URL 不需要登录
    ```

    

  - Access Token 获取方式:

    https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token

# 运行结果

会得到:

- assets/submission.json - 提交记录
- assets/last_modified.json - 本次运行的时间

这两份文件会在index.html 中用到



# 其他

- index.md - 这个文件不需要了，用markdown 的好处很容易制作，坏处是格式不很方便

- _config.yml - 与index.md 配套的theme，不需要了

- 爬虫间隔是60秒，用户Leetcode_ID，提交题目如果更改的话，需要手动更新



