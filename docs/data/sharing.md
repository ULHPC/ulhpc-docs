## Security and Data Integrity

Sharing data with other users must be done carefully. Permissions
should be set to the minimum necessary to achieve the desired
access. For instance, consider carefully whether it's really necessary
before sharing write permssions on data. Be sure to have archived
backups of any critical shared data. It is also important to ensure
that private login secrets (such as SSH **private** keys or apache
htaccess files) are **NOT** shared with other users (either intentionally
or accidentally). Good practice is to keep things like this in a
separare directory that is as locked down as possible.

The very first protection is to maintain your Home with access rights `700`

```bash
chmod 700 $HOME
```

## Sharing Data within ULHPC Facility

### Sharing with Other Members of Your Project

We can setup a project directory with specific group read and write permissions, allowing to
share data with other members of your project.

### Sharing with ULHPC Users Outside of Your Project

#### Unix File Permissions

You can share files and directories with ULHPC users outside of your
project by adjusting the unix file permissions. We have an extensive
write up of unix file permissions and how they work
[here](../filesystems/unix-file-permissions.md).

## Sharing Data outside of ULHPC

The IT service of the University can be contacted to easily and quickly share data over the web
using a dedicated Data Transfer service.
Open the appropriate ticket on the [Service Now](https://service.uni.lu) portal.
