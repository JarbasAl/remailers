from usenet.server_entry import UsenetServer
from remailers import Credentials
from remailers.hsub import create_hsub

creds = Credentials("priv_key.asc")
subject = "evil dolphin captain"
hsub = create_hsub(subject)
text = creds.encrypt("this is a test")
print(hsub)


USENET_URL = "freenews.netfront.net"
GROUP = 'alt.anonymous.messages'

with UsenetServer(USENET_URL) as server:
    response = server.post(text, hsub, GROUP)
    print(response)
