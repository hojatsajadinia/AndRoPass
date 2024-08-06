
![Logo](https://github.com/koengu/AndRoPass/raw/main/utils/resource/AndropasslogoNew.png)

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-310/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
![GitHub last commit](https://img.shields.io/github/last-commit/koengu/AndRoPass)
[![Open Source Love svg3](https://badges.frapsoft.com/os/v3/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)


#  AndRoPass

!! **THIS TOOL IS FOR EDUCATIONAL PURPOSE** !!

A tool that helps bypass **Root** and **Emulator** Detection in Android Application. AndRoPass repackage an APK file and bypass Root and Emulator Detection mechanism. The output Apk file is signed and zip alignined.


## Requirements
* Java Development Kit (JDK) > 11
* Python > 3.10


## Install and Run

Install AndRoPass like below:

```bash
  git clone https://github.com/hojatsajadinia/AndRoPass.git
  pip install -r requirements.txt
  python AndRoPass.py -h
```
    
## Example
Use AndRoPass like below:
```bash
  python AndRoPass.py -a [APK_FILE.apk]
```

## Build docker
You can build your own Docker image like below:
```bash
  docker build . -t AndRoPass
```

## Run via Docker (Recommended)
Run the Docker version of AndRoPass:
```bash
  docker run -it -v [APK_DIR_PATH]:/data hojatsajadinia/andropass:latest -a /data/APK_NAME.APK
```
## Screenshots

![App Screenshot2](https://github.com/koengu/AndRoPass/raw/main/utils/resource/screenshot2.png)

![App Screenshot](https://github.com/koengu/AndRoPass/raw/main/utils/resource/screenshot.png)


## RootBeer Bypass
AndRoPass can fully bypass [RootBeer](https://github.com/scottyab/rootbeer) detection mechanism like below:
![RootBeerBypass](https://github.com/koengu/AndRoPass/raw/main/utils/resource/rootbeer.png)

## Difference between WR and WOR:

There is no major difference between WR and WOR; the distinction lies in the decompilation techniques used. You can test either WR or WOR to see which one works best for you.

## Disclaimer

**Important Notice:**

The AndRoPass tool is designed to assist with bypassing root detection mechanisms in Android applications for legitimate purposes such as testing and development. However, it is crucial to emphasize the following:

- **Ethical Use:** Ensure that you have the appropriate permissions and rights before using this tool. Unauthorized use of this tool to bypass security mechanisms in applications you do not own or have explicit permission to test is unethical and may be illegal.

- **Responsibility:** The developers of AndRoPass are not responsible for any illegal activities or misuse of the tool. It is your responsibility to use this tool in compliance with all applicable laws and regulations.

- **Legitimate Purposes Only:** This tool should only be used for legitimate purposes, such as security research, educational objectives, or testing within a controlled and authorized environment.

By using AndRoPass, you acknowledge and agree to these terms and take full responsibility for your actions. Always use tools like this responsibly and with respect for the rights and privacy of others.

## License

[MIT](https://choosealicense.com/licenses/mit/)

