# Markdown Link Checker

This Python script scans through a local, user-provided Markdown file, locates all URLs within the file, and performs two checks:

1. Ensures that the URL is still accessible (in other words, that it does not return a 404 or is redirected)
2. If the URL utilizes HTTP over HTTPS, checks to see if it can use HTTPS and alerts the user if it can

## Getting Started

With these instructions, you will be able to deploy this script and analyze URLs within a local Markdown file.

1. Clone this repository

```
git clone https://github.com/ChristopherJHart/markdown-link-checker.git
```

2. Move into the repository's directory

```
cd markdown-link-checker
```

3. Execute the script using a Python 3 binary, passing in the filepath of a Markdown file as an argument

```
python3.6 markdown-link-checker.py /Users/Example/my_markdown_file.md
```

4. After a few moments, you should see the results of the script on the console.

```
Issue with URL: http://viptela.com/
Issue with URL: http://www.apstra.com/products/
Issue with URL: http://www.anutanetworks.com/ncx-overview/
Insecure URL http://rundeck.org/ detected!
        Use https://rundeck.org/ instead
Issue with URL: http://www.intellimentsec.com/
Issue with URL: http://www.rconfig.com/
Insecure URL http://cisco.com/go/nso detected!
        Use https://cisco.com/go/nso instead
Insecure URL http://www.intentionet.com/ detected!
        Use https://www.intentionet.com/ instead
Insecure URL http://packetpushers.net/podcast/podcasts/pq-show-99-netmiko-napalm-network-automation/ detected!
        Use https://packetpushers.net/podcast/podcasts/pq-show-99-netmiko-napalm-network-automation/ instead
Insecure URL http://packetpushers.net/podcast/podcasts/pq-show-81-network-testing-todd/ detected!
        Use https://packetpushers.net/podcast/podcasts/pq-show-81-network-testing-todd/ instead
Insecure URL http://packetpushers.net/podcast/podcasts/pq-135-mastering-python-networking-book/ detected!
        Use https://packetpushers.net/podcast/podcasts/pq-135-mastering-python-networking-book/ instead
Issue with URL: http://jinja2test.tk/
```

5. For more details, review the markdown-link-checker.log file created within the markdown-link-checker directory. This is especially useful if you run the script with the `--debug` flag.

```
$ tail markdown-link-checker.log
2018-10-27 22:54:28,685 ERROR    [https://slack.networktocode.com] Timed out while accessing URL
2018-10-27 22:54:28,685 DEBUG    [http://slack.networktocode.com] HTTPS does not work, reverting to HTTP
2018-10-27 22:54:33,803 ERROR    [https://jinja2test.tk/] Timed out while accessing URL
2018-10-27 22:54:33,803 DEBUG    [http://jinja2test.tk/] HTTPS does not work, reverting to HTTP
2018-10-27 22:54:34,113 ERROR    [http://jinja2test.tk/] Issue with URL | Code: 203
```

## License

This project is licensed under the MIT license - see the LICENSE.md file for details.