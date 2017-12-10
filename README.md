This is the backend of [English-Thai Dictionary แปลอังกฤษ-ไทย Chrome Extension](https://chrome.google.com/webstore/detail/english-thai-dictionary-แ/ofinfhfbojcjhgnocfcgoefgnledhddn)

Dictionary data is from Lexitron project by NECTEC. It's parsed into a dynamodb database through a small program in parselexutil folder.

The previous iteration of this same program is in Django and MySQL deployed on DigitalOcean. It had been moved to AWS Lambda and DynamoDB to save cost.