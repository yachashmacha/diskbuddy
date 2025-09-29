import os
import sys
import argparse
import subprocess

def main():
    p = argparse.ArgumentParser(description="DiskBuddy")
    s = p.add_subparsers(dest='cmd')

    s.add_parser('list').set_defaults(f=lambda a: subprocess.call(['lsblk']))
    s.add_parser('usage').set_defaults(f=lambda a: subprocess.call(['df', '-h']))

    m = s.add_parser('mount')
    m.add_argument('d')
    m.add_argument('p')
    m.set_defaults(f=lambda a: subprocess.call(['mount', a.d, a.p]))

    u = s.add_parser('unmount')
    u.add_argument('d')
    u.set_defaults(f=lambda a: subprocess.call(['umount', a.d]))

    fmt = s.add_parser('format')
    fmt.add_argument('d')
    fmt.add_argument('t')
    fmt.set_defaults(f=lambda a: subprocess.call(['mkfs', '-t', a.t, a.d]))

    c = s.add_parser('create')
    c.add_argument('d')
    c.add_argument('start')
    c.add_argument('end')
    c.set_defaults(f=lambda a: os.system(f"echo -e 'n

{a.start}
{a.end}
w' | fdisk {a.d}"))

    b = s.add_parser('backup')
    b.add_argument('d')
    b.add_argument('t')
    b.set_defaults(f=lambda a: subprocess.call(['dd', f'if={a.d}', f'of={a.t}', 'bs=4M', 'status=progress']))

    r = s.add_parser('restore')
    r.add_argument('i')
    r.add_argument('t')
    r.set_defaults(f=lambda a: subprocess.call(['dd', f'if={a.i}', f'of={a.t}', 'bs=4M', 'status=progress']))

    args = p.parse_args()
    if hasattr(args, 'f'):
        args.f(args)
    else:
        p.print_help()

if __name__ == "__main__":
    main()
