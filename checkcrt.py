import functools
import os
import datetime
import requests
import re
import sys
from tabulate import tabulate
from dotenv import load_dotenv
load_dotenv(verbose=True)

def key_cmp_f(a,b):
  if (a[1].find('Error:') >= 0):
    return 1
  if (b[1].find('Error:') >= 0):
    return -1
  a = int(re.sub(r"\033\[1;37;41m|\033\[0;0m|\033\[0;30;43m", '', a[1]).split(' ')[0])
  b = int(re.sub(r"\033\[1;37;41m|\033\[0;0m|\033\[0;30;43m", '', b[1]).split(' ')[0])
  return (a - b)

def send_mail(subject,text,html):
	senderdomain = os.getenv("CHECKCRT_MAILGUN_SENDER")
	token = os.getenv("CHECKCRT_MAILGUN_TOKEN")

	return requests.post(
		"https://api.mailgun.net/v3/"+senderdomain+"/messages",
		auth=("api", token),
		data={
			"from": os.getenv("CHECKCRT_MAILGUN_FROM"),
			"to": os.getenv("CHECKCRT_MAILGUN_TO").split(","),
			"subject": subject,
			"text": text,
			"html": html,
		})

brands = os.getenv("CHECKCRT_SITES")
if brands is None:
  raise Exception("No sites found")

brands = brands.split(",")

i = 0
table = []
cli_table = []
now = datetime.datetime.now()
while i < len(brands):
  brand = brands[i]

  parts = brand.split(".")
  subdomains = parts[0].split("/")
  del parts[0]
  hostname = ".".join(parts)
  x = 0
  while x < len(subdomains):
    subdomain = subdomains[x]
    
    if len(subdomain) > 0:
      domain = subdomain + "." + hostname
    else:
      domain = hostname
      
    try:
      res = os.popen('echo | openssl s_client -servername '+domain+' -connect '+domain+':443 2>/dev/null | openssl x509 -noout -dates | grep notAfter').read()
  
      expires = datetime.datetime.strptime(res.strip().split('=')[1], '%b %d %H:%M:%S %Y GMT')
      daysLeft = (expires-now).days
      
      if daysLeft < 0:
        cli_row = [domain,('\033[1;37;41m' + str(daysLeft) + ' days left\033[0;0m')]
        row = [domain,(str(daysLeft) + ' days left')]
      elif daysLeft < 30:
        cli_row = [domain,('\033[0;30;43m' + str(daysLeft) +' days left\033[0;0m')]
        row = [domain,(str(daysLeft) +' days left')]
      else:
        row = cli_row = [domain, (str(daysLeft) +' days left')]
    except:
      row = cli_row = [domain, 'Error: Could not access certificate']
  
    table.append(row)
    cli_table.append(cli_row)
    x += 1
  i += 1

table.sort(key=functools.cmp_to_key(key_cmp_f))
cli_table.sort(key=functools.cmp_to_key(key_cmp_f))

cli_res = tabulate(cli_table, headers=["Site", "Days left"],tablefmt="github")
htm_res = tabulate(table, headers=["Site", "Days left"],tablefmt="html")
txt_res = tabulate(table, headers=["Site", "Days left"],tablefmt="plain")

if ("email" in sys.argv[1:]):
  print(send_mail("CertCheck "+str(now), txt_res, htm_res))
else:
  print(cli_res)
