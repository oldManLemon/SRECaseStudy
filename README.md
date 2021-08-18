# SRE Case Study

  

This script is written in Python 3.9.5

  

  

1. Create two files one named `elasticPass` and the other named `gitToken`

  

2.  `elasticPass` contains your elasticsearch instance password, `gitToken` contains your git token. Inside `main.py` are links to the documentation. Please place your elastic password in that file and your git token in the other.

  

  

**Github Token:** https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token

  

**Elastic Search Login Methods** https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch

  

3. It is assumed here you have an elasticsearch cloud instance. If this is not the case please refer to the elastic search documentation and in main change the connection strings.

  

4. Go to main.py and enter your ElasticSearch Cloud ID. You will find it located under Creds and Settings at the top.

  

5. Create a virtual enviroment and install the requirements.txt `pip install -r requirements.txt`

  

6. run `main.py`

  

## Reasoning

  

  

I have not packaged this script as it really only does one thing and is not required to be dynamic, or insofar as I can see from the slides. If this was required, more things could be simply added as variables and script parameters. The essence would stay essentially the same.

  

## Script Actions

Creates an index in an elasticSearch instance called `rockerstarlang_commits` where it will push all commits made to this [project](https://github.com/RockstarLang/rockstar). It only gathers currently the master branch, as it was not specified.

It uses the following map:

    
    'Commit Message': { 'type': 'text'},
    
    'Commit Date': { 'format': 'date_optional_time', 'type': 'date'},
    
    'Account Dead': { 'type': 'boolean'},
    
    'Author Email': {'type': 'text'},
    
    'Author Username': { 'type': 'text'},
    
    'Author Account Creation Date': { 'format': 'date_optional_time', 'type': 'date'},
    
  
I added the account dead as a parameter, as I was unable to retrieve the username and account creation time, in some cases. I assume the account has being deleted, but whatever the reason, githubs api is unable to source that information. So I have acknowledged it in the results and moved on. 

The basics results of attempting to add data to the elasticSearch is printed to the console. I have it set this way as I can't stand it when there is no feed back while running the script. 
