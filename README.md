# badoinkazoink

Another side project

This script makes YouTube searches fors each line in a `titles.txt` file, and outputs a `results_urls.txt` file with the IDs of each top result, a `results_titles.txt` file for the titles, and a `results_skipped.txt` file if any searches didn't have valid results.

## Dependencies

- [scrapetube](https://pypi.org/project/scrapetube/)
- [yt-dlp](https://pypi.org/project/yt-dlp/)

## Instructions

Put the names of videos to search for in a `titles.txt` file in the same directory as the script, and run it.

## Why?

I made this to get data I can work with out of those music "playlists" on YouTube. If it has a list of songs in the description of the video, I'd copy those and put them in the `titles.txt` file (of course, after having removed the ##:## timestamps).

This script can also be used for batch downloading these files, as all you need to get a working YouTube URL from the results is to append `https://www.youtube.com/watch?v=` to the ID. This is a trivially easy task to automate with Python.

## To do

- Use the YouTube API to automatically add the results to a playlist under the user's account.
