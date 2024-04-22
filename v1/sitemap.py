# Find and Parse Sitemaps to Create List of all website's pages
from usp.tree import sitemap_tree_for_homepage

def getPagesFromSitemap(fullDomain):

    listPagesRaw = []

    tree = sitemap_tree_for_homepage(fullDomain)
    for page in tree.all_pages():
        listPagesRaw.append(page.url)

    return listPagesRaw


# Go through List Pages Raw output a list of unique pages links
def getListUniquePages(listPagesRaw):

    listPages = []

    for page in listPagesRaw:
        
        if page in listPages:
            
            pass

        else:
            
            listPages.append(page)

    return listPages

uncleaned_webpages = getPagesFromSitemap("https://www.recipetineats.com/")

webpages = getListUniquePages(uncleaned_webpages)

###NEED TO WRITE CODE WHICH UPLOADS WEBPAGES TO SQLITE3 database