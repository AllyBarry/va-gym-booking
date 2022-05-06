# Gym Booking Automation
Have you ever wanted to book a gym class but the slots fill up every time before you even get a chance?
This is an (:smiling_imp: evil) solution to that. Automate your booking with a scheduler and this handy code sample.
This sample is configured specifically for the Virgin Active (South Africa) online booking platform.

# Installation Requirements
I run the script through WSL2. VcXsr must be running if using the GUI.
 - Create a virtual environment and install the Python requirements
 - Copy the 'config-template' file to 'config.ini' and fill in the required values.
 - Geckodriver and Chromedriver successfully installed*
(This helped: https://www.gregbrisebois.com/posts/chromedriver-in-wsl2/)
 - Added `export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2; exit;}'):0.0` to my ~/.bashrc file
 - Add it to your crontabs file to schedule it to run:
 ```
 crontab -e
 # Example - for every Monday at 00:01:
 01 00 * * MON python /home/allyb/web_scraping/virgin-active-gym-booking.py
 ```
 - Note that cron needs to be configured to start up automatically if using wsl. (https://www.howtogeek.com/746532/how-to-launch-cron-automatically-in-wsl-on-windows-10-and-11/)

\* I have geckodriver and chromedriver in /usr/local/bin which is on my PATH.