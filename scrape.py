import requests
from bs4 import BeautifulSoup
BASE_URL = "http://www.reddit.com/r/earthporn+villageporn+cityporn+spaceporn+waterporn+abandonedporn+botanicalporn+adrenalineporn+destructionporn+machineporn+geekporn+mapporn+adporn+designporn+roomporn+skyporn+fireporn+infrastructureporn+climbingporn+architectureporn+artporn+cemeteryporn+fractalporn+exposureporn+agricultureporn+geologyporn+futureporn"


class Scraper(object):
	content = ''
	soup = None
	
	def __init__(self):
		self.iters = 5

	def find_next_url(self):
		return self.soup.select('[rel~="next"]')[0].get('href')

	def go(self, URL):
		tempfile = None
		print 'Downloading and writing HTML to file'
		tempfile = open('temp.html', 'wb')
		print 'Running request to URL:%s' % URL
		r = requests.get(URL)
		print 'Finished retreiving HTML'
		print 'Writing HTML to temp file...'
		tempfile.write(r.text.encode('utf-8'))
		tempfile.close()

		tempfile = open('temp.html', 'rb')

		tempfile.seek(0)
		self.content = ''.join(tempfile.readlines())
		tempfile.close()
		print 'Parsing HTML'
		self.soup = BeautifulSoup(self.content)
		print 'Trying to find links'
		urls = map(lambda x: x.get('href'), self.soup.select('p.title > a'))

		for url in urls:
			if url.find('comments') > 0 or url.find('reddit.com') > 0:
				continue
			filename = url.split('/')[-1]
			if filename.find('.') < 0:
				continue
			print 'GOT URL!', url, 'Filename: %s' % filename 
			try:
				f = open('pics/%s' % filename, 'r')
				print 'Image already exists, skipping...'
				f.close()
				continue
			except IOError:
				f = open('pics/%s' % filename, 'wb')
				print 'Downloading and writing %s' % filename
				f.write(requests.get(url).content)
				f.close()
				print 'Closed file.'

		if self.iters > 0:
			next_url = self.find_next_url()
			if not next_url:
				return
			print 'Found next URL: %s' % next_url
			self.iters = self.iters - 1
			print 'Iteration:%s' % self.iters
			self.go(next_url)

		print 'Done.'



if __name__ == "__main__":
	s = Scraper()
	s.go(BASE_URL)
