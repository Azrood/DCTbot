from utils.secret import reddit_secret, reddit_useragent, reddit_client_id
import praw
import random



def reddit_nsfw():
    reddit = praw.Reddit(client_id=reddit_client_id,
                     client_secret=reddit_secret,
                     user_agent=reddit_useragent)


    subreddit_list = ["nsfw","RealGirls","NSFW_GIF","holdthemoan","BustyPetite","cumsluts","LegalTeens","PetiteGoneWild","nsfw_gifs","GirlsFinishingTheJob","AsiansGoneWild","Amateur","rule34","BiggerThanYouThought","porninfifteenseconds","collegesluts","TittyDrop","ass","pawg","hentai","milf","HappyEmbarrassedGirls","OnOff","porn","LipsThatGrip","Blowjobs","celebnsfw","GWCouples","nsfwhardcore","dirtysmall","Boobies","WatchItForThePlot","trashyboners","homemadexxx","pussy","nsfwcosplay","juicyasians","gonewildcurvy","palegirls","girlsinyogapants","asstastic","curvy","freeuse","GodPussy","StraightGirlsPlaying","workgonewild","60fpsporn","anal","NSFW_Snapchat","JizzedToThis","AsianHotties","lesbians","FestivalSluts","TinyTits","thick","wifesharing","grool","gwcumsluts","pornvids","bodyperfection","GirlswithGlasses","rearpussy","TooCuteForPorn","18_19","Hotwife","bigasses","BreedingMaterial","quiver","Stacked","BigBoobsGW","ginger","redheads","SexInFrontOfOthers","whenitgoesin","gettingherselfoff","boobbounce","creampies","porn_gifs","Hotchickswithtattoos","theratio","SheLikesItRough","tightdresses","burstingout","amateurcumsluts","facedownassup","altgonewild","WouldYouFuckMyWife","hugeboobs","CuteLittleButts","deepthroat","O_Faces","Upskirt","HENTAI_GIF","HugeDickTinyChick","fitgirls""suicidegirls","RandomActsOfBlowJob"]
    sub = random.choice(subreddit_list)
    subreddit = reddit.subreddit(sub)

    hop = random.choice(["hot","top","rising","new"])
    if hop == "new" :
        for submission in subreddit.new(limit=10):
            if submission.url.endswith(('.jpg','.png')):
                return submission.url
    elif hop == "top" :
        for submission in subreddit.top(limit=10):
            if submission.url.endswith(('.jpg','.png')):
                return submission.url
    elif hop == "rising" :
        for submission in subreddit.rising(limit=10):
            if submission.url.endswith(('.jpg','.png')):
                return submission.url
    elif hop == "hot" :
        for submission in subreddit.hot(limit=10):
            if submission.url.endswith(('.jpg','.png')):
                return submission.url
