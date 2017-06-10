#!/usr/bin/python

# -*- coding: utf-8 -*-
import feedparser
import sys
import argparse
import datetime

OUTPUT_FILE="/usr/local/nagios/libexec/Output.txt"

def parse_last_rss_feed(url):
    try:
        ynet_feed = feedparser.parse(url)
        #print ynet_feed.entries[0] #DEBUG
        return ynet_feed.entries[0]
    except:
        output = 'Could not parse URL (%s)' % url
        exitcritical(output)


# Exit Status
def exitok(output):
    print 'OK - %s' % output
    sys.exit(0)


def exitwarning(output):
    print 'WARNING - %s' % output
    sys.exit(1)


def exitcritical(output):
    print 'CRITICAL - %s' % output
    sys.exit(2)


def exitunknown(output):
    sys.exit(3)

def main():

    # Set up our arguments
    parser = argparse.ArgumentParser(description="nagios script to check rss feed")

    parser.add_argument('-H', dest='rssfeed',
                         help='URL of RSS feed to monitor',
                         required=True)

    #Parse the info
    try:
        args = parser.parse_args()
    except:
        output = ': Invalid argument(s) {usage}'.format(usage=parser.format_usage())
        exitunknown(output)

    # Parse our feed
    rssfeed = args.rssfeed
    if (rssfeed.find('http://') != 0 and rssfeed.find('https://') != 0):
        rssfeed = 'http://{rssfeed}'.format(rssfeed=rssfeed)

    # we have the feed
    latest_entry = parse_last_rss_feed(rssfeed)
    feeddate = latest_entry['updated_parsed']

    # Get the difference in time from last post
    datetime_feeddate = datetime.datetime(*feeddate[:6])

    # Check for time difference
    with open(OUTPUT_FILE, "r") as read_file:
        if str(datetime_feeddate) == read_file.readline():
            exitok("no new feeds in store")
        else:
            with open(OUTPUT_FILE, "w+") as write_file:
                write_file.write(str(datetime_feeddate))
                exitcritical("New feed in store, need to update!")


if __name__ == '__main__':
    main()
