

from redis import Redis
from rq import Queue

from count import check_url

q = Queue(connection=Redis())

f = open("urls.list","r")

urls = f.read().split()
for url in urls:
    result = q.enqueue(
                check_url, "https://" + url)

