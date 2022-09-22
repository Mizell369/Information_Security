import requests
browser = requests.session()
browser.proxies['http'] = 'http://127.0.0.1:8080'
postdata = {'inputName':'hacker','inputPassword':'letmein'}
response = browser.post('http://127.0.0.1:5730/login', postdata, allow_redirects = False)
print("RESPONSE: ", response.status_code, response.reason)
print("SERVER HEADERS", response.headers)
print("COOKIES:  ",browser.cookies.items())
#STOP DONT COPY ALL OF IT!  Now examine the request/response in burp.

postdata = {'inputName':'hacker','inputPassword':'letmein'}
response = browser.post('http://127.0.0.1:5730/login', postdata)
print("RESPONSE: ", response.status_code, response.reason)
print("SERVER HEADERS", response.headers)
print("COOKIES:  ",browser.cookies.items())
#STOP DONT COPY ALL OF IT!  Now examine the request/response in burp.

browser.headers['User-Agent']='Mozilla FutureBrowser 145.9'
postdata = {'inputName':'apiusername','inputPassword':'apipassword'}
response = browser.post('http://127.0.0.1:5730/login', postdata)
print("RESPONSE: ", response.status_code, response.reason)
print("SERVER HEADERS", response.headers)
print("COOKIES:  ",browser.cookies.items())
#STOP DONT COPY ALL OF IT!  Now examine the request/response in burp.

browser.headers['SomeSpecialHeader']='Send This Value Also'
postdata = {'inputMAC':'00:00:5e:00:01:02'}
content = browser.post('http://127.0.0.1:5730/data', postdata).content
print(content)
postdata = {'inputMAC':'00:00:00:00:00:00'}
content = browser.post('http://127.0.0.1:5730/data', postdata).content
print(content)
