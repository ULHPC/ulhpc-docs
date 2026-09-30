#import "template.typ": *

#let unilu-colormap = (
rgb("#e9edee"),
rgb("#e9edee"),
rgb("#4D4E4F"),
rgb("#AB3502"),
rgb("#E69426"),
rgb("#9CD7F3"),
)


#set text(lang: "en")
#show: sns-polylux-template.with(
  aspect-ratio    : "16-9",
  title           : [Getting Started on Grid’5000],
  subtitle        : [Practical Tutorial Session],
  event           : [University of Luxembourg\ 08/09/2025],
  short-title     : [],
  short-event     : [],
  logo-1          : image("pics/UNI-Logo-en-rgb.png"),
  logo-2          : image("pics/UNI-Logo-en-rgb.png"),
  side_image      : "pics/logo.png",
  colormap        : unilu-colormap,
  authors         : (
  )
)
#set page(footer: none)

#title-slide()

#toc-slide( title: [Table of Contents] )

#slide(title: [Grid'5000 Getting Started Tutorial])[
  Follow along with the tutorial at:

  #link("https://hpc-docs.uni.lu/g5k/getting-started-g5k/")[https://hpc-docs.uni.lu/g5k/getting-started-g5k/]

  #v(1em)
  _A hands-on guide to using Grid'5000 for research_
]

#new-section-slide([Introduction])

#slide(title: [What is Grid'5000?])[
  Grid'5000 is a large-scale testbed for experiment-driven research in computer science

  *Key Features:*
  - 11 sites in France, Belgium and Luxembourg
  - \~25,000 cores, 800 compute nodes, 550+ GPUs
  - Highly configurable and controllable hardware (bare-metal)
  - Advanced monitoring and measurement features
  - Reproducible research support
  
  *Focus Areas:* Parallel/distributed computing, cloud, HPC, Big Data, AI
]

#slide(title: [Before we start])[
  Make sure you have:
  - A Grid'5000 account
  - A Standard SSH client (OpenSSH on Mac OS, Linux or WSL) 
  - Your SSH key configured

 #block(
    fill: yellow.lighten(80%),
    stroke: orange + 1pt,
    inset: 10pt,
    radius: 4pt,
    width: 100%
  )[
    ⚠️ Request your account here (select the group *luxembourg-misc*)
    
    *#link("https://www.grid5000.fr/w/Special:G5KRequestAccountUMS")*
  ]
  
]

#slide(title: [Key Concepts])[

  *Hierarchical Resource Organization:*

  #align(center)[
    #table(
      columns: (1fr, 2fr),
      [*Resource*], [*Description*],
      [*Cluster*], [Named group of homogeneous nodes],
      [*Node*], [Bare-metal server/machine],
      [*Core*], [Smallest reservable unit (CPU core)]
    )
  ]

  *Examples:*
  - Cluster: `larochette`, `clervaux`, `petitprince`
  - Node: `larochette-1`, `clervaux-11`
  - Luxembourg clusters: `clervaux` (48 nodes), `larochette` (7 nodes), `vianden` (1 node), `petitprince` (11 nodes)
]

#slide(title: [Important resources])[

  *Grid'5000 Wiki:* *#link("https://www.grid5000.fr")*
  - Hardware specs: *#link("https://www.grid5000.fr/w/Hardware")*
  - Status and monitoring: *#link("https://www.grid5000.fr/w/Status")*

  *Resource Availability:*
  - Check Drawgantt charts for real-time availability
  - Plan reservations during off-peak hours
  - Monitor maintenance schedules
]


#new-section-slide([First connection])

#slide(title: [SSH keys setup])[
  *Before first login, generate your SSH keys:*

  ```bash
  user@pc: ssh-keygen -t ed25519
  user@pc: cat .ssh/id_ed25519.pub
  # Copy the output
  ```

  *Add your public key to Grid'5000:*
  1. Visit: https://api.grid5000.fr/stable/users/
  2. Paste public key in "SSH Keys" tab
  3. Save changes

  ⚠️ *Required before any Grid'5000 access*
]

#slide(title: [First connection])[
  #place(right, dy: 20pt, image("pics/Grid5000_SSH_access.png", width: 50%))

  *Manual connection:*
  ```bash
  user@pc:~$ ssh access.grid5000.fr
  user@access-north:~$ ssh luxembourg
  user@fluxembourg:~$
  ```

  *You should see the welcome message.*
]

#slide(title: [SSH config (recommended)])[

  *Edit `~/.ssh/config` on your local machine:*

  #set par(leading: 0.1em)
  ```bash
  Host g5k
    User <g5k_login>
    Hostname access.grid5000.fr
    ForwardAgent no
  
  Host *.g5k
    User <g5k_login>
    ProxyCommand ssh g5k -W "$(basename %h .g5k):%p"
    ForwardAgent no
  ```

  *Now you can connect directly:*
  ```bash
  user@pc:~$ ssh luxembourg.g5k
  ```
]

