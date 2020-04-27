# Checkcrt
Keep track of your certificates.

## How to setup with chronjob
How to check certificates status using checkcrt.py with chronjob

### Prerequisites
* A free Mailgun account mailgun.com
* Server running unix dist

### Setup
1. Download the source
```
wget -q https://github.com/ostseb/checkcrt/archive/master.zip
```

2. Unzip the tarball
```
unzip -q master.zip 
```

3. Install requirements
```
cd checkcrt-master/
pip install -r requirements.txt
```

4. Configure your .env file. See [.env](#.env) for more information
5. Test your config `python checkcrt.py` or `python checkcrt.py email`
6. Set up cron
Run `crontab -e` and add `12 20 * * 3 python /path/to/script/checkcrt.py email`

## .env
```
CHECKCRT_MAILGUN_SENDER="domain.tld"
CHECKCRT_MAILGUN_TOKEN="key-xxx"
CHECKCRT_MAILGUN_FROM="Checkcrt<noreply@domain.tld>"
CHECKCRT_MAILGUN_TO="you@domain.tld,cto@domain.tld"
CHECKCRT_SITES="www.subbrand.tld,/www/api.brand.tld"
```

## Understand the sites syntax

`/www/api.brand.tld` - This will scan:
* brand.tld
* www.brand.tld
* api.brand.tld

`www/store/api.brand.tld` - This will scan:
* www.brand.tld
* store.brand.tld
* api.brand.tld
