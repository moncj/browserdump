# browserdump

BrowserDump is a web browsing forensics tool, implemented in Python 2.7. In this proof-of-concept version, it has been developed and tested in limited Operation Systems, MAC OS Catalina 10.15.4, and Ubuntu 16.0.4. Currently, it supports 3 major browsers, IE 11, Chrome, and Firefox. Due to previous researches, we found out that private browser artifacts can be obtained by extracting live memory through manual approaches that are not practical in all actuality of forensics investigation. Moreover, Existing web forensics tools mainly focus on gathering web histories from SQL Database Files which can only collect public browsing information. The goal of this tool is to fill the gap of web forensics approaches and facilitate examiners to recover entire web browsing artifacts, including URLs and images, regardless of browser mode.

Software Requirement
- Python 2.6 or later, but not 3.0. http://www.python.org
- Volatility Framework 2.6.1 https://github.com/volatilityfoundation/volatility
- Scalpel 2.1 https://github.com/sleuthkit/scalpel\\

Methodology
The tool performs forensics functions based on a collection of open tools including Volatility and Scalpel. Firstly, Volatility is used to initialize the analysis of memory. We acquire the capability of Volatility to enumerate computer processes in the captured memory file and then separate only a chunk of the web browser's memory to be processed further. Possible URL histories are discovered and collected by matching string patterns with Regular Expression concentrating on HTTP and HTTPS protocol. While image recovery was proceeding under the functionality of Scalpel. JPG and PNG image files were carved out based on specific string header in the customized configuration file.

Instruction
1. Download both project.py and img.conf and drop them in Volatility folder

Command
python project.py -f <inputfile> -p <profile> -b <ie|chrome|firefox|all> -o <output>

Example
python project.py -f ../chrome_memdump.mem -p Win10x64_17134 -b chrome -o chrome-output

##
