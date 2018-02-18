Shared timer application for synchronizing users working in intervals (e.g. 25 minutes).

# Usage

Start session as user 'Franz':
```
./start_session.py
```

Check if user 'Franz' has a running session (and file a request if so):
```
./query.py Franz
```

List all sessions of all users:
```
./list.py
```

# Setup
Prerequisite:
Shared folder that all users have read/write access to.

For the GUI notification:
```
apt-get install python-gobject libnotify
```

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

# Privacy Considerations
## Prevent users from checking other's working state
- instead of a central repository, there's a daemon running on every user's machine.
- communication is via UDP broadcast or multicast
- It's impossible for User B to check whether A has a running session.
- User B wants to talk to A after his session:
	- B sends a broadcast addressed with A
		- includes his public key
	- 3 possible outcomes:
		- A is not logged in at all -> no reply
		- A has no session running at the moment -> broadcasts 'no session' encrypted with public key of B
		- A has a session running -> broadcasts 'end time' encrypted with public key of B

