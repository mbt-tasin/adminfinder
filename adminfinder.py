import aiohttp
import asyncio
import re
import argparse
import time
import os
import sys

if sys.platform.startswith('linux'):
    W = '\033[1;37m'
    B = '\033[1;34m'
    R = '\033[1;31m'
    G = '\033[1;32m'
    Y = '\033[1;33m'
    C = '\033[1;36m'
else:
    W = B = R = G = Y = C = ''


banner = f'''
{G}░█▀█░█▀▄░█▄█░▀█▀░█▀█░░░█▀▀░▀█▀░█▀█░█▀▄░█▀▀░█▀▄
░█▀█░█░█░█░█░░█░░█░█░░░█▀▀░░█░░█░█░█░█░█▀▀░█▀▄
░▀░▀░▀▀░░▀░▀░▀▀▀░▀░▀░░░▀░░░▀▀▀░▀░▀░▀▀░░▀▀▀░▀░▀

Ultra-Fast Admin Finder Tool BY: MBT.Tasin Version:2.0

Github: https://github.com/tasinmohsen

{Y}[!] legal disclaimer: Usage of Admin Finder for attacking targets without 
prior mutual consent is illegal. It is the end user's responsibility to obey 
all applicable local, state, and federal laws. Developers assume no liability 
and are not responsible for any misuse or damage caused by this program{W}
'''


async def scan_admin_panel(web, adminpanel, session, adminpanel_txt, loaded_links, found_count, error_count, total_links, tt_tried_link, site):
    try:
        webpanel = web + "/" + adminpanel
        async with session.get(webpanel, timeout=5) as response:
            if response.status in (200, 401, 403):
                if response.status == 401:
                    print(f"{Y}[{response.status}] Unauthorized at [{webpanel}]{W}", end='\r')
                else:
                    found_count[0] += 1
                    print(f"[{tt_tried_link[0]}/{total_links}] {G}Found:{found_count[0]} {W} [{response.status}] Connected to [{webpanel}] successfully{W}", end='\r')
                    if adminpanel_txt:
                        with open(adminpanel_txt, "a") as file:
                            file.write(f"{webpanel}\n")
                    loaded_links.append(webpanel)
                    site.append(webpanel)
            else:
                error_count[0] += 1
                print(f"[{tt_tried_link[0]}/{total_links}] Found:{found_count[0]} [{response.status}] Unexpected status code for [{webpanel}]{W}", end='\r')
    except (asyncio.TimeoutError, aiohttp.client_exceptions.ServerDisconnectedError, aiohttp.client_exceptions.ClientOSError):
        print(f"{R}Error: Retrying...{W}", end='\r')
        await scan_admin_panel(web, adminpanel, session, adminpanel_txt, loaded_links, found_count, error_count, total_links, tt_tried_link, site)
    except KeyboardInterrupt:
        pass

REQUESTS_PER_WAIT = 1000
WAIT_TIME_SECONDS = 5

async def main():
    print(banner)
    parser = argparse.ArgumentParser(description="Admin Panel Finder")
    parser.add_argument("-u", "--url", required=True, help="URL of the website to scan")
    parser.add_argument("-w", "--wordlist", default="default_adminpanel_list.txt", help="Word list of admin panel paths")
    parser.add_argument("-o", "--output", action="store_true", help="Save output to a file")
    args = parser.parse_args()

    if not os.path.exists(args.wordlist):
        print(f"{R}Error: Wordlist file '{args.wordlist}' not found.{W}")
        return
    website = args.url

    if not re.match(r'^https?://', website):
        website = 'http://' + website

    print(f"{G}[+]{W} Target: {Y}{website}{W}")
    print(f"{G}[+]{W} Finding the website admin panel")
    adminpanel_txt = None
    output_filename = None
    if args.output:
        adminpanel_txt = f"output/{website.replace('://', '_').replace('/', '_')}_admin.txt"
        if os.path.exists(adminpanel_txt):
            os.remove(adminpanel_txt)
        output_filename = f"output/{website.replace('://', '_').replace('/', '_')}_output.txt"

    loaded_links = []
    found_count = [0]
    error_count = [0]
    site = []

    if not os.path.exists('output'):
        os.makedirs('output')

    start_time = time.time()

    max_threads = 100  # You can adjust this based on your system's capacity
    async with aiohttp.ClientSession() as session:
        tasks = []
        with open(args.wordlist, 'r') as admin_list:
            admin_list_lines = admin_list.readlines()
            total_links = len(admin_list_lines)
            tt_tried_link = [0]
            print(f"{G}[+]{W} Total {Y}{total_links}{W} Link Loaded\n")
            for line in admin_list_lines:
                adminpanel = line.strip('\n')
                tt_tried_link[0] += 1
                task = scan_admin_panel(website, adminpanel, session, adminpanel_txt, loaded_links, found_count, error_count, total_links, tt_tried_link, site)
                tasks.append(task)

                if len(tasks) >= max_threads:
                    await asyncio.gather(*tasks)
                    tasks = []

                # Wait for a specified time after sending a certain number of requests
                if tt_tried_link[0] % REQUESTS_PER_WAIT == 0:
                    await asyncio.sleep(WAIT_TIME_SECONDS)

            await asyncio.gather(*tasks)

    end_time = time.time()
    elapsed_time = end_time - start_time

    num_found_panels = len(loaded_links)
    print(f"\n\n{W}Those admin panels are found on this page [{Y}{website}{W}]{G}")
    for link in site:
        print(link)
    if num_found_panels == 0:
        print(f"{R}[x]{G} No admin panel found!{W}")
    else:
        print(f"\n{G}[+] {Y}{num_found_panels}{G} Admin Panel(s) Found in {elapsed_time:.2f} seconds")

    if args.output:
        if output_filename:
            if os.path.exists(output_filename):
                os.remove(output_filename)
            print(f"Output saved at {output_filename}")

if __name__ == "__main__":
    asyncio.run(main())
