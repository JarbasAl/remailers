from usenet.server_entry import UsenetServer
from remailers.aam import AnonBox
from remailers.keys import Credentials
from datetime import timedelta

USENET_URL = "news2.neva.ru"

server = UsenetServer(USENET_URL)
creds = Credentials("my_private_key.asc")
inbox = AnonBox(creds, server)


### Test search by subject, all subjects below should work
# this is the subject after hsub
subject = "4b67314630615a4f693c3adc1b49da3157a2f2337a70f6a7"
# this is the subject before hsub
subject = "evil dolphin"
print("retrieving", subject, "from", USENET_URL)
articles = inbox.retrieve_by_subject(subject, since=timedelta(days=1))
for article in articles:
    print(article.subject, "-", article.text)


### Test brute force decryption (try to decrypt all messages)
print("retrieving from", USENET_URL)
articles = inbox.retrieve(since=timedelta(days=1))
for article in articles:
    print(article.subject, "-", article.text)

