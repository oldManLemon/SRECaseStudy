from github import Github
from elasticsearch import Elasticsearch


#*Creds and Settings
#Git Token
tokenFile = open('gitToken','r')
token = tokenFile.read()
tokenFile.close()
#Elastic Instance Password
elasticFile = open('elasticPass','r')
elPass = elasticFile.read()
elasticFile.close()

#ElasticSearch cloud ID
cloudID = "githubRock:ZWFzdHVzMi5henVyZS5lbGFzdGljLWNsb3VkLmNvbTo5MjQzJGYzOWJhNzdkODQxNDQ1MmQ5MjZhMGNjMWMwYWU4MjI1JGQwYzZhMzI3YjQ3YzQ0NDU5OWY0OTA3ZjMyODk5NTYy"

#Github Setup
#* https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token
github = Github(token)
repo = github.get_repo("RockstarLang/rockstar")

#Elastic Setup 
#! This setup is only useful if you have a cloud ElasticSearch instance. Otherwise see documenation https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch
es = Elasticsearch(
cloud_id=cloudID,
http_auth=("elastic", elPass),)

#Github connection, is pretty garunteed to work. 
try:
    commits = repo.get_commits()
except:
    exit()

def testConn(connection):
    if es.ping():
        return True
    else:
        return False

if testConn(es):
    #Mapping
    commit_mapping = {
        'mappings': {
            'properties': {
                    'Commit Message': { 'type': 'text'},
                    'Commit Date': { 'format': 'date_optional_time', 'type': 'date'},
                    'Account Dead': { 'type': 'boolean'},
                    'Author Email': {'type': 'text'},
                    'Author Username': { 'type': 'text'},
                    'Author Account Creation Date': { 'format': 'date_optional_time', 'type': 'date'},
            }
        }
    }
    print("mapping")
    #*Make our index if not already made
    res = es.indices.create(index = 'rockerstarlang_commits', body=commit_mapping, ignore=400)
    print(res)
    #Get Commits
    commits = repo.get_commits()
    for commit in commits:
        #Commit Message
        commitMsg = commit.commit.message
        commitSha = commit.commit.sha
        #Catch dead accounts
        try:
            #Created
            commitUsrCreated = commit.author.created_at
            # #Just Username
            commitUserLoginName = commit.author.login
            #must be lowercase
            accountDead = "false"
        except AttributeError:
            # print("Cannot determine account, most likely no longer exists")
            commitUserLoginName = commit.committer
            accountDead = "true"
        
        # #date of Commit
        commitDate = commit.commit.author.date
        # #Committers Email
        commitersEmail = commit.commit.author.email
        data = {
             'Commit Date': commitDate,
            'Commit Message':commitMsg,
            'Commit Author':commitUserLoginName,
            'Author Email':commitersEmail,
            'Author Account Creation Date':commitUsrCreated,
            'Account Dead': accountDead,
        }
        try:
            res =  es.create(index='rockerstarlang_commits',body=data,id=commitSha,refresh=True,ignore=[409,400])
            print(res)
        except:
            print("Failed to Commit")



   


else:
    print("No Connection to elastic search server")

