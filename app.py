##################################
#  Author : Hardeep Kumar
#  Created On : Tue Aug 11 2020
#  File : run.py
#
#  run file for Flasog
###################################
from flasog import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
