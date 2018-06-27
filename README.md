# About

`findmissing` is a python script that prints out missing numbers in an incrementing or decrementing sequence of numbers.

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
1bah8OM_F49BNeoct8M2DlXRRuOD8AUiY   DSC003.019   bin    1.1 GB   2018-06-12 17:24:41
1eZfY4qn3Ol6w1BFafQn6YDy1uOU82NNA   DSC003.020   bin    1.1 GB   2018-06-12 17:21:46
1x-P84Jq1cyuJCW2Opvy4m_qOjOHvAKtA   DSC003.021   bin    1.1 GB   2018-06-12 17:27:16
1O4TjR8Cl31A5qxHkyVmhmukp4dofCO3t   DSC003.025   bin    1.1 GB   2018-06-12 17:36:00
```

> **Note**: The above sample can be found in readme_sample.txt.

The above output shows eight 1.1 GB files in google drive. If we look at the extensions of the files it is evident that there are several files missing.

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
15
16
17
18
22
23
24
$ 
```

# Options

In the example above, files climbed up to `DSC003.029`. We can inform the script of this with the `-l` flag like so:

```
$ python findmissing.py -f readme_sample.txt -p "DSC003\.(\d+)" -l DSC003.029
3
4
5
6
7
9
12
13
14
15
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

Conversely, files started at `DSC003.000`, which we can inform the script of as well:

```

```