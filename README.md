[![Build Status](https://travis-ci.org/Stunner/findmissing.svg?branch=master)](https://travis-ci.org/Stunner/findmissing)

# About

`findmissing` is a python script that prints out missing numbers in an incrementing or decrementing sequence of numbers.

`findmissing` has been developed and tested with Python 2.7 and 3.6.

## Use Case

I had some really big files I needed to upload to Google Drive, so `split` them into 1 GB files. An annoyance with the Google Web interface is that it will upload files that are queued by random rather than in order. So if you queue up the following files:

```
SubFile.001
SubFile.002
SubFile.003
SubFile.004
SubFile.005
```

It may start with `SubFile.004` and then `Subfile.002` and so on. Allowing for potential gaps in what files are uploaded, especially when the upload fails for whatever reason.

Initially, when this happened I had to resort to manually determining which files were missing and reupload those. More often than not I would inadvertently upload duplicates (Google Drive allows for files with the same name to exist at the same path), which would waste time in uploading files I didn't need to upload and additional effort in removing duplicated files.

# Example

I use [`gdrive`](https://github.com/prasmussen/gdrive) to query the files I have uploaded to Google Drive with the command `gdrive list --query "name contains 'DSC003'" | sort -k2`:

```
Id                                  Name         Type   Size     Created
1vBpXEM3_Jal1yUcHHghLdrG3rXrxQ3p0   DSC003.002   bin    1.1 GB   2018-06-12 13:55:37
1RknmQFhtzNDorO4Lp8AGpr4S_zmBqwKc   DSC003.008   bin    1.1 GB   2018-06-12 14:26:43
1Dgt5ZFKT3zilwPZdiPyPmhM0Y3Fz_xo8   DSC003.010   bin    1.1 GB   2018-06-12 16:57:14
16QPadXBXPGIwiRhzMFRuY7tZkdIlJ1DI   DSC003.011   bin    1.1 GB   2018-06-12 16:54:57
1zD492J3F42Azeoct82DMlXRRuWA8AUiY   DSC003.015   bin    1.1 GB   2018-06-12 17:32:12
1bah8OM_F49BNeoct8M2DlXRRuOD8AUiY   DSC003.019   bin    1.1 GB   2018-06-12 17:24:41
1eZfY4qn3Ol6w1BFafQn6YDy1uOU82NNA   DSC003.020   bin    1.1 GB   2018-06-12 17:21:46
1x-P84Jq1cyuJCW2Opvy4m_qOjOHvAKtA   DSC003.021   bin    1.1 GB   2018-06-12 17:27:16
1O4TjR8Cl31A5qxHkyVmhmukp4dofCO3t   DSC003.025   bin    1.1 GB   2018-06-12 17:36:00
```

> **Note**: The above sample can be found in readme_sample.txt.

The above output shows nine 1.1 GB files in google drive. If we look at the extensions of the files it is evident that there are several files missing.

`findmissing` can be used to determine the missing files like so:

```
$ python findmissing.py -f readme_sample.txt -p "DSC003\.(\d+)"
3
4
5
6
7
9
12
13
14
16
17
18
22
23
24
$ 
```

The `-p` flag is required and takes in a regex expression with a group (specified with parenthesis) denoting which portion of the string contains the number.

Also, the script is capable of reading from `stdin` so redirecting output to it is possible. Here is the aformentioned example but reading from `stdin` instead of from a file:

```
$ cat readme_sample.txt | python findmissing.py -p "DSC003\.(\d+)"
3
4
5
6
7
9
12
13
14
16
17
18
22
23
24
$ 
```

# Options

In the example above, files climbed up to `DSC003.029`. We can inform the script of this with the `--last` (`-l`) flag like so:

```
$ python findmissing.py -f readme_sample.txt -p "DSC003\.(\d+)" --last DSC003.029
3
4
5
6
7
9
12
13
14
16
17
18
22
23
24
26
27
28
29
```

Conversely, files started at `DSC003.000`, which we can inform the script of as well (with `--first` [`-i`]):

```
$ python findmissing.py -f readme_sample.txt -p "DSC003\.(\d+)" --first DSC003.0 --last DSC003.29
0
1
3
4
5
6
7
9
12
13
14
16
17
18
22
23
24
26
27
28
29
```

These two options can also be used together to hone in on a specific sub-range of missing values. For instance let's say we wanted to only view missing values from `10` to `20` (inclusive):

```
$ python findmissing.py -f readme_sample.txt -p "DSC003\.(\d+)" -i DSC003.10 -l DSC003.20
12
13
14
16
17
18
```
