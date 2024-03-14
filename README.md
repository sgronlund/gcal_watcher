# gcal_watcher
This repository watches over unwatched changes in a shared Google Calendar albeit in a quite hacky fashion. 

## how worky
1. Fetch ICS content via GCal
2. Read through content and parse events which are in scope for the search
3. Compare to the most recently parsed events and see if there has been any bad guys making unwanted changes
4. Alert user that changes have been made and that someone should act/take action/check what's going on

## Implemented
- [x] Fetch GCal content and parse
- [ ] Get diff between two different times
- [ ] Alert the user

## nice to have
- [ ] Cron job/scheduling?
- [ ] Email for alerts 
