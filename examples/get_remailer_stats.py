from datetime import timedelta


class RemailerStats:
    GROUP = "alt.privacy.anon-server.stats"

    def __init__(self, usenet_server):
        self.usenet_server = usenet_server

    def retrieve(self, subject, since=None):
        since = since or timedelta(days=2)
        articles = []
        with self.usenet_server as server:
            for article in server.get_new_news(self.GROUP, since=since):
                if subject in article.subject:
                    article.text  # retrieve body while connection is open
                    articles.append(article)
        # TODO sort by date
        return articles[0]

    def get_mixmaster_stats(self, since=None):
        return self.retrieve("Frelled Mixmaster Stats", since=since)

    def get_cypherpunk_stats(self, since=None):
        return self.retrieve("Frelled Cypherpunk Stats", since=since)