#new-section-slide([First resource reservation])

#slide(title: [Reserving resources])[

  *Basic reservation with OAR:*
  ```bash
  [user@fluxembourg|~]$ oarsub -r now -q testing
  # Filtering out exotic resources (vianden).
  # Set walltime to default (3600 s).
  OAR_JOB_ID=256908
  # Advance reservation request: waiting for validation...
  # Reservation valid --> OK
  ```

  *Check reservation status:*
  ```bash
  [user@fluxembourg|~]$ oarstat -u
  ```

  *Job States:* W (waiting), L (launching), R (running), E (error), F (finished)
]

#slide(title: [Connecting to the reservation])[

  *Get detailed job information:*
  ```bash
  user@fluxembourg:~$ oarstat -f -j <JOB_ID>
  ```

  *Connect to allocated node:*
  ```bash
  # Method 1: Direct SSH
  [user@fluxembourg|~]$ ssh clervaux-11
  
  # Method 2: OAR shortcut (single reservation only)
  [user@fluxembourg|~]$ oarsub -C
  ```

  *Verify you're on the compute node* - prompt should change!
]


#slide(title: [Working on the node])[

  *Storage locations:*
  - `~/` - Home directory (25GB, NFS-mounted, persistent)
  - `/tmp/` - Local disk (fast I/O, non-persistent)  
  - Storage groups - Large shared volumes

  *Best practice:* Work in `/tmp/` for performance, copy results to `~/`

  *Example workflow:*
  ```bash
  user@clervaux-11:~$ cd /tmp/
  # Download, compile, run experiments
  # Copy important results back to ~/
  ```
]

#slide(title: [Practical example])[

  *Download and run NAS Parallel Benchmarks:*
  ```bash
  user@clervaux-11:~$ cd /tmp/
  user@clervaux-11:~$ wget 'https://www.nas.nasa.gov/assets/npb/NPB3.4.3.tar.gz'
  user@clervaux-11:~$ tar -xzvf NPB3.4.3.tar.gz
  user@clervaux-11:~$ cd NPB3.4.3/NPB3.4-OMP
  user@clervaux-11:/tmp/NPB3.4.3/NPB3.4-OMP$ cp config/suite.def.template config/suite.def
  user@clervaux-11:/tmp/NPB3.4.3/NPB3.4-OMP$ cp config/make.def.template config/make.def
  user@clervaux-11:/tmp/NPB3.4.3/NPB3.4-OMP$ make -j$(nproc) suite
  ```
]
#slide(title: [Practical Example])[

  *Run benchmarks and save results:*
  ```bash
  user@clervaux-11:/tmp/NPB3.4.3/NPB3.4-OMP$ mkdir /tmp/benchs
  user@clervaux-11:/tmp/NPB3.4.3/NPB3.4-OMP$ for bench in $(ls bin); do ./bin/$bench | tee /tmp/benchs/$bench.txt; done
  user@clervaux-11:/tmp/NPB3.4.3/NPB3.4-OMP$ cp -R /tmp/benchs ~/benchs-$OAR_JOBID
  ```
]

#slide(title: [Root Access with sudo-g5k])[

  *Gain administrator privileges:*
  ```bash
  user@clervaux-11:~$ sudo-g5k
  user@clervaux-11:~$ sudo -iu root
  root@clervaux-11:~#
  ```

  *Now you can:*
  - Install system packages: `apt update && apt install ...`
  - Modify system configuration
  - Install drivers, kernels, file systems, etc.

  ⚠️ *Warning:* Using `sudo-g5k` triggers full node redeployment after job ends
]

#new-section-slide([Advanced resource management])

#slide(title: [Advanced resource selection])[

  *Reserve specific cluster:*
  ```bash
  user@fluxembourg:~$ oarsub -r now -p clervaux
  ```

  *Reserve by hardware properties:*
  ```bash
  user@fluxembourg:~$ oarsub -r now -p "core_count > 8"
  user@fluxembourg:~$ oarsub -r now -p "cputype LIKE 'Intel Xeon%'"
  ```

  *Reserve exotic resources:*
  ```bash
  user@fluxembourg:~$ oarsub -r now -p vianden -t exotic
  ```

  *Reserve multiple nodes for longer time:*
  ```bash
  user@fluxembourg:~$ oarsub -r now -l nodes=2,walltime=4:00
  ```
]

#slide(title: [Advanced reservations])[

  *Schedule future reservations:*
  ```bash
  user@fluxembourg:~$ oarsub -r "2025-06-10 10:00, 2025-06-10 12:00"
  ```

  *Extend running reservation:*
  ```bash
  user@fluxembourg:~$ oarwalltime <oar_job_id> +1:00
  ```

  *Always clean up when done:*
  ```bash
  user@clervaux-11:~$ logout
  [user@fluxembourg|~]$ oardel <JOB_ID>
  ```

  💡 *Good practice:* Delete unused reservations to free resources for others
]

#new-section-slide([System deployment])

