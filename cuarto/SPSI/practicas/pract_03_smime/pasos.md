### Práctica 3

## Emisor 1 EVE
openssl smime -sign -in pract_03.pdf -out pract_03.pdf.sgn -signer eve.cert.pem -inkey eve.key.pem -binary -nodetach

openssl smime -encrypt -in pract_03.pdf.sgn -out pract_03.pdf.sgn.enc alice.cert.pem	

## Emisor 2 ALICE
openssl smime -decrypt -in pract_03.pdf.sgn.enc -out pract_03.pdf.sgn -recip alice.cert.pem -inkey alice.key.pem

openssl smime -pk7out -in pract_03.pdf.sgn | \
openssl pkcs7 -print_certs -noout

openssl smime -verify -binary -in pract_03.pdf.sgn -noverify -out pract_03.pdf

openssl smime -resign -in pract_03.pdf.sgn -out pract_03_2.pdf.sgn -signer alice.cert.pem -inkey alice.key.pem -nodetach

openssl smime -encrypt -in pract_03_2.pdf.sgn -out pract_03_2.pdf.sgn.enc bob.cert.pem

## Receptor BOB
openssl smime -decrypt -in pract_03_2.pdf.sgn.enc -out pract_03_2.pdf.sgn -recip bob.cert.pem -inkey bob.key.pem


openssl smime -pk7out -in pract_03_2.pdf.sgn | \
openssl pkcs7 -print_certs -noout

openssl smime -verify -binary -in pract_03_2.pdf.sgn -noverify -out pract_03_2.pdf
