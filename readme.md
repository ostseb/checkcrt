# Checkcrt
Keep track of your certificates.

## .env
MAILGUN_SENDER="domain.tld"
MAILGUN_TOKEN="key-xxx"
MAILGUN_FROM="Checkcrt<noreply@domain.tld>"
MAILGUN_TO="you@domain.tld,cto@domain.tld"
SITES="www.subbrand.tld,/www/api.brand.tld"


## Understand the sites syntax

`/www/api.brand.tld` - This will scan:
* brand.tld
* www.brand.tld
* api.brand.tld

`www/store/api.brand.tld` - This will scan:
* www.brand.tld
* store.brand.tld
* api.brand.tld
