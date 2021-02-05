import numpy as np
import json

projects_list_url = "https://commons.wikimedia.org/w/api.php?action=sitematrix&smtype=language&format=json"
projects = json.load(projects_list_url)

print(projects)

# https://wikimedia.org/api/rest_v1/metrics/pageviews/top-by-country/fr.wikipedia/all-access/2021/01