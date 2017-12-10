Lexitron API
=============

This is the backend of [English-Thai Dictionary แปลอังกฤษ-ไทย Chrome Extension](https://chrome.google.com/webstore/detail/english-thai-dictionary-แ/ofinfhfbojcjhgnocfcgoefgnledhddn)

Dictionary data is from [Lexitron project](http://lexitron.nectec.or.th/) by NECTEC. It's parsed into a dynamodb database through a small program in parselexutil folder.

The previous iteration of this same program was written in 2013 using Django and MySQL and deployed on DigitalOcean. It had been partially re-written to use AWS Lambda and DynamoDB to save cost.

Possible area of improvement
-----------------------------

- Regex to check for various patterns can be combined
- Unit test that mocks dynamodb response