
# Some use case ideas
- User A starts a 30 min session at 2018-01-01T16:10
	- creates file "A-2018-01-01T16:40" containing the end time

- User B wants to know whether A has a session running currently
	- checks whether there is a file name with prefix 'A'
	- AND time stamp is still in the future

- User B wants to talk to A after his session
	- appends his user name to the current session file of user A
	- (or also a time stamp)
	- (or also some subject)

- User A finishes his current session
	- deletes his file
	- (or all of his files)

- User A wants to check if anyone has filed a 'talk request' for him
	- checks if his current session file contains anything

- User A walks over to User B due to a 'talk' request.

- User A wants to check who else is on the team, currently busy
	- lists all files and shows prefixes

- This works with
	- Dropbox
	- git
	- svn
	- Samba
	- local file system
	- scp?
