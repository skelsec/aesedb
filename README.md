# aesedb
async parser for JET

# What is this
This project is mainly aims to provide an async parsing option for NTDS.dit database file for obtaining user secrets.  
It might also useful for parsing random JET databases.

# Install
`pip install aesedb` or via cloning from github

# Usage
Either use it as a library (check the example on how) or if you wanna jump in parsing NTDS.dit use the following commands  

### Basic
`antdsparse <SYSTEM reg hive> <NTDS.dit>`
### User friendly
`antdsparse <bootkey> <NTDS.dit> -o <outputfile> --progress`  
`antdsparse <SYSTEM reg hive> <NTDS.dit> -o <outputfile> --progress`  

# Kudos
Core components of this library are from the awesome [impacket](https://github.com/SecureAuthCorp/impacket) toolkit.