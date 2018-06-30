### How to use

```bash
$ echo 'ACTION=="add", DRIVERS=="sd", RUN+="/home/xi/kek.sh"' > 
  /etc/udev/rules.d/kek.rule

$ sudo udevadm control -R
```

### About udev

Udev is a listener of events associated with hardware devices, connect / disconnect basically. It has pattern-match rules, each leads to an action: create a link to a device in `/dev` dir, mount a device, or run a user-defined program. [Man page](https://jlk.fjfi.cvut.cz/arch/manpages/man/udev.7) defines how rules are constructed, there is a slightly watery [guide](http://www.reactivated.net/writing_udev_rules.html). Brief retelling:


1. `CLAUSE, CLAUSE, CLAUSE, ACTION` defines a rule.
2. `CLAUSE` is `VAR=="val"`, set of VAR's can be found in man page.
3. `ACTION` modifies the state
   + `RUN+="/home/xi/kek.sh"` runs the program, absolute path is required.
   + The first argument passed is either "add" or "remove"
   + Detach it as soon as possible, like `bash -c "kek &"`


### Useful commands

* Extract parameters to write clauses:
  ```
  udevadm info -a -p $(udevadm info -q path -n /dev/sdd1)
  ```
  
* Test rules (not executing programs)

  ```bash
  udevadm test /sys/block/sdd/
  ```

* Reload rules:
  ```bash
  sudo udevadm control -R
  ```
