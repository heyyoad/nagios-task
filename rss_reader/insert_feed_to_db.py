#!/usr/bin/python

# -*- coding: utf-8 -*-
import feedparser
from datetime import datetime
import psycopg2
import sys

RSS_URL = "http://www.ynet.co.il/Integration/StoryRss1854.xml"
CONN_STRING = "dbname='rss_feeds' user='pg_user' host='localhost' password='justforfun'"

def get_last_rss_feed():
    try:
        ynet_feed = feedparser.parse(RSS_URL)
        #print ynet_feed.entries[0]#DEBUG
        #print ynet_feed.entries[0]['published']
        # print ynet_feed.entries[0]['title']
        # print ynet_feed.entries[0]['link']
        return ynet_feed.entries[0]
    except:
        print 'Could not parse URL (%s)' % RSS_URL
        sys.exit(1)

def insert_new_feed(publish_date, title, link):
    con = None
    #datetime_object = datetime.strptime(publish_date, '%b %d %Y %I:%M%p')
    try:
        con = psycopg2.connect(CONN_STRING)
        cur = con.cursor()
        cur.execute("INSERT INTO feeds VALUES (%s, %s, %s)", (publish_date, title, link))
        # cur.execute("INSERT INTO Cars VALUES(1,'Audi',52642)")
        con.commit()


    except psycopg2.DatabaseError, e:

        if con:
            con.rollback()

        print 'Error %s' % e
        sys.exit(1)


    finally:

        if con:
            con.close()

def get_all_feeds():
    con = None
    try:
        conn = psycopg2.connect(CONN_STRING)
        cur = conn.cursor()
        cur.execute("SELECT * FROM feeds")

        rows = cur.fetchall()

        for row in rows:
            print row
    except psycopg2.DatabaseError as e:
        print "I am unable to connect to the database: " + str(e)
        sys.exit(1)

    finally:
        if con:
            con.close()


def main():
     latest_feed = get_last_rss_feed()
     insert_new_feed(latest_feed['published'], latest_feed['title'], latest_feed['link'])
     #get_all_feeds() #DEBUG

if __name__ == '__main__':
    main()
