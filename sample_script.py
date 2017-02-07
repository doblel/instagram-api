"""script example."""
from instagram import Instagram

ACCESS_TOKEN = '<access_token>'

ig = Instagram(access_token=ACCESS_TOKEN)

me = ig.self()['data']

print 'id:', me['id']
print 'username:', me['username']
print 'bio:', me['bio']
print 'media:', me['counts']['media']
print 'follows:', me['counts']['follows']
print 'followers:', me['counts']['followed_by']
