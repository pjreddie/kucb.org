import feedparser

def update_entries():
    print "updating!!"
    feed = feedparser.parse("http://feeds.aprn.org/aprn-news")
    for entry in feed.entries[:5]:
        entries.append({"title":entry.title, "link":entry.link})
