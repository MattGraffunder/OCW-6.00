# 6.00 Problem Set 5
# RSS Feed Filter
#
# Name: Matt Graffunder
# Collaborators: None 
# Time Spent: 1:30

import feedparser
import string
import time
from project_util import translate_html
from news_gui import Popup

#-----------------------------------------------------------------------
#
# Problem Set 5

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        summary = translate_html(entry.summary)
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        newsStory = NewsStory(guid, title, subject, summary, link)
        ret.append(newsStory)
    return ret

#======================
# Part 1
# Data structure design
#======================

# Problem 1

class NewsStory(object):
    def __init__(self, guid, title, subject, summary, link):
        self.guid = guid
        self.title = title
        self.subject = subject
        self.summary = summary
        self.link = link

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_subject(self):
        return self.subject

    def get_summary(self):
        return self.summary

    def get_link(self):
        return self.link

#======================
# Part 2
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

# Whole Word Triggers
# Problems 2-5

class WordTrigger(Trigger):
    def __init__(self, word):
        self.word = word.lower()
        
    def is_word_in(self, text):
        #LowerCase the text
        searchText = text.lower()
        
        #Replace puctuation with spaces
        for p in string.punctuation:
            searchText = searchText.replace(p, ' ')
            
        #Split on Spaces
        searchWords = searchText.split()
        
        #Inspect Each Word
        for searchWord in searchWords:
            if searchWord == self.word:
                return True

        #Didn't find a matching word
        return False

class TitleTrigger(WordTrigger):    
    def evaluate(self, story):
        return self.is_word_in(story.get_title())
    
class SubjectTrigger(WordTrigger): 
    def evaluate(self, story):
        return self.is_word_in(story.get_subject())
    
class SummaryTrigger(WordTrigger):   
    def evaluate(self, story):
        return self.is_word_in(story.get_summary())

# Composite Triggers
# Problems 6-8

class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.t = trigger

    def evaluate(self, story):
        return not self.t.evaluate(story)
    
# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.t1 = trigger1
        self.t2 = trigger2

    def evaluate(self, story):
        return self.t1.evaluate(story) and self.t2.evaluate(story)
    
# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.t1 = trigger1
        self.t2 = trigger2

    def evaluate(self, story):
        return self.t1.evaluate(story) or self.t2.evaluate(story)

# Phrase Trigger
# Question 9

class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase

    def evaluate(self, story):
        return self.phrase in story.get_subject() or self.phrase in story.get_title() or self.phrase in story.get_summary()

#======================
# Part 3
# Filtering
#======================

def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory-s.
    Returns only those stories for whom
    a trigger in triggerlist fires.
    """
    releventStories = []

    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                releventStories.append(story)
                break
    
    return releventStories

#======================
# Part 4
# User-Specified Triggers
#======================

def readTriggerConfig(filename):
    """
    Returns a list of trigger objects
    that correspond to the rules set
    in the file filename
    """
    # Here's some code that we give you
    # to read in the file and eliminate
    # blank lines and comments
    triggerfile = open(filename, "r")
    all = [ line.rstrip() for line in triggerfile.readlines() ]
    lines = []
    for line in all:
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)

    # TODO: Problem 11
    # 'lines' has a list of lines you need to parse
    # Build a set of triggers from it and
    # return the appropriate ones

    activeTriggers = []
    triggers = {}

    for line in lines:
        # Parse Line
        args = line.split()
        #If type of trigger, create trigger
        if args[0] == "ADD":
            #Get all the triggers after the word add
            for t in args[1:]:
                activeTriggers.append(triggers[t])
        elif args[1] == "TITLE":
            triggers[args[0]] = TitleTrigger(args[2])            
        elif args[1] == "SUBJECT":
            triggers[args[0]] = SubjectTrigger(args[2])
        elif args[1] == "SUMMARY":
            triggers[args[0]] = SummaryTrigger(args[2])
        elif args[1] == "NOT":
            triggers[args[0]] = NotTrigger(triggers[args[2]])
        elif args[1] == "AND":
            triggers[args[0]] = AndTrigger(triggers[args[2]], triggers[args[3]])
        elif args[1] == "OR":
            triggers[args[0]] = OrTrigger(triggers[args[2]], triggers[args[3]])
        elif args[1] == "PHRASE":
            #Phrase can be an arbitrary length, need to rebuild phrase from string            
            triggers[args[0]] = PhraseTrigger(" ".join(args[2:]))

    return activeTriggers
    
import thread

def main_thread(p):
    # A sample trigger list - you'll replace
    # this with something more configurable in Problem 11
##    t1 = SubjectTrigger("Trump")
##    t2 = SummaryTrigger("Mall")
##    t3 = PhraseTrigger("West Virginia")
##    t4 = OrTrigger(t2, t3)
##    triggerlist = [t1, t4]
    
    # TODO: Problem 11
    # After implementing readTriggerConfig, uncomment this line 
    triggerlist = readTriggerConfig("triggers.txt")
    guidShown = []
    
    while True:
        print "Polling..."

        # Get stories from Google's Top Stories RSS news feed
        stories = process("http://news.google.com/?output=rss")
        # Get stories from Yahoo's Top Stories RSS news feed
        stories.extend(process("http://rss.news.yahoo.com/rss/topstories"))

        # Only select stories we're interested in
        stories = filter_stories(stories, triggerlist)
    
        # Don't print a story if we have already printed it before
        newstories = []
        for story in stories:
            if story.get_guid() not in guidShown:
                newstories.append(story)
        
        for story in newstories:
            guidShown.append(story.get_guid())
            p.newWindow(story)

        print "Sleeping..."
        time.sleep(SLEEPTIME)

SLEEPTIME = 60 #seconds -- how often we poll
if __name__ == '__main__':
    p = Popup()
    thread.start_new_thread(main_thread, (p,))
    p.start()

