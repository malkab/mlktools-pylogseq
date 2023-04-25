- #procesar

DEPRECATED DOCS
===

Exporting and Importing from Gmail
----------------------------------
__TAGS:__ linux, macos, gmail, email, export, conversion, import, thunderbird, imap

In Linux, to export, just use the Gmail exporter Takeout (Account Management). It exports selected tags to MBOX. Those must be safeguarded and never touched.

To view exported messages or even to reimport to Gmail:

- make a working copy of the MBOX file;

- if intending to import to Gmail, activate IMAP access, create in Gmail the label to import to, and, at Gmail Settings, go to Labels and activate IMAP access for just the required labels;

- install Thunderbird from packages;

- configure Gmail account IMAP access in Thunderbird (it's pretty much straightforward);

- install ImportExportTools from a file (it is in D/Packages);

- import the MBOX in local folders. If it's just for checking, we are done;

- to reimport, copy all messages in the MBOX local folder to the Gmail IMAP label folder;

- deactivate IMAP access in Gmail.
