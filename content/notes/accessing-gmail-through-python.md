---
Category: Programming
Tags: python, gmail
Date: 29 Nov 2009
---

# Accessing GMail through Python

Over the last couple of years, I've made several attempts at efficiently
interacting with Gmail through Python. There were a number of motivations:

* Filtering mail: Putting emails into folder based on more elaborate rules than
  the server-side filters Gmail provides.
* Processing mail: Modifying emails, for example decrypting gpg-encrypted
  mails, or fixing missing header fields.
* Import and export: You want to keep local backups of your emails, and restore
  them.
* New mail notification, distinguishing between senders.

### How Does Gmail Work? ###

Gmail follows a somewhat new paradigm compared to traditional mail systems.

Traditionally, a mailbox contains a ordered list of messages. These messages
can sometimes have a limited number of tags (e.g. 'replied'), and conversation
threads can be constructed from the 'references' field in the email's
header. In Python, there is a class describing the traditional [mailbox
interface](http://docs.python.org/library/mailbox.html). There tends to be a
collection of mailboxes (folders) associated with one email account / server,
usually at least an Inbox and a Sent mailbox.

In contrast, a Gmail mailbox does not center around messages, but instead
around conversation threads: the mailbox is an unordered list of conversation
threads. Each thread can have a number of tags or labels associated with it.
Note that theses labels are not associated with the individual messages, but
always with the thread as a whole. Threads cannot be split or combined, there
is no guaranteed relationship between the 'references' header field in
the messages and the membership to a thread.

Also, even though the 'Inbox', 'Sent', 'All Mail', etc. look very similar to
the structure of multiple folders on, say, an IMAP server, this can be
misleading. You should look at your Gmail account as a single mailbox, with
'Inbox', 'Sent', 'All Mail', etc.  being labels to threads.
The difference is that each thread can have multiple labels, compared to a
message always being in a single folder.  If you put a message into multiple
folders on your IMAP server, these messages would be completely independent:
They'd take up more space, and deleting the message from one folder would
leave it entirely unaffected in the other. In Gmail, applying additional labels
to a thread does not use more space, and putting a thread into the Trash
removes the entire thread globally. Google explains this in their [help
section](http://mail.google.com/support/bin/answer.py?hl=en&amp;answer=10708).

### How Does Gmail Work through IMAP? ###

In addition to its web interface, which is based on the paradigm I just
explained, Google also provides [access via
IMAP](http://mail.google.com/support/bin/topic.py?topic=12806).

To do this, it is necessary to map Gmail features somehow into IMAP. Google
decided to break the focus on threads (in the web interface, you'll always
have entire threads in your Inbox, for example, while in IMAP, not all of the
messages belonging to the same thread have to be in the Inbox at the same
time). Also, they mapped labels to folders. This means that from the IMAP
client's point of view identical messages have no immediate connection
between them, they have to be downloaded multiple times, and any changes to one
do not affect the other copies. To keep the consistency, Google behaves as if
there constantly was a second IMAP client connected to the account, reacting to
anything you do. If you move a message to the Trash, the shadow client will
also delete the copies of the message from all other folders. In this way,
Google conforms to the IMAP standard, while keeping the consistency with their
paradigm.

Nonetheless, in many situations the way in which the Gmail system was mapped to
IMAP is not so well chosen. For one thing, it would be nice to (at least
optionally) keep the messages of a thread together even in the IMAP interface.
Of course, this would mean even more intrusion by the shadow client, but at
least you'd be able to look at the entire thread without having to switch to
the 'All Mail' folder. It is also not always clear when a message will
show up in a given folder.

Secondly, at least from the programmer's point of view, it would be nice to
have access to the labels of a message not just through different folders. It
turns out the the IMAP standard allows for arbitrary labels ('flags') to
messages ([RFC3501](http://tools.ietf.org/html/rfc3501#section-2.3.2).  I am
not aware of any email client that makes full use of this possibility, a few
(like Thunderbird) use quasi-standard labels '$1', '$2', etc and
internally map them to labels like 'personal', 'work', etc. This
lack of support is probably what suggested Google to use folders instead.
Nonetheless, there is no reason why the Gmail IMAP server should not provide
access to the label-flags directly.

### Gmail Mailbox Class ###

It would be nice to have a Python class that provides a high level interface to
Gmail through IMAP. Of course, one can access the Gmail account just on the
normal IMAP level, as explained in the previous section. For this, I've
written a package called [ProcImap](http://github.com/goerz/procimap/).  Just
using that, one can already do a lot. However, one would really like to move
slightly more in the direction of the unique Gmail paradigm. Specifically, we
want two additional methods:

* Return all the labels of a given message
* Return all messages that belong to the same thread as a given message.

It turns out that both of these demands are extremely difficult to fulfill. I
experimented with some implementations for this in a Gmail module as part of
the ProcImap package, which was meanwhile removed again due to the difficulties
involved. Obviously, if Google decided to give access to the labels via the
IMAP flags feature, the first problem would be solved. For the second problem,
Google would have to keep a strict correlation between the 'references'
headers in the messages and the thread status.

So, what makes this problem so hard? Essentially, it comes down to the fact
that you have to deal with multiple copies of the same messages in different
folders. We could just go through all folders, find out which of them contain a
copy of the given message, and thus reconstruct a list of labels. Likewise, we
could reconstruct the threads (to the limit of the information we can get from
the 'references' headers) by identifying copies of the same message.

Unfortunately, this is something IMAP was absolutely not made for. There simply
is no efficient way to decide whether two email messages are copies of each
other. In theory, the 'message-id' header field should fulfill this
purpose, but its proper use has never been enforced. Messages may have missing
IDs, or different messages may have the same ID. Comparing the full header of
two messages is also not enough: one could be a copy of the other, stripped of
attachments, for example. The only thing that would work is to compare a hash
of the full messages. This is highly inefficient and also very sensitive to any
sort of corruption.

There is also one last issue: Gmail sometimes considers different mails as
identical, and refuses to add them to the account. It is completely unclear
under which conditions this happens. For example, I've had instances where
Gmail would refuse to add (i.e. silently ignore) the decrypted version of an
email while the encrypted version was still in the mailbox. Also, trying to
upload a copy of an email with some modified header fields often fails.

The severity of these problems becomes clear when we look at the decryption
problem again in detail. We would have to follow the following steps:

* Save all the labels of the message. As discussed above, this is very
  difficult.
* Download the encrypted email and move the original to the Trash (direct
  deletion of a message is not possible). This will remove all copies of the
  message from all folders.
* Identify the message in the Trash, and delete it from there. As discussed
  above, the identification is hard. If we neglect this step we may run into
  the problem that the upload of the decrypted message will fail.
  Alternatively, we can delete the entire trash, this however may be
  undesirable.
* Decrypt the message and upload it again.
* Store copies in all the original labels.

So far, there is no satisfactory way to go through this process.

### Brute Forcing Gmail ###

There is one possible but inefficient way out of this: Download every message
in every folder (that means downloading multiple copies of the same message),
and analyze the structure of the messages. We can then keep the information of
which message has which labels, and which message belongs to which thread in a
local cache. We would have to update that cache in regular intervals (which
could be done at a sufficiently small cost since we only need to process
changes since the last update). Using that cache, we could implement an
interface that provides access to most aspects of the Gmail paradigm. The no
longer existing Gmail class in the ProcImap package experimented with that
approach, but the entire concept turned out to be very inelegant in its
implementation.

Nonetheless, the brute force approach can be useful for certain applications.
For example, I have a collection of python scripts
([gmailbkp](http://github.com/goerz/gmailbkp)) that work on top of ProcImap and
provide incremental backup of your gmail mailbox.

### libgmail ###

There is one available alternative to the IMAP approach: The
[libgmail](http://libgmail.sourceforge.net/) package. This package uses Java
Script to access Gmail (basically, it connects like a browser to the Gmail
website). The package provides a full abstraction of the Gmail paradigm, and it
does absolutely everything we want exactly how we want it. There is one big
drawback, however: Google does not support the library and monitors their web
interface for 'suspicious activity'. If you access your account too
intensely using libgmail, Google will lock you out for 24 hours. This makes it
impossible to use the library for backup purposes.  I did try:
[gmail_archive.py](http://github.com/goerz/gmail_archive.py).  Be warned that
using this script will very likely get you locked out of your account.

For smaller tasks, libgmail can be extremely valuable. It probably could solve
the decryption example. However, even with such small task the danger of being
locked out is always present.

In conclusion, there is no satisfactory way to interface Python with Gmail. You
either have to limit yourself to IMAP, or work with the dangers of libgmail.
The ProcImap package will probably not provide any explicit support for Gmail
in the future.
