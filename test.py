from crawler.footer_links import discover_footer_links

root = "https://amfacosmetics.com"

urls = discover_footer_links(root)

print("DISCOVERED FOOTER / HOMEPAGE LINKS:")
for u in urls:
    print("-", u)