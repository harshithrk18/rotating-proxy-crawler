from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random

ua = UserAgent() 
proxies = [] 
a = []

def util(s):
	d = {'hour':3600, 'minutes':60,'seconds':1}
	w = s.split()
	w.remove('ago')
	print(w)

	t = 0
	if 'hour' in w:
		t = int(w[0])*d['hour'] + int(w[2])
	elif 'minutes' in w:
		t = int(w[0])*d['minutes']
	else:
		t = int(w[0])

	return t
def main():
  proxies_req = Request('https://www.sslproxies.org/')
  proxies_req.add_header('User-Agent', ua.random)
  proxies_doc = urlopen(proxies_req).read().decode('utf8')

  soup = BeautifulSoup(proxies_doc, 'html.parser')
  proxies_table = soup.find(id='proxylisttable')

  for row in proxies_table.tbody.find_all('tr'):
    t = util(row.find_all('td')[7].string)
    a.append({
      'ip':   row.find_all('td')[0].string,
      'port': row.find_all('td')[1].string,
      'time': t
    })
  proxies.extend(sorted(a, key=lambda i:i['time']))

  print(proxies)
  p = 0
  for n in range(100):
    proxy = proxies[p]
    req = Request('http://icanhazip.com')
    req.set_proxy(proxy['ip'] + ':' + proxy['port'], 'http')
    try:
      my_ip = urlopen(req).read().decode('utf8')
      print('#' + str(n) + ': ' + my_ip)
      p+=1
    except:
      del proxies[p]
      
      print('Proxy ' + proxy['ip'] + ':' + proxy['port'] + ' deleted.')


main()