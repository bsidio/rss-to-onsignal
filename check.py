from urllib.parse import urlparse
import feedparser, json, logging, psycopg2, os, requests

class Feedparser:
    # Set logging preferences
    
    log_level = logging.DEBUG

    log = logging.Logger('parser')
    log.setLevel(log_level)

    log_handler = logging.StreamHandler()
    log_handler.setLevel(log_level)

    log_fmt = logging.Formatter('[{asctime}] [{levelname}]\n{message}\n',
                                datefmt = '%d-%m %H:%M:%S', style = '{')
    log_handler.setFormatter(log_fmt)

    log.addHandler(log_handler)


    def connect(self):
        """Connects to the database"""
        self.url = urlparse(os.environ["DATABASE_URL"])
        self.log.info('connecting to the database')
        self.db = psycopg2.connect(database=self.url.path[1:],
                                    user=self.url.username,
                                    password=self.url.password,
                                    host=self.url.hostname,
                                    port=self.url.port)

        self.log.info('connection established')

    def get_latest_title(self):
        """Retrieves the last item's title from the database"""
        c = self.db.cursor()
        c.execute('SELECT * FROM titles.titles')

        self.latest_title = c.fetchone()[0]
        #print(self.latest_title)
        self.log.info('latest title is ' + self.latest_title)

        c.close()

    def parse(self):
        """Takes latest feed items and checks whether they are new"""       
        # Get feed RSS
        
        try:
            feed = feedparser.parse(os.environ["FEED_URL"])
            self.log.info('feed parsed successfully')
        except Exception:
            self.log.warning('an error occured while parsing')
            self.db.close()
            exit()
        
        # Add counter and titles' list
        i = 0
        self.new_titles = []
        # print(self.latest_title)
        length = len(feed.entries)

        while i < length:
            # print(i)
            if feed.entries[i].title == self.latest_title:
                break
            
            # If new title, add it and seek deeper
            self.new_titles.append([feed.entries[i].title, feed.entries[i].link])
            i += 1



    def send(self):
        """Pushes new titles to Onesignal"""
        if not self.new_titles:
            self.log.info('no new titles, nothing to send')
            self.db.close()
            exit()
        
        # Onesignal headers and data
        header = {"Content-Type": "application/json",
                  "Authorization": "Basic "+str(os.environ['ONESIGNAL_AUTHORIZATION'])}
        payload = {"app_id": str(os.environ['ONESIGNAL_APP_ID']),
                   "included_segments": ["All"]
                  }

        # Customize messages
        if len(self.new_titles) != 0:
            self.log.info('sending one new title')

            payload["headings"] = {"en": "News Alert"}
            payload["contents"] = {"en": self.new_titles[0][0]}
        
        # Attempt to send a push
        print(payload)
        req = requests.post("https://onesignal.com/api/v1/notifications",
                            headers = header,
                            data = json.dumps(payload))

        if req.status_code != requests.codes.ok:
            self.log.warning('error code ' + str(req.status_code)
                             + ': ' + req.text)
        else:
            self.log.info('sent successfully!')

    def save(self):
        """Records the latest title to the database"""

        c = self.db.cursor()
        
        # Delete everything from the database
        self.log.info('purging the database')
        c.execute('DELETE FROM titles.titles;')
        self.log.info('purged successfully!')
        # Add the latest title to the database
        self.log.info('adding ' + self.new_titles[0][0] + ' to the database')
        c.execute('INSERT INTO titles.titles VALUES (%s);', (self.new_titles[0][0],))
        self.log.info('db altering success, exiting')

        self.db.commit()
        c.close()
        self.db.close()

parse = Feedparser()

parse.connect()
parse.get_latest_title()
parse.parse()
parse.send()
parse.save()