## birdy

Birdy is backup program and an experiment.

Tradtitional backups -- meaning monolithic clones of the entire system -- may reduce cognitive overhead in the inception, but they have issues. Fundamentally, I don't like backing up mountains of data that cannot, should not, and will not ever be restored. What's relevant on my device is (1) personal files and (2) my configurations. So that's what birdy backs up.

Birdy is configured through a csv file, which is just a list of every relevant file (meaning the backup candidates), some info about where the files reside, and flags to determine if the files should be encrypted, are they files vs directories, and are they massive or in need of special treatment.

### Notes
- Birdy takes a modular approach, where every item is backed up individually (assuming it has been changed).
- The same is true of restores.
- There is a flag to set encryption on or off per file.

### Release Notes
0.6.4 switch from bz2 to gz <br />
0.6.3 add filter to python tar <br />
0.5.9 refactor, added full path support for system files <br />
0.5.8 bug fixes <br />
0.5.6 bug fixes <br />
0.5.5 bug fixes <br />
0.5.5 added Nextcloud path <br />
0.5.4 bug fixes <br />
0.5.3 bug fixes <br />
0.5.2 bug fixes <br />
0.5.1 bug fixes <br />
0.5.0 birdy alpha, complete ground-up refactor of original code
