# ComicDownloader2
2nd Version of my Comic Downloader. This version uses Selenium to scrape the website, get the source image URL and then automatically press the button to go to the next page

Support for new sites can be added by adding the XPath for the next button and the image tag in the conditionals in the comicSourceSite() method. (Add the site name and a new number for users to know which source to choose)

To use program, simply copy the comics URL from the first page, type the name of the comic and the amount of pages it has, before selecting in the menu the Comic's Source Site.

Comics will be downloaded as PNG in a new directory with the name of the comic
