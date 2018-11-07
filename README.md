# New Dawn Server Repo
## Setup
1. Clone the repo to your local machine by running `git clone https://github.com/tangziyi001/new_dawn_server.git`
2. Download virtualenv
3. Run `virtualenv new_dawn` to create a virtual env
4. Activate your virtual env by running `source new_dawn/bin/activate`
5. Run `pip install -r requirements.txt` to install dependencies
6. Add "127.0.0.1" to ALLOWED_HOSTS in new_dawn_server/settings.py

## Dev
* Make sure to re-do the step 4 above before coding. After dev, run `deactivate` to exit the virtual env.
* Please create your own branch by running `git branch <yourname>` and run `git checkout <yourname>` before development. Commit and push your work by running `git push origin <yourname>` instead of master.
* Send pull request for code review before merging.