#slide(title: [System deployment])[
// TODO: Add a note concerning kaenv3
  *Reserve node for deployment:*
  ```bash
  user@fluxembourg:~$ oarsub -r now -t deploy -q testing
  ```

  *Deploy custom environment:*
  ```bash
  user@fluxembourg:~$ kadeploy3 -e debian12-min -m clervaux-3.luxembourg.grid5000.fr
  # or with job ID:
  user@fluxembourg:~$ oarsub -C <job_id>
  user@fluxembourg:~$ kadeploy3 -e debian12-min
  ```
]
#slide(title: [System deployment])[

  *Available environments:*
  - `debian11-min`, `debian12-min` - Minimal Debian
  - `debian11-nfs`, `debian12-nfs` - With NFS home mounting  
  - `ubuntu2404-min`, `ubuntu2404-nfs` - Ubuntu variants

  *List all environments:*
  ```bash
  user@fluxembourg:~$ kaenv3
  ```
]

#slide(title: [Serial console access])[

  *Access node console (useful for debugging):*
  ```bash
  user@fluxembourg:~$ kaconsole3 -m clervaux-3
  ```

  *Reboot deployed node:*
  ```bash
  user@fluxembourg:~$ kareboot3 simple -m clervaux-3
  ```

  *Exit console:* Type `&.` or press `ESC` 4 times

  *Use case:* Recover from network misconfigurations, debug boot issues
]

#new-section-slide([Experiment automation])

#slide(title: [Commands])[

  *Submit command with reservation:*
  ```bash
  user@fluxembourg:~$ oarsub -r now "lscpu > lscpu.txt"
  ```

  *Script-based experiments:*
  ```bash
  user@fluxembourg:~$ chmod +x experiment.sh
  user@fluxembourg:~$ oarsub -t deploy -r now "./experiment.sh" -q testing
  ```

  *Monitor job output:*
  ```bash
  user@fluxembourg:~$ multitail -i OAR.<jobid>.stdout -i OAR.<jobid>.stderr
  ```
  
  #set par(leading: 0.2em)
  *Day vs Night usage:*
  - Day: Interactive work, shorter reservations
  - Night/Weekends: Automated, longer experiments
]

#slide(title: [REST API Usage])[

  *Programmatic resource discovery:*
  - Sites: *#link("https://api.grid5000.fr/stable/sites/")*
  - Luxembourg clusters: *#link("https://api.grid5000.fr/stable/sites/luxembourg/clusters/")*
  - Node details: *#link("https://api.grid5000.fr/stable/sites/luxembourg/clusters/vianden/nodes/vianden-1")*

]
  
#slide(title: [REST API Usage])[
  *Automated job submission:*
  #set par(leading: 0.2em)
  ```python
  import requests

  payload = {
      'resources': 'nodes=1',
      'types': ['deploy'], 
      'command': './experiment.sh',
      'properties': f"cluster='{cluster}'"
  }
  job = requests.post(api_job_url, data=payload).json()
  ```
]

#new-section-slide([Summary and Wrap-up])

#slide(title: [Summary: Key Commands])[

  #table(
    columns: (1fr, 2fr),
    [*Command*], [*Purpose*],
    [`oarsub -r now`], [Reserve resource immediately],
    [`oarstat -u`], [Check your reservations],
    [`oarsub -C`], [Connect to reserved node],  
    [`oardel <job_id>`], [Delete reservation],
    [`sudo-g5k`], [Gain root access],
    [`kadeploy3 -e <env>`], [Deploy OS environment],
    [`kaconsole3 -m <node>`], [Access serial console],
    [`oarwalltime <job> +1:00`], [Extend reservation]
  )
]

#slide(title: [Best Practices])[

  *Resource Management:*
  - Always delete unused reservations
  - Use `/tmp/` for intensive I/O operations  
  - Copy important results to home directory
  - Plan reservations during off-peak hours

  *Experimentation:*
  - Test interactively first, then automate
  - Use version control for experiment scripts
  - Document your environment and dependencies
  - Monitor resource usage and platform status

  *Troubleshooting:*
  - Check Grid'5000 status page for issues
  - Use `kaconsole3` for network problems
  - Monitor job output files for errors
]

#slide(title: [Next Steps & Resources])[

  *Advanced Topics:*
  - Network reconfiguration (KaVLAN)
  // - Energy monitoring
  - Multi-site experiments
  - Custom environment creation

  *Key Documentation:*
  - Tutorial: *#link("https://hpc-docs.uni.lu/g5k/getting-started-g5k/")*
  - Main wiki: *#link("https://www.grid5000.fr/w/Home")*
  // - API documentation: https://www.grid5000.fr/w/API
  // - Experiment scripting: https://www.grid5000.fr/w/Experiment_scripting_tutorial

  *Support:*
  - Support page: *#link("https://www.grid5000.fr/w/Support")*
  - User mailing list and forums
]

#empty-slide()[
    *Questions?*
]
