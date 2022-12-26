---
Category: Tech
tags: mac
Date: 09 Nov 2008
---

# Setting Adium Status Messages with Quicksilver

Switching from [Pidgin](http://www.pidgin.im/) to
[Adium](http://www.adiumx.com/), one missing feature was the saved status
messages for different accounts. I have an ICQ account with only German
contacts, and an AIM account with only American contacts. In Pidgin, I can
create and save a status message "Dining Hall" that will set both accounts to
away and set different status messages for each of them, e.g. "Mensa" for the
ICQ and "At the dining hall" for AIM. In fact, I can save such collections of
status data where both the status and the status message is different for any
of my IM accounts.

In Adium I can only define saved statuses with a single status and a single
message, and then apply any of those saved statuses to any single account or to
the entirety of all my accounts.

However, with AppleScript, this is easy to add. The [Adium's AppleScript
API](http://trac.adiumx.com/wiki/AppleScript_Support_1.2) was a little hard to
find, but once you have that, the rest is easy. For example, I'll create a
script `AdiumDiningHall.applescript` in `~/Library/Scripts` with
the following lines:

```applescript
#!/usr/bin/osascript
tell application "Adium" to tell the account "micgoe01" to go online
tell application "Adium" to tell the account "175434867" to go online

tell application "Adium" to tell the account "micgoe01" to go away
tell application "Adium" to tell the account "175434867" to go away

tell application "Adium" to set status message of account "micgoe01" to "At the dining hall"
tell application "Adium" to set status message of account "175434867" to "Mensa"
```

If I leave out the first part about going online, the status will only be set for accounts that are already online.
I could also write a script that sets all accounts to Available:

```applescript
#!/usr/bin/osascript
tell application "Adium" to tell the account "michaelgoerz@gmail.com" to go online
tell application "Adium" to tell the account "175434867" to go online

tell application "Adium" to tell the account "micgoe01" to go available
tell application "Adium" to tell the account "175434867" to go available
```

Or one that signs out of all my accounts:

```applescript
#!/usr/bin/osascript
tell application "Adium" to tell the account "micgoe01" to go offline
tell application "Adium" to tell the account "175434867" to go offline
```

The beauty of having these scripts in `~/Library/Scripts/` is that they are
available to QuickSilver. I just hit Cmd+Space,
type part of my script name, hit Enter, and my predefined status is set in
Adium. It doesn't get any faster than that.
