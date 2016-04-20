#! /bin/bash

# Move to directory of Repo
cd /var/www/FlaskApps/Flu_Tracker

# Pull latest version of project down from GitHub
sudo git pull

# Reset wsgi file
sudo touch ../flutracker.wsgi

# Reset conf file for project
sudo touch /etc/apache2/sites-enabled/Flu_Tracker.conf

# Restart apache
/etc/init.d/apache2 restart

# Leave the server
exit
