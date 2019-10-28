

from redis import Redis
from rq import Queue

from count import check_url

q = Queue(connection=Redis())


for i in range(0,100):
    result = q.enqueue(
                check_url, 'https://cded1u2ypquuejdj.mojostratus.io/magento/')

