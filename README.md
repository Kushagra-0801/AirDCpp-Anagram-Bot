# AirDCpp-Anagram-Bot

AirDCpp web extension that reads messages from `Anagram Game Hub`.
If the message is a question statement, the extension looks up the letter frequency in a dictionary and gets a list of all the words with the same frequency.
A post request is then made for each possible answer.

## Known Problems

1. Extension only looks for `Anagram Game Hub` and the hub has to be connected before the extension is started.
2. The extension could sometimes cross the message limit and get blocked from writing more messages.
3. Since the extension keeps on making http request, it could congest the network if the client is on a remote server instead of localhost.
