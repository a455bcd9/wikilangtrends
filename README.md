# wikilangtrends
Languages trends on Wikipedia

Wikimedia Statistics provides various metrics on their website: https://stats.wikimedia.org/

However, you can't compare two editions or get statistics for all Wikipedia projects.

ToolForge is slightly better: https://pageviews.toolforge.org/siteviews/?platform=all-access&source=pageviews&agent=user&range=latest-20&sites=en.wikipedia.org

I opened a feature request on Phabricator: https://phabricator.wikimedia.org/T257071

In the meantine, the code is this repo helps to answer the following questions:
* What's the most read (or edited) edition of Wikipedia by country at any point in time?
* In each country, what are the most read (or edited) editions of Wikipedia at any point in time?
* How did the share of page views (or edits) by language among all Wikipedias evolve over time?
* How did the share of page views (or edits) by country on one Wikipedia edition evolve over time?

Issues with the map:
* PS, AD, MC, SZ, PS, MT + PM, MV, FM, TL and some dependent territories

This code uses the Wikimedia API: https://wikimedia.org/api/rest_v1/#/
